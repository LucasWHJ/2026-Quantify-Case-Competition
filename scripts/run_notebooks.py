"""Execute notebooks in isolated temporary kernels without global installation."""
from pathlib import Path
import argparse
import json
import os
import sys
import tempfile
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager


def execute(path, root, kernel_dir):
    manager = KernelManager(kernel_name="quantify", kernel_spec_manager=KernelSpecManager(kernel_dirs=[str(kernel_dir)]))
    notebook = nbformat.read(path, as_version=4)
    client = NotebookClient(notebook, km=manager, timeout=240, allow_errors=False,
                            resources={"metadata": {"path": str(root)}})
    client.execute(env=os.environ.copy())
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    print(f"Executed {path.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    paths = [root / "analysis/pilot-economics.ipynb"] if args.pilot_only else sorted((root / "analysis").glob("*.ipynb"))
    with tempfile.TemporaryDirectory(prefix="quantify-kernel-") as temp:
        kernel_dir = Path(temp)
        spec = kernel_dir / "quantify"
        spec.mkdir()
        (spec / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "Quantify analysis", "language": "python"}), encoding="utf-8")
        for path in paths:
            execute(path, root, kernel_dir)


if __name__ == "__main__":
    main()
