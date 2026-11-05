"""Crea dist/risacca-mod.zip con solo i file della mod. Uso: python3 tools/build.py [--selftest]"""
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["metadata.xml", "main.lua", "logic.lua", "content", "resources", "resources-dlc3"]
BANNED = ("docs/", "tools/", "tests/", "extracted/")
# git-ignored: senza questi file lo zip uscirebbe senza rinomine
REQUIRED = ["resources-dlc3/items.xml", "resources-dlc3/pocketitems.xml", "resources-dlc3/info_display.xml"]
# Versione del gioco da cui viene resources-dlc3/ e quante voci hanno i suoi file (estratti e generati devono
# coincidere): definizioni vecchie dopo una patch possono far crashare il gioco. A ogni patch si rigenera e si aggiorna.
GAME_VERSION = "1.9.7.17.J460"
VANILLA_COUNTS = {"resources-dlc3/items.xml": 959, "resources-dlc3/pocketitems.xml": 148}
# Gli ID degli oggetti della mod dipendono dall'ordine in content/items.xml: cambiarlo cambia gli oggetti
# di una run continuata. Si aggiunge solo in fondo, qui e in items.xml; non si toglie mai una voce.
ORDER = {
    "collectible": ["Ho Rotto il Gioco", "-1 al Dead God", "Non Vi Rubo Altro Tempo", "La Mossa del Pro Player",
                    "Potrebbe Stare Qua", "Il Miracolo di San Gennaruzzo", "La Trollata", "Fai Così, Fai Così",
                    "Tacchinardi", "Tacchinibus", "Il Tacchino della Domenica", "Sono un Idiota", "Fermi Tutti"],
    "trinket": ["Win Streak", "Che Fai, Te Ne Privi?", "Mannaggia a Lui"],
}


def item_order(xml_text):
    order = {"collectible": [], "trinket": []}
    for e in ET.fromstring(xml_text):
        order["trinket" if e.tag == "trinket" else "collectible"].append(e.get("name"))
    return order


def order_errors(order, saved=ORDER):
    return [kind for kind in saved if order[kind] != saved[kind]]


def missing_required(root=ROOT):
    return [name for name in REQUIRED if not (Path(root) / name).is_file()]


def count_errors(root=ROOT):
    return [name for name, n in VANILLA_COUNTS.items() if len(ET.parse(Path(root) / name).getroot()) != n]


def build(dst, root=ROOT):
    missing = missing_required(root)
    if missing:
        sys.exit("File mancanti: " + ", ".join(missing) + "\nRigenerali con: python3 tools/rename.py extracted")
    wrong = count_errors(root)
    if wrong:
        sys.exit("Numero di voci diverso da VANILLA_COUNTS in tools/build.py (" + ", ".join(wrong) + ", gioco "
                 + GAME_VERSION + ").\nSe il gioco è stato aggiornato, riestrai i file, rilancia tools/rename.py "
                 "e aggiorna GAME_VERSION e VANILLA_COUNTS.")
    wrong = order_errors(item_order((root / "content" / "items.xml").read_text(encoding="utf-8")))
    if wrong:
        sys.exit("Ordine di content/items.xml diverso da ORDER in tools/build.py (" + ", ".join(wrong) + ").\n"
                 "Aggiungi gli oggetti solo in fondo, in tutti e due, e non toglierne: cambierebbero gli ID.")
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
    assert order_errors(item_order((ROOT / "content" / "items.xml").read_text(encoding="utf-8"))) == []
    swapped = {"collectible": ORDER["collectible"][1::-1] + ORDER["collectible"][2:], "trinket": ORDER["trinket"]}
    assert order_errors(swapped) == ["collectible"]
    assert order_errors({"collectible": ORDER["collectible"], "trinket": ORDER["trinket"][:-1]}) == ["trinket"]
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
            (root / name).write_text("<items>" + "<x />" * VANILLA_COUNTS.get(name, 0) + "</items>")
        assert count_errors(root) == []
        (root / REQUIRED[0]).write_text("<items />")
        assert count_errors(root) == [REQUIRED[0]]
        (root / REQUIRED[0]).write_text("<items>" + "<x />" * VANILLA_COUNTS[REQUIRED[0]] + "</items>")
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
