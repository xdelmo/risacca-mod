"""Crea dist/risacca-mod.zip con solo i file della mod. Uso: python3 tools/build.py [--selftest]"""
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["metadata.xml", "main.lua", "logic.lua", "content", "resources", "resources-dlc3"]
BANNED = ("docs/", "tools/", "tests/", "extracted/")


def build(dst):
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for name in INCLUDE:
            p = ROOT / name
            files = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.is_file()) if p.is_dir() else []
            for f in files:
                z.write(f, "risacca-mod/" + f.relative_to(ROOT).as_posix())
    return dst


def selftest():
    with tempfile.TemporaryDirectory() as d:
        names = zipfile.ZipFile(build(Path(d) / "t.zip")).namelist()
    for n in ("metadata.xml", "main.lua", "logic.lua"):
        assert "risacca-mod/" + n in names, (n, names)
    assert not [n for n in names if n.removeprefix("risacca-mod/").startswith(BANNED)], names
    assert not [n for n in names if "/." in n], names
    print("OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        print(build(ROOT / "dist" / "risacca-mod.zip"))
