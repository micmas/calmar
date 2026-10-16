"""
ollama_client.py — thin, dependency-free client for local Ollama inference.

Shared by extract.py and auto_review.py so both get the same context
sizing, truncation detection, and error messages.

Nothing here talks to a third-party API. All traffic goes to a local
Ollama server (default http://localhost:11434), which is the point:
paper full text and verbatim quotes never leave the machine.

Design notes
------------
* Plain urllib — no SDK, no new dependency.
* `num_ctx` is sized from the actual prompt. Ollama SILENTLY TRUNCATES
  anything past num_ctx; that truncation is the single most common
  cause of a local model "failing" a task it could otherwise do.
* `format` accepts a JSON Schema. Constraining decoding to a schema is
  by far the biggest reliability win for small/mid models asked to
  produce structured output — prefer it over "please reply in YAML".
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("APHASIA_LOCAL_MODEL", "gemma4:26b")

NUM_CTX_FLOOR = 8192       # never go below this
NUM_CTX_HEADROOM = 1.35    # prompt tokens * this, then round up to 4K
NUM_CTX_CEILING = 262144   # gemma4 tops out at 256K


class OllamaError(RuntimeError):
    """Raised for any failure talking to the local Ollama server."""


def normalize_host(host: str | None) -> str:
    host = (host or DEFAULT_HOST).rstrip("/")
    if not host.startswith(("http://", "https://")):
        host = "http://" + host
    return host


def estimate_tokens(text: str) -> int:
    """Rough char/4 heuristic — fine for sizing a context window."""
    return len(text) // 4


def autosize_num_ctx(prompt: str, max_tokens: int,
                     floor: int = NUM_CTX_FLOOR) -> int:
    need = int(estimate_tokens(prompt) * NUM_CTX_HEADROOM) + max_tokens
    need = max(need, floor)
    need = ((need + 4095) // 4096) * 4096
    return min(need, NUM_CTX_CEILING)


def is_local(host: str) -> bool:
    """True if `host` points at this machine. Used to warn loudly when
    OLLAMA_HOST has been pointed somewhere remote — which would quietly
    defeat the whole reason for running locally."""
    h = normalize_host(host)
    return any(x in h for x in ("localhost", "127.0.0.1", "0.0.0.0", "::1"))


def check_model_available(model: str, host: str = DEFAULT_HOST,
                          timeout: int = 15) -> tuple[bool, str]:
    """Return (available, message). Cheap preflight so a long batch run
    fails in 2 seconds instead of on paper 1 of 40."""
    host = normalize_host(host)
    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=timeout) as r:
            tags = json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return False, (f"Couldn't reach Ollama at {host} ({e.reason}).\n"
                       f"  Start it with:  ollama serve")
    names = [m.get("name", "") for m in tags.get("models", [])]
    if model in names:
        return True, f"{model} available at {host}"
    # Ollama treats "foo" and "foo:latest" as the same thing.
    if any(n.split(":")[0] == model.split(":")[0] for n in names):
        close = [n for n in names if n.split(":")[0] == model.split(":")[0]]
        return False, (f"{model!r} not found, but these related tags are "
                       f"local: {close}. Use one of those, or "
                       f"`ollama pull {model}`.")
    return False, (f"{model!r} is not pulled. Run:  ollama pull {model}\n"
                   f"  Local models: {names or '(none)'}")


def chat(prompt: str,
         *,
         model: str = DEFAULT_MODEL,
         system: str | None = None,
         max_tokens: int = 4000,
         host: str = DEFAULT_HOST,
         num_ctx: int | None = None,
         temperature: float = 0.0,
         seed: int | None = None,
         fmt: str | dict | None = None,
         timeout: int = 3600,
         verbose: bool = True) -> dict:
    """POST /api/chat and return a result dict.

    Returns {text, prompt_tokens, output_tokens, truncated_input,
             truncated_output, duration_s, num_ctx}.

    `fmt` may be "json" or a JSON Schema dict (constrained decoding).
    Raises OllamaError on transport failure or empty output.
    """
    host = normalize_host(host)
    full = (system or "") + prompt
    if num_ctx is None:
        num_ctx = autosize_num_ctx(full, max_tokens)

    options: dict = {
        "num_ctx": num_ctx,
        "num_predict": max_tokens,
        "temperature": temperature,
    }
    if seed is not None:
        options["seed"] = seed

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload: dict = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": options,
    }
    if fmt is not None:
        payload["format"] = fmt

    if verbose:
        print(f"  → local {model} @ {host} "
              f"(num_ctx={num_ctx:,}, num_predict={max_tokens:,}, "
              f"temp={temperature})")

    req = urllib.request.Request(
        f"{host}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        if e.code == 404:
            raise OllamaError(
                f"Ollama has no model named {model!r} (HTTP 404).\n"
                f"  Pull it:  ollama pull {model}\n"
                f"  Server said: {detail}") from e
        raise OllamaError(f"Ollama HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise OllamaError(
            f"Couldn't reach Ollama at {host} ({e.reason}).\n"
            f"  Start it with:  ollama serve\n"
            f"  Or point elsewhere with --ollama-host / OLLAMA_HOST.") from e
    except TimeoutError as e:
        raise OllamaError(
            f"Ollama timed out after {timeout}s. Large num_ctx on a big "
            f"model can be very slow — try a smaller --num-ctx.") from e

    text = (body.get("message") or {}).get("content", "") or ""
    n_in = body.get("prompt_eval_count")
    n_out = body.get("eval_count")
    dur_s = (body.get("total_duration") or 0) / 1e9

    # The two silent failure modes worth catching explicitly.
    trunc_in = bool(n_in and n_in >= num_ctx - 8)
    trunc_out = body.get("done_reason") == "length"

    if verbose:
        print(f"  ← {n_in} in + {n_out} out tokens in {dur_s:.0f}s "
              f"(done_reason={body.get('done_reason')})")
    if trunc_in:
        print(f"  ⚠ prompt filled num_ctx ({n_in} ≥ {num_ctx:,}). Input was "
              f"likely TRUNCATED — rerun with a larger --num-ctx.")
    if trunc_out:
        print("  ⚠ output hit num_predict — response is probably "
              "incomplete. Rerun with a larger max-tokens.")

    if not text.strip():
        raise OllamaError(
            "Ollama returned an empty response. Usually means the model was "
            "killed for memory — try a smaller --num-ctx or a smaller model.")

    return {"text": text, "prompt_tokens": n_in, "output_tokens": n_out,
            "truncated_input": trunc_in, "truncated_output": trunc_out,
            "duration_s": dur_s, "num_ctx": num_ctx, "model": model}
