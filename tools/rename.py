"""Genera resources-dlc3/items.xml e pocketitems.xml con i nomi alla Risacca.
Uso: python3 tools/rename.py <cartella_estratta> | --selftest"""
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


RULES = [(re.compile(p, re.I), r) for p, r in [
    (r"\bMega Satan\b", "Mega Stanley Kubrick"),
    (r"\bkeys?\b", "Chiaviz-Chiavoz"),
    (r"\bbombs?\b", "Bombiz-Bomboz"),
    (r"\bboss(es)?\b", "Beppe Bossicchio"),
    (r"\bBumbo\b", "Bumbazzo"),
    (r"\bGreed\b", "Ballerino di Flamenco"),
]]


def rename_text(s):
    if s == "Incubus":
        return "Il buddy più forte del gioco"
    for rx, rep in RULES:
        s = rx.sub(rep, s)
    return s


def convert(src, table, dst):
    tree = ET.parse(src)
    for el in tree.getroot().iter():
        for attr in ("name", "description"):
            v = el.get(attr)
            if v is None:
                continue
            text = table.get(v.lstrip("#"), v) if v.startswith("#") else v
            new = rename_text(text)
            if new != text:
                el.set(attr, new)
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    tree.write(dst, encoding="utf-8", xml_declaration=True)


def selftest():
    cases = {
        "Skeleton Key": "Skeleton Chiaviz-Chiavoz",
        "Bobby-Bomb": "Bobby-Bombiz-Bomboz",
        "Bomber Boy": "Bomber Boy",
        "Keeper's Box": "Keeper's Box",
        "Mom's Key": "Mom's Chiaviz-Chiavoz",
        "+5 bombs": "+5 Bombiz-Bomboz",
        "Boss Rush": "Beppe Bossicchio Rush",
        "Mega Satan": "Mega Stanley Kubrick",
        "Incubus": "Il buddy più forte del gioco",
        "Bumbo": "Bumbazzo",
        "Bumbo's Heart": "Bumbazzo's Heart",
        "Greed's Gullet": "Ballerino di Flamenco's Gullet",
        "Ultra Greedier": "Ultra Greedier",
    }
    for src, want in cases.items():
        got = rename_text(src)
        assert got == want, (src, got, want)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "items.xml").write_text(
            '<items><passive id="1" name="#SAD_ONION_NAME" description="Tears up"/>'
            '<active id="2" name="#KEY_NAME" description="#KEY_DESC"/></items>', encoding="utf-8")
        (d / "stringtable.sta").write_text(
            '<stringtable><category name="Items">'
            '<key name="SAD_ONION_NAME"><string>Sad Onion</string></key>'
            '<key name="KEY_NAME"><string>Skeleton Key</string><string>Chiave</string></key>'
            '<key name="KEY_DESC"><string>99 keys</string></key>'
            '</category></stringtable>', encoding="utf-8")
        table = load_table(d / "stringtable.sta")
        convert(d / "items.xml", table, d / "out.xml")
        out = list(ET.parse(d / "out.xml").getroot())
        assert len(out) == 2, out
        assert out[0].attrib == {"id": "1", "name": "#SAD_ONION_NAME", "description": "Tears up"}, out[0].attrib
        assert out[1].get("name") == "Skeleton Chiaviz-Chiavoz", out[1].attrib
        assert out[1].get("description") == "99 Chiaviz-Chiavoz", out[1].attrib
    print("OK")


def load_table(path):
    """key name (senza '#') -> prima <string> (inglese)."""
    table = {}
    for key in ET.parse(path).getroot().iter("key"):
        s = key.find("string")
        if s is not None and s.text:
            table.setdefault(key.get("name").lstrip("#"), s.text)
    return table


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        src = Path(sys.argv[1])
        table = load_table(src / "stringtable.sta")
        for f in ("items.xml", "pocketitems.xml"):
            convert(src / f, table, Path(__file__).resolve().parent.parent / "resources-dlc3" / f)
