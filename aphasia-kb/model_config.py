"""
model_config.py — resolve which local model each task should use.

Single source of truth is models.yaml. Scripts ask for a ROLE
("extract", "review", "rag") rather than hardcoding a tag, so swapping
in a better local model is a one-line edit to models.yaml.

Run directly to see the resolved config and check what's pulled:

    python model_config.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
CONFIG_PATH = HERE / "models.yaml"

# Fallback if models.yaml is missing or unreadable — the pipeline should
# still run rather than dying over a config file.
_FALLBACK = {
    "default": "gemma4:26b",
    "roles": {
        "extract": {"model": None, "max_tokens": 16000, "num_ctx": None},
        "review":  {"model": None, "max_tokens": 2000,  "num_ctx": None},
        "rag":     {"model": None, "max_tokens": 1200,  "num_ctx": None},
    },
}

ROLE_ENV_VAR = {
    "extract": "APHASIA_EXTRACT_MODEL",
    "review":  "APHASIA_REVIEW_MODEL",
    "rag":     "APHASIA_RAG_MODEL",
}
GLOBAL_ENV_VAR = "APHASIA_LOCAL_MODEL"

_cache: dict | None = None


def load_config(path: Path = CONFIG_PATH) -> dict:
    global _cache
    if _cache is not None:
        return _cache
    try:
        cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        cfg = dict(_FALLBACK)
    except Exception as e:
        print(f"⚠ couldn't parse {path.name} ({e}); using built-in defaults",
              file=sys.stderr)
        cfg = dict(_FALLBACK)
    cfg.setdefault("default", _FALLBACK["default"])
    cfg.setdefault("roles", {})
    _cache = cfg
    return cfg


def resolve(role: str, cli_model: str | None = None) -> dict:
    """Resolve settings for `role`. Returns {model, max_tokens, num_ctx,
    source} where `source` explains which layer won — worth surfacing,
    because "why is it using that model?" is otherwise a guessing game.
    """
    cfg = load_config()
    spec = (cfg.get("roles") or {}).get(role) or {}

    file_model = spec.get("model") or cfg.get("default")
    role_env = os.environ.get(ROLE_ENV_VAR.get(role, ""))
    global_env = os.environ.get(GLOBAL_ENV_VAR)

    if cli_model:
        model, source = cli_model, "--model"
    elif role_env:
        model, source = role_env, ROLE_ENV_VAR[role]
    elif global_env:
        model, source = global_env, GLOBAL_ENV_VAR
    else:
        model, source = file_model, "models.yaml"

    return {
        "model": model,
        "max_tokens": spec.get("max_tokens") or 4000,
        "num_ctx": spec.get("num_ctx"),
        "source": source,
        "role": role,
    }


def model_for(role: str, cli_model: str | None = None) -> str:
    return resolve(role, cli_model)["model"]


def list_local_models(host: str | None = None,
                      name_filter: str | None = None) -> list[dict]:
    """Return locally-pulled models from Ollama, biggest first.

    Each item: {name, size_gb, params, family}. `name_filter` matches a
    substring of the tag (e.g. "gemma" to show only gemma variants).
    """
    import json
    import urllib.request
    from ollama_client import DEFAULT_HOST, normalize_host

    host = normalize_host(host or DEFAULT_HOST)
    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=15) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"couldn't reach Ollama at {host}: {e}") from e

    out = []
    for m in data.get("models", []):
        name = m.get("name", "")
        if name_filter and name_filter.lower() not in name.lower():
            continue
        det = m.get("details") or {}
        out.append({
            "name": name,
            "size_gb": (m.get("size") or 0) / 1e9,
            "params": det.get("parameter_size", "?"),
            "family": det.get("family", "?"),
        })
    out.sort(key=lambda x: x["size_gb"], reverse=True)
    return out


def pick_model_interactive(host: str | None = None,
                           name_filter: str | None = None,
                           purpose: str = "") -> str | None:
    """Show a numbered menu of local models and return the chosen tag.

    Returns None if the user cancels or nothing is available. Meant for a
    terminal; callers should fall back to the configured default when
    this returns None (e.g. stdin isn't a TTY).
    """
    import sys

    if not sys.stdin.isatty():
        return None
    try:
        models = list_local_models(host, name_filter)
    except RuntimeError as e:
        print(f"⚠ {e}")
        return None
    if not models:
        flt = f" matching {name_filter!r}" if name_filter else ""
        print(f"No local models{flt}. Pull one first, e.g. "
              f"`ollama pull gemma4:12b`.")
        return None

    title = f"Choose a model{f' for {purpose}' if purpose else ''}:"
    print("\n" + title)
    for i, m in enumerate(models, 1):
        print(f"  {i}. {m['name']:<26} {m['size_gb']:5.1f} GB  "
              f"{m['params']:>6}  {m['family']}")
    print("  q. cancel (use the configured default)")

    while True:
        try:
            choice = input("› ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if choice in ("q", "", "cancel"):
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            picked = models[int(choice) - 1]["name"]
            print(f"→ using {picked}")
            return picked
        print(f"  enter 1–{len(models)}, or q")


def _main() -> int:
    from ollama_client import DEFAULT_HOST, check_model_available, is_local

    host = os.environ.get("OLLAMA_HOST", DEFAULT_HOST)
    print(f"config : {CONFIG_PATH}")
    print(f"host   : {host}"
          f"{'' if is_local(host) else '   ⚠ NOT LOCAL — text would leave this machine'}")
    print()

    ok_all = True
    for role in ("extract", "review", "rag"):
        r = resolve(role)
        ok, msg = check_model_available(r["model"], host)
        ok_all &= ok
        mark = "✓" if ok else "✗"
        ctx = r["num_ctx"] or "auto"
        print(f"{mark} {role:<8} {r['model']:<20} "
              f"max_tokens={r['max_tokens']:<6} num_ctx={ctx}")
        print(f"  {'':<9}(from {r['source']})")
        if not ok:
            print(f"  {'':<9}{msg}")
    print()
    print("Edit models.yaml to change any of these." if ok_all else
          "Pull the missing models, or edit models.yaml to point at what "
          "you have.")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(_main())
