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
    "K": (20, 14, 14), "g": (196, 196, 204), "D": (70, 70, 84), "R": (214, 40, 40),
    "B": (52, 108, 222), "Y": (240, 196, 48), "y": (176, 128, 30), "L": (255, 244, 150),
    "P": (236, 60, 220), "C": (60, 236, 236), "s": (150, 150, 158), "d": (96, 96, 106),
    "G": (64, 150, 56), "F": (230, 70, 30), "O": (255, 150, 30), "W": (255, 255, 255),
}

# Solo i riempimenti: il contorno nero stile Isaac lo aggiunge outline().
SPRITES = {
    "ho_rotto_il_gioco": [  # joypad crepato con pixel glitch
        "   C                PP  ",
        "  CC                PPP ",
        "  ggggggggggKggggggggg  ",
        " gggggggggggKgggggRRggg ",
        "ggggDggggggKggggggRRgggg",
        "ggggDggggggKggggYYggBBgg",
        "ggDDDDDgggggKgggYYggBBgg",
        "ggggDggggggggKggggGGgggg",
        "ggggDgggggggKgggggGGgggg",
        "gggggggggggKgggggggggggg",
        "gggggggggggKgggggggggggg",
        "gggggggg        gggggggg",
        " gggggg          gggggg ",
        " CCggg            gggPP ",
        " CC    CC             P ",
    ],
    "meno_uno_dead_god": [  # lapide con "-1"
        "      ssssss      ",
        "    sWssssssss    ",
        "   sWssssssssss   ",
        "  sWssssssssssss  ",
        "  sssssssssRRsss  ",
        "  ssssssssRRRsss  ",
        "  sssssssRRRRsss  ",
        "  ssRRRRssRRRsss  ",
        "  ssRRRRssRRRsss  ",
        "  ssssssssRRRsss  ",
        "  ssssssssRRRsss  ",
        "  sssssssRRRRRss  ",
        "  ssssssssssssss  ",
        "  sdssssssssssds  ",
        "  ssssssssssssss  ",
        "  ssssssssssssds  ",
        " dddddddddddddddd ",
        "GGGGGGGGGGGGGGGGGG",
        "GGGGGGGGGGGGGGGGGG",
    ],
    "win_streak": [  # coppa con fiammella
        "        F         ",
        "       FF         ",
        "       FOF        ",
        "      FOLOF       ",
        "      FOLLOF      ",
        "       FLLF       ",
        "  YYYYYYYYYYYYYY  ",
        "YY YWYYYYYYYYyY YY",
        "Y  YWYYYYYYYYyY  Y",
        "Y  YWYYYYYYYYyY  Y",
        " Y YYYYYYYYYYyY Y ",
        "  YYYYYYYYYYYyYY  ",
        "    YYYYYYYYyY    ",
        "      YYYYyY      ",
        "        Yy        ",
        "        Yy        ",
        "       yYYy       ",
        "     yyyyyyyy     ",
        "     yyyyyyyy     ",
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
