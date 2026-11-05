"""Crea dist/risacca-mod.zip con solo i file della mod. Uso: python3 tools/build.py [--selftest]"""
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["metadata.xml", "main.lua", "logic.lua", "content", "resources", "resources-dlc3"]
BANNED = ("docs/", "tools/", "tests/", "extracted/")
# git-ignored: senza questi file lo zip uscirebbe senza rinomine
REQUIRED = ["resources-dlc3/items.xml", "resources-dlc3/pocketitems.xml", "resources-dlc3/info_display.xml"]


def missing_required(root=ROOT):
    return [name for name in REQUIRED if not (Path(root) / name).is_file()]


def build(dst, root=ROOT):
    missing = missing_required(root)
    if missing:
        sys.exit("File mancanti: " + ", ".join(missing) + "\nRigenerali con: python3 tools/rename.py extracted")
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for name in INCLUDE:
            p = root / name
            files = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.is_file()) if p.is_dir() else []
            for f in files:
                z.write(f, "risacca-mod/" + f.relative_to(root).as_posix())
        # alla radice dello zip, fuori dalla mod; CRLF per il Blocco note, comunque sia stato fatto il checkout
        z.writestr("readme.txt", (root / "readme.txt").read_bytes().replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    return dst


def selftest():
    with tempfile.TemporaryDirectory() as d:
        assert missing_required(d) == REQUIRED
        # copia della mod con resources-dlc3/ finto: il selftest gira anche su un clone pulito
        root = Path(d) / "mod"
        root.mkdir()
        for name in INCLUDE[:-1] + ["readme.txt"]:
            src = ROOT / name
            (shutil.copytree if src.is_dir() else shutil.copy2)(src, root / name)
        for name in REQUIRED:
            (root / name).parent.mkdir(parents=True, exist_ok=True)
            (root / name).write_text("<items />")
        with zipfile.ZipFile(build(Path(d) / "t.zip", root)) as z:
            names = z.namelist()
            readme = z.read("readme.txt")
    assert readme.count(b"\n") == readme.count(b"\r\n") > 0
    assert not [w for w in (b"workshop", b"github") if w in readme.lower()], "il readme non deve rimandare altrove"
    for n in ["metadata.xml", "main.lua", "logic.lua"] + REQUIRED:
        assert "risacca-mod/" + n in names, (n, names)
    assert not [n for n in names if n.removeprefix("risacca-mod/").startswith(BANNED)], names
    assert not [n for n in names if "/." in n], names
    print("OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        print(build(ROOT / "dist" / "risacca-mod.zip"))
