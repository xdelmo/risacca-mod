"""Leggibilità e distinguibilità di tutte le icone in resources/gfx/items/collectibles/ (anche quelle future).

Tavola: per ogni icona 1x e 2x su sfondo scuro (HUD) e chiaro (piedistallo), la versione in grigi,
dove un simbolo con poco contrasto di luminosità (il vecchio "-1" rosso sulla pelle) sparisce,
e l'oggetto vanilla più somigliante, preso dalla tavola di riferimento in docs/.
Report: per ogni icona l'icona della mod e l'oggetto vanilla più somiglianti, con il punteggio.

    python3 tools/leggibilita.py             # → dist/leggibilita.png e report; esce con 1 se una coppia è da rivedere
    python3 tools/leggibilita.py --selftest
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "resources/gfx/items/collectibles"
# git-ignored: è la grafica del gioco. Si scarica da The Spriters Resource (Rebirth > Items (Repentance))
REFERENCE = ROOT / "docs/PC _ Computer - The Binding of Isaac_ Rebirth - Items - Items (Repentance).png"
BG = [(24, 20, 20), (120, 104, 96)]  # HUD, piedistallo
CELL, LABEL = 72, 120
# shortcut: soglie tarate a occhio su 13 icone e sul 90° percentile vanilla (0.81), da rivedere se danno falsi allarmi
LIMIT_MOD, LIMIT_VANILLA = 0.7, 0.8


def row(im, twin):
    """Una riga: 1x e 2x su ogni sfondo, 2x in grigi, poi il sosia vanilla a 2x."""
    grey = im.convert("LA").convert("RGBA")
    tiles = [(im, BG[0], 1), (im, BG[0], 2), (im, BG[1], 1), (im, BG[1], 2), (grey, BG[1], 2), (twin, BG[1], 2)]
    out = Image.new("RGBA", (CELL * len(tiles), CELL), (255, 255, 255, 255))
    for i, (src, bg, k) in enumerate(tiles):
        tile = Image.new("RGBA", (CELL, CELL), bg + (255,))
        s = src.resize((32 * k, 32 * k), Image.NEAREST)
        tile.alpha_composite(s, ((CELL - s.width) // 2, (CELL - s.height) // 2))
        out.paste(tile, (i * CELL, 0))
    return out


def vanilla():
    """Gli oggetti della tavola di riferimento, griglia di celle 32x32: [(nome, immagine)]."""
    if not REFERENCE.is_file():
        sys.exit(f"Manca la tavola di riferimento: {REFERENCE.relative_to(ROOT)}")
    sheet = Image.open(REFERENCE).convert("RGBA")
    cells = []
    for y in range(0, sheet.height, 32):
        for x in range(0, sheet.width, 32):
            cell = sheet.crop((x, y, x + 32, y + 32))
            if cell.getbbox():
                cells.append((f"vanilla riga {y // 32 + 1} col {x // 32 + 1}", cell))
    return cells


def centered(im):
    """{(x, y): rgb} dei pixel opachi, con l'ingombro centrato: conta la forma, non la posizione."""
    x0, y0, x1, y1 = im.getbbox()
    dx, dy = (32 - x1 - x0) // 2, (32 - y1 - y0) // 2
    return {(x + dx, y + dy): im.getpixel((x, y))[:3]
            for x in range(x0, x1) for y in range(y0, y1) if im.getpixel((x, y))[3] > 0}


def similarity(a, b):
    """Da 0 a 1: quanto si sovrappongono le forme, ridotto dalla differenza di colore dove si sovrappongono."""
    shared = a.keys() & b.keys()
    if not shared:
        return 0.0
    distance = sum(max(abs(p - q) for p, q in zip(a[c], b[c])) for c in shared) / len(shared) / 255
    return len(shared) / len(a.keys() | b.keys()) * (1 - distance)


def closest(c, others):
    return max(others, key=lambda o: similarity(c, o[1]))


def analyze():
    """[(nome, immagine, (sosia nella mod, punteggio), (sosia vanilla, punteggio), immagine del sosia vanilla)]."""
    icons = [(p.stem, Image.open(p).convert("RGBA").crop((0, 0, 32, 32))) for p in sorted(ICONS.glob("*.png"))]
    prints = [(n, centered(im)) for n, im in icons]
    refs = vanilla()
    ref_prints = [(n, centered(im)) for n, im in refs]
    ref_images = dict(refs)
    out = []
    for (name, im), (_, c) in zip(icons, prints):
        mod_name, mod_c = closest(c, [p for p in prints if p[0] != name])
        van_name, van_c = closest(c, ref_prints)
        out.append((name, im, (mod_name, similarity(c, mod_c)), (van_name, similarity(c, van_c)), ref_images[van_name]))
    return out


def sheet(results):
    out = Image.new("RGBA", (LABEL + CELL * 6, CELL * len(results)), (255, 255, 255, 255))
    d = ImageDraw.Draw(out)
    for i, (name, im, _, _, twin) in enumerate(results):
        out.paste(row(im, twin), (LABEL, i * CELL))
        d.text((4, i * CELL + CELL // 2 - 5), name[:18], fill=(0, 0, 0, 255))
    return out


def selftest():
    a = {(x, y): (200, 0, 0) for x in range(10) for y in range(10)}
    assert similarity(a, a) == 1
    assert similarity(a, {c: (0, 200, 200) for c in a}) < 0.5  # stessa forma, altro colore
    assert similarity(a, {(x + 20, y): v for (x, y), v in a.items()}) == 0
    off = Image.new("RGBA", (32, 32))
    off.putpixel((3, 3), (1, 2, 3, 255))
    assert centered(off).keys() == {(15, 15)}
    if not REFERENCE.is_file():  # clone pulito o CI: la tavola non è nella repo
        print("SELFTEST OK (senza la tavola di riferimento)")
        return
    refs = vanilla()
    assert len(refs) > 500  # se la griglia fosse sfasata, le celle piene non tornerebbero
    results = analyze()
    assert len(results) == len(list(ICONS.glob("*.png"))) > 0
    assert sheet(results).size == (LABEL + CELL * 6, CELL * len(results))
    print("SELFTEST OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        results = analyze()
        for name, _, (m, ms), (v, vs), _ in sorted(results, key=lambda r: -max(r[2][1], r[3][1])):
            flag = "  DA RIVEDERE" if ms >= LIMIT_MOD or vs >= LIMIT_VANILLA else ""
            print(f"{name:24} mod {ms:.2f} {m:24} {v} {vs:.2f}{flag}")
        (ROOT / "dist").mkdir(exist_ok=True)
        sheet(results).save(ROOT / "dist/leggibilita.png")
        print(ROOT / "dist/leggibilita.png")
        if any(r[2][1] >= LIMIT_MOD or r[3][1] >= LIMIT_VANILLA for r in results):
            sys.exit(1)
