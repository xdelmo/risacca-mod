"""Tavola di leggibilità di tutte le icone in resources/gfx/items/collectibles/ (anche quelle future).

Per ogni icona: 1x e 2x su sfondo scuro (HUD) e chiaro (piedistallo), più la versione in grigi,
dove un simbolo con poco contrasto di luminosità (il vecchio "-1" rosso sulla pelle) sparisce.
Se esiste extracted/gfx/items/collectibles/, accanto mette gli sprite vanilla per il confronto.

    python3 tools/leggibilita.py             # → dist/leggibilita.png
    python3 tools/leggibilita.py --selftest
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "resources/gfx/items/collectibles"
VANILLA = ROOT / "extracted/gfx/items/collectibles"
BG = [(24, 20, 20), (120, 104, 96)]  # HUD, piedistallo
CELL, LABEL = 72, 120


def row(im):
    """Una riga: 1x e 2x su ogni sfondo, poi 2x in grigi."""
    grey = im.convert("LA").convert("RGBA")
    out = Image.new("RGBA", (CELL * 5, CELL), (255, 255, 255, 255))
    for i, (src, bg, k) in enumerate([(im, BG[0], 1), (im, BG[0], 2), (im, BG[1], 1), (im, BG[1], 2), (grey, BG[1], 2)]):
        tile = Image.new("RGBA", (CELL, CELL), bg + (255,))
        s = src.resize((32 * k, 32 * k), Image.NEAREST)
        tile.alpha_composite(s, ((CELL - s.width) // 2, (CELL - s.height) // 2))
        out.paste(tile, (i * CELL, 0))
    return out


def sheet():
    icons = sorted(ICONS.glob("*.png"))
    refs = sorted(VANILLA.glob("*.png"))[:8]
    entries = [(p.stem, p) for p in icons] + [("vanilla " + p.stem, p) for p in refs]
    out = Image.new("RGBA", (LABEL + CELL * 5, CELL * len(entries)), (255, 255, 255, 255))
    d = ImageDraw.Draw(out)
    for i, (name, p) in enumerate(entries):
        out.paste(row(Image.open(p).convert("RGBA").crop((0, 0, 32, 32))), (LABEL, i * CELL))
        d.text((4, i * CELL + CELL // 2 - 5), name[:18], fill=(0, 0, 0, 255))
    return out, len(icons)


def selftest():
    im, n = sheet()
    assert n == len(list(ICONS.glob("*.png"))) > 0
    assert im.size == (LABEL + CELL * 5, im.height) and im.height >= CELL * n
    print("SELFTEST OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        im, _ = sheet()
        (ROOT / "dist").mkdir(exist_ok=True)
        im.save(ROOT / "dist/leggibilita.png")
        print(ROOT / "dist/leggibilita.png")
