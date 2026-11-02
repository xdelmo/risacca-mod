"""Disegna gli sprite 32x32 della mod da griglie di caratteri. Uso: python3 tools/sprites.py [--selftest]"""
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = {
    "ho_rotto_il_gioco": "resources/gfx/items/collectibles/ho_rotto_il_gioco.png",
    "meno_uno_dead_god": "resources/gfx/items/collectibles/meno_uno_dead_god.png",
    "win_streak": "resources/gfx/items/trinkets/win_streak.png",
}
PALETTE = {
    "K": (20, 14, 14),      # Isaac dark outline / contorno profondo stile Isaac
    "W": (255, 255, 255),  # Punto luce puro speculare
    
    # Cartuccia retrò (Ho Rotto il Gioco)
    "w": (236, 238, 245),  # Luce plastica cartuccia
    "g": (186, 190, 202),  # Grigio cartuccia
    "m": (132, 138, 152),  # Ombra media scanalature
    "d": (82, 86, 100),    # Ombra profonda / slot superiore
    
    # Glitch TMTRAINER
    "C": (50, 245, 245),   # Ciano neon acceso
    "c": (18, 155, 185),   # Ciano profondo
    "P": (245, 50, 210),   # Magenta acceso
    "p": (165, 25, 145),   # Magenta scuro
    
    # Ossa e corna (Teschio Dead God / The Beast)
    "t": (235, 230, 216),  # Luce ossea / avorio chiaro
    "s": (184, 178, 162),  # Tonalità osso principale
    "u": (130, 124, 112),  # Ombra ossea / fessura
    "k": (76, 70, 62),     # Ombra profonda cavità
    
    # Sangue / Incisione (-1)
    "l": (255, 95, 95),    # Riflesso rosso sangue acceso
    "R": (225, 35, 35),    # Rosso sangue vermiglio
    "r": (135, 20, 25),    # Sangue scuro / ombra incisione
    
    # Oro e metallo (Win Streak / Etichetta e pin cartuccia)
    "L": (255, 246, 160),  # Oro chiaro speculare
    "Y": (246, 198, 42),   # Oro brillante
    "y": (180, 126, 24),   # Oro caldo in ombra
    "b": (116, 72, 16),    # Bronzo antico / sottosquadro
    
    # Fiamma sacra dello streak
    "F": (230, 48, 26),    # Fiamma rossa esterna
    "O": (255, 145, 28),   # Fiamma arancione viva
}

# Solo i riempimenti: il contorno nero stile Isaac lo aggiunge outline().
SPRITES = {
    "ho_rotto_il_gioco": [  # Cartuccia di gioco retrò spaccata con pixel glitch TMTRAINER
        "   d m d m d      CC    ",
        "  wddmddmddd    CCCCc   ",
        "  wggggggggm     CCc    ",
        "  wg wKww gg    P       ",
        "  wg  wK   m   PPp      ",
        "  wg YYYYY m   Ppp      ",
        "  wg YRRYY m            ",
        "  wg YRRYY m    CC      ",
        "  wg YYYYY m    CCc     ",
        "  wg mmmm  m     c      ",
        "  wg  K    m            ",
        "  wggm K g m            ",
        "  wggm  K  m            ",
        "  wggmm  K mm   PP      ",
        "  wggggm  K g   PPp     ",
        "  wddddd  Kdd    p      ",
        "   YY YY   YY           ",
        "   yy yy   yy           ",
    ],
    "meno_uno_dead_god": [  # Teschio cornuto del Dead God / Beast con "-1" inciso a sangue
        "  s              s  ",
        " tss            sst ",
        " tss            sst ",
        "  tsu          ust  ",
        "  tsu  tttttt  ust  ",
        "   tsutsssssstust   ",
        "   tssurlllru rRssu ",
        "    ssulRRRruurlRsu ",
        "    ssurrrrru  rRsu ",
        "    ssuuuuuuu  rRsu ",
        "    ssuuuuuuu rRRsu ",
        "   tssKKssKKsssssu  ",
        "   tsKKKssKKKssssu  ",
        "   tssKKssKKsssssu  ",
        "    ssssKKsssssu    ",
        "    tsstttsssstu    ",
        "    susususususu    ",
        "     k u k u k      ",
    ],
    "win_streak": [  # Calice d'oro cesellato con manici sinuosi e fiamma dello streak ardente
        "         F          ",
        "        FFF         ",
        "        FOF         ",
        "       FOOOF        ",
        "       FOLOF   FF   ",
        "      FOLLLOF FOF   ",
        "      FOLLWLOFOF    ",
        "       FOWLLOFO     ",
        "  LLLLLLOFFFOLLLLb  ",
        " LWWWWWWLLLLLLLLLYb ",
        "YY LWWYYYYYYYYYyY YY",
        "Yb LWWYYYYYYYYYyY by",
        "Yb  YYYYYYYYYYYyY by",
        " Yb  YYYYYYYYYyY  y ",
        "  y   YYYYYYYyY  y  ",
        "       YYYYyYy      ",
        "        YyYyb       ",
        "        YyYyb       ",
        "       LYYYYyb      ",
        "      LYYYYYYyb     ",
        "     LYYYYYYYYyb    ",
        "    LYYYYYYYYYYyb   ",
        "    bbbyyyyyybbbb   ",
    ],
}


def render(rows):
    w = max(len(r) for r in rows)
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    ox, oy = (32 - w) // 2, (32 - len(rows)) // 2
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != " ":
                im.putpixel((ox + x, oy + y), PALETTE[ch] + (255,))
    return outline(im)


def outline(im):
    out = im.copy()
    for y in range(32):
        for x in range(32):
            if im.getpixel((x, y))[3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < 32 and 0 <= ny < 32 and im.getpixel((nx, ny))[3]:
                    out.putpixel((x, y), PALETTE["K"] + (255,))
                    break
    return out


def write_all(base):
    paths, imgs = [], []
    for name, rel in OUT.items():
        im = render(SPRITES[name])
        p = Path(base) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        im.save(p)
        paths.append(p)
        imgs.append(im)
    prev = Image.new("RGBA", (len(imgs) * 288 + 32, 320), (58, 44, 40, 255))
    for i, im in enumerate(imgs):
        big = im.resize((256, 256), Image.NEAREST)
        prev.alpha_composite(big, (32 + i * 288, 32))
    (Path(base) / "docs").mkdir(exist_ok=True)
    prev.save(Path(base) / "docs/preview.png")
    return paths


def selftest():
    with tempfile.TemporaryDirectory() as d:
        paths = write_all(Path(d))
        assert len(paths) == 3, paths
        for p in paths:
            im = Image.open(p)
            assert im.size == (32, 32) and im.mode == "RGBA", (p, im.size, im.mode)
            assert im.getpixel((0, 0))[3] == 0, p
            px = [im.getpixel((x, y)) for y in range(32) for x in range(32)]
            assert sum(1 for c in px if c[3] > 0) >= 60, p
            assert any(c[3] > 0 and 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] < 40 for c in px), p
    print("SELFTEST OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        write_all(ROOT)
