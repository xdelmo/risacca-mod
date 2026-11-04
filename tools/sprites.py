"""Disegna gli sprite 32x32 della mod da griglie di caratteri in stile Binding of Isaac: Repentance+.
Standard grafici e regole visive documentati in docs/standard-grafici.md.
Uso: python3 tools/sprites.py [--selftest]
"""
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = {
    "ho_rotto_il_gioco": "resources/gfx/items/collectibles/ho_rotto_il_gioco.png",
    "meno_uno_dead_god": "resources/gfx/items/collectibles/meno_uno_dead_god.png",
    "win_streak": "resources/gfx/items/trinkets/win_streak.png",
    "non_vi_rubo": "resources/gfx/items/collectibles/non_vi_rubo.png",
    "potrebbe_stare_qua": "resources/gfx/items/collectibles/potrebbe_stare_qua.png",
    "san_gennaruzzo": "resources/gfx/items/collectibles/san_gennaruzzo.png",
    "te_ne_privi": "resources/gfx/items/trinkets/te_ne_privi.png",
    "mossa_pro_player": "resources/gfx/items/collectibles/mossa_pro_player.png",
}
PALETTE = {
    "K": (8, 0, 0),        # Contorno Isaac: colore del bordo in 443 collezionabili vanilla su 548
    "W": (255, 255, 255),  # Punto luce speculare

    # Plastica e metallo freddo
    "w": (236, 238, 245),
    "g": (186, 190, 202),
    "m": (132, 138, 152),
    "d": (82, 86, 100),
    "n": (50, 50, 72),

    # Glitch TMTRAINER
    "C": (50, 245, 245),
    "P": (245, 50, 210),

    # Ossa
    "t": (235, 230, 216),
    "s": (184, 178, 162),
    "u": (130, 124, 112),

    # Rosso: sangue e vernice della sveglia
    "l": (255, 95, 95),
    "R": (205, 35, 35),
    "r": (125, 20, 25),

    # Oro un po' spento, verso il rame
    "L": (250, 232, 150),
    "Y": (226, 172, 52),
    "y": (164, 108, 30),
    "b": (100, 58, 20),

    # Fiamma
    "F": (230, 48, 26),
    "O": (255, 145, 28),
}

# Solo i riempimenti: il contorno da 2px stile Isaac lo aggiunge outline().
# Le griglie restano sui 16-20px: col contorno diventano 20-24, come i vanilla.
SPRITES = {
    "ho_rotto_il_gioco": [  # Cartuccia spaccata in due, con l'etichetta glitch TMTRAINER
        "  wwwwwwwgK        ",
        " wwggggggKK gggm   ",
        " wggggggKK wggggm  ",
        " wgCCCCKK wPPPPgm  ",
        " wgCCCKK wPPPPPgm  ",
        " wgCCCCKK wPPPPgm  ",
        " wgPPPPPKK wCCCgm  ",
        " wgPPPPPPKK wCCgm  ",
        " wgPPPPPKK wCCCgm  ",
        " wgCCCCKK wPPPPgm  ",
        " wggggKK wggggggm  ",
        " wgggKK wgggggggm  ",
        " wggKK wggggggmmm  ",
        " wmmKK wmmmmmmmm   ",
        "  mKmK   mKmKmKm   ",
        "  mKmK   mKmKmKm   ",
    ],
    "meno_uno_dead_god": [  # Teschio cornuto con "-1" di sangue sulla fronte
        "tt              uu",
        "ttt            suu",
        " tts          ssu ",
        " ttss tttttt ssuu ",
        "  ttttttssssssuu  ",
        "  tsssssssRRsssu  ",
        "  tssssssRRRsssu  ",
        "  tsRRRRssRRsssu  ",
        "  tsRRRRssRRsssu  ",
        "  tsssssssRRsssu  ",
        "  tsssssssssssu   ",
        "  tsKKKKssKKKKsu  ",
        "  tsKKKKssKKKKsu  ",
        "  tssKKssssKKssu  ",
        "   tssssKKssssu   ",
        "    tssssssssu    ",
        "    tKsKsKsKsu    ",
        "    uKuKuKuKuu    ",
    ],
    "win_streak": [  # Coppa di rame con la fiamma dello streak
        "         F          ",
        "        FOF         ",
        "       FOOF   F     ",
        "      FOLOOF FOF    ",
        "      FOLLOFFOF     ",
        "   LLLLLLLLLLLLb    ",
        "YYY LYYYYYYYYYyb yyb",
        "Y   LYYYYYYYYYyb   b",
        "YY  LYYYYYYYYYyb  yb",
        " YY  LYYYYYYYyb  yb ",
        "  YYYLYYYYYYYybyyb  ",
        "      LYYYYYyb      ",
        "       YYYyb        ",
        "        Yyb         ",
        "        Yyb         ",
        "      LYYYyyb       ",
        "     LYYYYYyyb      ",
        "     bbbbbbbbb      ",
    ],
    "non_vi_rubo": [  # Sveglia rossa con due campanelle, ferma sulle 3
        "  wgg        ggm  ",
        " wggmm      ggmmm ",
        " wgmm  lRRR  gmmm ",
        "  mm lRRRRRRR  mm ",
        "    lRRRRRRRRRr   ",
        "   lRRwwwwwwwRRr  ",
        "  lRwwwwwKwwwwgRr ",
        "  lRwwwwwKwwwwgRr ",
        "  RRwwwwwKwwwwgRr ",
        "  RRwwwwwKKKKwgRr ",
        "  RRwwwwwwwwwwgRr ",
        "  RRwwwwwwwwwggRr ",
        "   RRwwgggggggRr  ",
        "    RRRRRRRRRrr   ",
        "     rrrrrrrrr    ",
        "   RRr       Rrr  ",
        "   rr         rr  ",
    ],
    "potrebbe_stare_qua": [  # Bomba con miccia corta e "?" giallo
        "             OY  ",
        "            OYWO ",
        "           ssOY  ",
        "          ss     ",
        "      mddsddn    ",
        "    mmddddddddn  ",
        "   mWmdYYYYYddnn ",
        "  mWmdYYddYYYddnn",
        "  mmddddddYYYddnn",
        "  mdddddYYYYdddnn",
        "  dddddYYYddddnnn",
        "  dddddddddddnnnn",
        "  dddddYYYdddnnnn",
        "   ddddYYYddnnnn ",
        "    ndddddnnnnn  ",
        "      nnnnnnn    ",
    ],
    "san_gennaruzzo": [  # Ampolla col sangue del miracolo e croce in cima
        "       YY       ",
        "     YYYYYy     ",
        "       Yy       ",
        "      wggg      ",
        "      wggg      ",
        "     wwgggg     ",
        "    wWwggggg    ",
        "   wWwwwggggg   ",
        "  wWwlRRRRRRgg  ",
        "  wWlRRRRRRRRrg ",
        "  wWlRRRRRRRRrg ",
        "  wwlRRRRRRRrrg ",
        "  wwRRRRRRRrrrg ",
        "   wRRRRRrrrrg  ",
        "    gggggggggg  ",
    ],
    "te_ne_privi": [  # Moneta d'oro con "?" inciso
        "     WLLLLL     ",
        "   WWLYYYYYYY   ",
        "  WLYYYYYYYYYy  ",
        " LLYYYKKKKYYYYy ",
        " LYYYKKYYKKYYYy ",
        "LYYYYKKYYKKYYYyy",
        "LYYYYYYYYKKYYYyy",
        "LYYYYYYYKKYYYYyy",
        "LYYYYYYKKYYYYYyy",
        "LYYYYYYKKYYYYyyy",
        "LYYYYYYYYYYYYyyy",
        " YYYYYYKKYYYYyy ",
        " YYYYYYKKYYyyyy ",
        "  YYYYYYYyyyyb  ",
        "   yyyyyyyybb   ",
        "     bbbbbb     ",
    ],
    "mossa_pro_player": [  # Controller grigio con la corona d'oro del pro player
        "     L   Y   y      ",
        "     LY YYY Yy      ",
        "     LYYYYYYyy      ",
        "     LYYYYYYyy      ",
        "                    ",
        "    wwggggggggmm    ",
        "  wwwggggggggggmmm  ",
        " wwggddgggggggRggmm ",
        " wgddddddggggRgRgmm ",
        " wgddddddgggggRggmm ",
        " wgggddggggggggggmm ",
        " wgggggggmmmmgggmmm ",
        " wwggggmmm  mmggmmm ",
        "  wgggmm      mggm  ",
        "   wgmm        mm   ",
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
    return outline(outline(im))  # due passate: il contorno vanilla è da 2px


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


def check_vanilla_style(im, p):
    """Soglie misurate sui PNG vanilla: colori e ingombro entro il 90° percentile, contorno da 2px."""
    x0, y0, x1, y1 = im.getchannel("A").getbbox()
    assert min(x0, y0, 32 - x1, 32 - y1) >= 2 and max(x1 - x0, y1 - y0) <= 26, (p, x0, y0, x1, y1)
    opaque = {(x, y) for y in range(32) for x in range(32) if im.getpixel((x, y))[3]}
    assert len({im.getpixel(c) for c in opaque}) <= 9, p
    near = ((1, 0), (-1, 0), (0, 1), (0, -1))
    edge = {(x, y) for x, y in opaque if any((x + a, y + b) not in opaque for a, b in near)}
    second = {(x, y) for x, y in opaque - edge if any((x + a, y + b) in edge for a, b in near)}
    dark = sum(max(im.getpixel(c)[:3]) < 40 for c in second)
    assert all(im.getpixel(c)[:3] == PALETTE["K"] for c in edge) and dark / len(second) >= 0.8, p


def selftest():
    with tempfile.TemporaryDirectory() as d:
        paths = write_all(Path(d))
        assert len(paths) == len(OUT), paths
        for p in paths:
            im = Image.open(p)
            assert im.size == (32, 32) and im.mode == "RGBA", (p, im.size, im.mode)
            assert im.getpixel((0, 0))[3] == 0, p
            px = [im.getpixel((x, y)) for y in range(32) for x in range(32)]
            assert sum(1 for c in px if c[3] > 0) >= 60, p
            assert any(c[3] > 0 and 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] < 40 for c in px), p
            check_vanilla_style(im, p)
    print("SELFTEST OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        write_all(ROOT)
