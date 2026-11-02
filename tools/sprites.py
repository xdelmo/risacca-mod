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
    "K": (20, 14, 14),      # Contorno scuro e crepe profonde stile Isaac
    "W": (255, 255, 255),  # Punto luce puro speculare
    
    # Joypad (plastica e pulsanti)
    "w": (236, 238, 244),  # Luce calda plastica scocca
    "g": (188, 192, 202),  # Grigio principale controller
    "m": (138, 142, 156),  # Ombra media controller
    "d": (88, 92, 106),    # Ombra profonda / impugnature inferiori
    "D": (54, 56, 68),     # D-pad ardesia scuro
    "R": (224, 40, 40),    # Tasto rosso / fiamma
    "Y": (246, 200, 45),   # Tasto giallo / oro principale
    "B": (48, 115, 232),   # Tasto blu
    "G": (45, 185, 60),    # Tasto verde
    
    # Glitch TMTRAINER
    "C": (50, 245, 245),   # Ciano neon acceso
    "c": (18, 155, 185),   # Ciano profondo
    "P": (245, 50, 210),   # Magenta acceso
    "p": (165, 25, 145),   # Magenta scuro
    
    # Lapide Meno Uno Dead God (pietra, crepe, muschio e terra)
    "t": (216, 220, 224),  # Bordo luce pietra
    "s": (160, 164, 174),  # Pietra grigia
    "u": (114, 118, 130),  # Pietra ombreggiata / rilievo interno
    "k": (72, 75, 86),     # Crepa roccia scura
    "r": (142, 22, 32),    # Rosso scuro incisione incassata
    "l": (255, 95, 95),    # Rosso vivo riflesso incisione
    "e": (110, 76, 52),    # Terra media
    "E": (70, 46, 32),     # Terra scura
    "M": (68, 150, 50),    # Muschio chiaro
    "v": (36, 88, 30),     # Muschio d'ombra
    
    # Coppa Win Streak (metallo dorato e fuoco)
    "L": (255, 244, 150),  # Oro chiaro / highlight fiamma
    "y": (180, 128, 26),   # Oro caldo in ombra
    "b": (118, 74, 16),    # Bronzo profondo / sottosquadro
    "F": (230, 48, 26),    # Fiamma rossa esterna
    "O": (255, 145, 28),   # Fiamma arancione viva
}

# Solo i riempimenti: il contorno nero stile Isaac lo aggiunge outline().
SPRITES = {
    "ho_rotto_il_gioco": [  # Joypad bombato crepato con frammenti glitch TMTRAINER
        "      dd       CC         ",
        "   CC dd   PP  CCc        ",
        "  CCc dd   PP             ",
        "  wwwwddwwwwKwwwwwwww     ",
        " wwwwwwwwwwKwwwwwwRRw     ",
        "wwwwDwwwwwwwKwwwwRRRww    ",
        "wwwDDDDwwwwwwKwwYYwBBww   ",
        "wwwDDDDDwwwwKkwwYYwBBww P ",
        "wwwwDwwwwwwKKwwwwGGwGwwPp ",
        "wwwgDggggggKkggggGGgGgwPp ",
        "ggggggggggmKkgggggggggw   ",
        "gggggggggmmKKmggggggggg   ",
        " ggggggmdd   mmdmggggg    ",
        "  ggggmd       mmdggg     ",
        "   dmd     CC    mdd      ",
        "           CCc            ",
        "            c             ",
    ],
    "meno_uno_dead_god": [  # Lapide gotica con "-1" scolpito in bassorilievo rosso sangue
        "       ttsstt         ",
        "     ttsssssstt       ",
        "    tsssssssssst      ",
        "   ttskkssssssstt     ",
        "   tssksssssssssu     ",
        "  tsskssssssssssu     ",
        "  tsskkkkkkkkkkssu    ",
        "  tskuuuuuuuuuussu    ",
        "  tskurlllru  rRRrus  ",
        "  tskulRRRru rllRRus  ",
        "  tskurrrrru  rRRrus  ",
        "  tskuuuuuuu  rRRrus  ",
        "  tskuuuuuuu  rRRrus  ",
        "  tskuuuuuuu rRRRRus  ",
        "  tskuuuuuuuuuussu    ",
        "  tssutttttttttssu    ",
        "  usskuussksuusssku   ",
        "  usssuuussuuusssku   ",
        "  vMkkMvkkkMMvkvkk    ",
        " vMMvMMMEeEEMMMvMMv   ",
        " EEEEEeeEEeeEEEEEEE   ",
    ],
    "win_streak": [  # Coppa d'oro cesellata con manici sinuosi e fiamma dello streak viva
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
