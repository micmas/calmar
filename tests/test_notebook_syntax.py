"""Static syntax checks for saved notebook code cells; no cells are executed."""

import ast
import json
from pathlib import Path

from IPython.core.inputtransformer2 import TransformerManager


ROOT = Path(__file__).resolve().parents[1]


def test_saved_notebook_code_cells_compile():
    transformer = TransformerManager()
    failures = []
    for name in ("calmar-guided.ipynb", "lesion-interpretation-pipeline.ipynb"):
        notebook = json.loads((ROOT / name).read_text())
        for cell in notebook["cells"]:
            if cell.get("cell_type") != "code":
                continue
            cell_id = cell.get("id", "unknown")
            source = transformer.transform_cell("".join(cell.get("source", [])))
            try:
                compile(source, f"{name}:{cell_id}", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
            except SyntaxError as error:
                failures.append(f"{name}:{cell_id}:{error.lineno}: {error.msg}")
    assert not failures, "Notebook syntax errors:\n" + "\n".join(failures)
