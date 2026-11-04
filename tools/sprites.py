"""Disegna gli sprite 32x32 della mod da griglie di caratteri in stile Binding of Isaac: Repentance+
e i nomi dei boss rinominati per la schermata VS.
Standard grafici e regole visive documentati in docs/standard-grafici.md.
Uso: python3 tools/sprites.py [--selftest]
"""
import random
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

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
    "la_trollata": "resources/gfx/items/collectibles/la_trollata.png",
    "fai_cosi": "resources/gfx/items/collectibles/fai_cosi.png",
    "mannaggia_a_lui": "resources/gfx/items/trinkets/mannaggia_a_lui.png",
    "tacchinardi": "resources/gfx/items/collectibles/tacchinardi.png",
    "tacchinibus": "resources/gfx/items/collectibles/tacchinibus.png",
    "tacchino_domenica": "resources/gfx/items/collectibles/tacchino_domenica.png",
    "sono_un_idiota": "resources/gfx/items/collectibles/sono_un_idiota.png",
    "fermi_tutti": "resources/gfx/items/collectibles/fermi_tutti.png",
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

    # Lacrime
    "a": (176, 222, 245),
    "A": (96, 164, 222),
    "c": (48, 96, 160),
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
        "  ttttttttttttuu  ",
        "  ttttttttRRttsu  ",
        "  tttttttRRRttsu  ",
        "  tRRRRRttRRttsu  ",
        "  tRRRRRttRRttsu  ",
        "  ttttttttRRttsu  ",
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
    "san_gennaruzzo": [  # Reliquiario d'oro con il sangue del miracolo nella teca: non deve sembrare una pozione
        "        LY        ",
        "      LYYYYy      ",
        "        Yy        ",
        "      LYYYYy      ",
        "    LYYYYYYYYy    ",
        "   LYYwwwwwwYYy   ",
        "  LYYwWwwwwwwYYy  ",
        "  LYwWwRRRRwwwYy  ",
        "  LYwwRRRRRRwwYy  ",
        "  LYwwRRRRrrwwYy  ",
        "  LYwwRRRrrrwwYy  ",
        "  LYYwwRrrrwwYYy  ",
        "   LYYwwwwwwYYy   ",
        "    yYYYYYYYYy    ",
        "      yYYYyb      ",
        "       YYyb       ",
        "     LYYYYyyb     ",
        "    LYYYYYYyyb    ",
        "    bbbbbbbbbb    ",
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
    "la_trollata": [  # Troll bomb con occhi storti e ghigno rosso
        "             OY  ",
        "            OYWO ",
        "           ssOY  ",
        "          ss     ",
        "      mddsddn    ",
        "    mmddddddddn  ",
        "   mWmddddddddnn ",
        "  mWmdWWdddWWddnn",
        "  mmddWKdddKWddnn",
        "  mdddddddddddnnn",
        "  dddRdddddddRdnn",
        "  ddddRRRRRRRddnn",
        "  dddddRWWWRddnnn",
        "   dddddRRRdddnn ",
        "    ndddddnnnnn  ",
        "      nnnnnnn    ",
    ],
    "fai_cosi": [  # Due lacrime gemelle
        "    aA              ",
        "   aaAc             ",
        "   aAAc      aA     ",
        "  aaAAAc    aaAc    ",
        " aWaAAAAc   aAAc    ",
        " aWAAAAAc  aaAAAc   ",
        " aAAAAAAc aWaAAAAc  ",
        " aAAAAAcc aWAAAAAc  ",
        "  AAAAcc  aAAAAAAc  ",
        "   cccc   aAAAAAcc  ",
        "           AAAAcc   ",
        "            cccc    ",
    ],
    "mannaggia_a_lui": [  # Cornetto rosso con il tappo d'oro
        "            lR  ",
        "           lRr  ",
        "          lRRr  ",
        "         lRRr   ",
        "        lRRRr   ",
        "       lRRRRr   ",
        "      lWRRRr    ",
        "     lWRRRRr    ",
        "    lRRRRRr     ",
        "   lRRRRRrr     ",
        "   lRRRRrr      ",
        "  LYYYyyb       ",
        " LYYYYyb        ",
        "  YYyyb         ",
    ],
    "tacchinardi": [  # Coscia di tacchino
        "        LYYy     ",
        "      LYYYYyy    ",
        "     LYYYYYyyb   ",
        "    LYYYYYYyyb   ",
        "    YYYYYYyyyb   ",
        "    YYYYYyyybb   ",
        "    yYYYyyybb    ",
        "     yyyyybb     ",
        "      bbbbt      ",
        "        tts      ",
        "        tts      ",
        "         tts     ",
        "        tttsu    ",
        "       Wttssu    ",
        "        tsuu     ",
    ],
    "tacchinibus": [  # Piuma di tacchino
        "          lF ",
        "         lFFr",
        "        lFFFr",
        "       lOFFr ",
        "      lOOFFr ",
        "     lOOOFr  ",
        "    LOOOFFr  ",
        "    LOOFFr   ",
        "   LYOOFr    ",
        "   LYOFFr    ",
        "  LYYOFr     ",
        "  LYYFr      ",
        "  YYyr       ",
        " Yyb         ",
        " yb          ",
        "yb           ",
    ],
    "tacchino_domenica": [  # Tacchino arrosto sul piatto
        "   LL          LL   ",
        "  WLLy        WLLy  ",
        "   Lyb  LYYy   Lyb  ",
        "    yYLYYYYYYyyb    ",
        "    LYYYYYYYYyyb    ",
        "   LYYYYYYYYYyyyb   ",
        "   YYYYYYYYYYyyyb   ",
        "   YYYYYYYYYyyyyb   ",
        "   yYYYYYYYyyyybb   ",
        "    yyyyyyyyyybb    ",
        "  gggbbbbbbbbbbggm  ",
        " Wggggggggggggggggm ",
        "  gggggggggggggmmm  ",
        "    mmmmmmmmmmmm    ",
    ],
    "sono_un_idiota": [  # Cappello da asino di carta, con la fascia rossa
        "       Wt       ",
        "       tts      ",
        "      Wtts      ",
        "      ttss      ",
        "     Wttssu     ",
        "     tttssu     ",
        "    lRRRRRr     ",
        "    RRRRRrr     ",
        "   Wtttsssu     ",
        "   ttttsssuu    ",
        "  Wttttsssuu    ",
        "  tttttssssuu   ",
        " lRRRRRRRRrrr   ",
        " RRRRRRRRRrrrr  ",
        "Wtttttssssssuuu ",
        "tttttttssssssuuu",
        " ssssssssuuuuuu ",
    ],
    "fermi_tutti": [  # Cartello di stop
        "     llllll     ",
        "    lRRRRRRr    ",
        "   lRRRRRRRRr   ",
        "  lRRRRRRRRRRr  ",
        " lRRRRRRRRRRRRr ",
        "lRRRRRRRRRRRRRRr",
        "lRWWWWWWWWWWWWRr",
        "lRWWWWWWWWWWWwRr",
        "lRwwwwwwwwwwwwRr",
        "lRRRRRRRRRRRRRRr",
        "lRRRRRRRRRRRRRrr",
        " RRRRRRRRRRRRrr ",
        "  RRRRRRRRRRrr  ",
        "   RRRRRRRRrr   ",
        "    rrrrrrrr    ",
        "       uu       ",
        "       uu       ",
        "      suuu      ",
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


# Sostituiscono i PNG vanilla con lo stesso percorso: (righe, altezza delle lettere, spessore del tratto)
BOSS_NAMES = {
    "resources/gfx/ui/boss/bossname_68.0_peep.png": (["PIPPOLINS"], 28, 6),
    "resources/gfx/ui/boss/bossname_274.0_megasatan.png": (["MEGA STANLEY"], 20, 4),
    "resources/gfx/ui/boss/bossname_thebeast.png": (["IL BEASTY BOY"], 20, 4),  # il vanilla non ha questo PNG, il nome viene da bossportraits.xml
    "resources/gfx/ui/boss/bossname_bumbino.png": (["BUMBAZZO"], 28, 6),
}
BOSS_NAME_COLOR = (199, 178, 153)  # l'unico colore dei bossname vanilla
BOSS_NAME_SIZE = (256, 64)         # il ritaglio di BossName in versusscreen.anm2
BOSS_NAME_CENTER = 104             # i nomi vanilla più larghi vanno da x=0 a x=205: così MEGA STANLEY non tocca il bordo
GLYPHS = {  # tratti su una griglia alta 6
    "A": [[(0, 6), (2, 0), (4, 6)], [(1, 4), (3, 4)]],
    "B": [[(0, 0), (0, 6), (3, 6), (4, 5), (4, 4), (3, 3), (0, 3)], [(0, 0), (3, 0), (4, 1), (4, 2), (3, 3)]],
    "C": [[(4, 1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5)]],
    "D": [[(0, 0), (0, 6), (3, 6), (4, 5), (4, 1), (3, 0), (0, 0)]],
    "E":[[(4, 0), (0, 0), (0, 6), (4, 6)], [(0, 3), (3, 3)]],
    "F": [[(4, 0), (0, 0), (0, 6)], [(0, 3), (3, 3)]],
    "G": [[(4, 1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5), (4, 3), (2, 3)]],
    "I": [[(0, 0), (2, 0)], [(1, 0), (1, 6)], [(0, 6), (2, 6)]],  # con le stanghette, o si fonde con la L
    "L": [[(0, 0), (0, 6), (4, 6)]],
    "M": [[(0, 6), (0, 0), (2, 3), (4, 0), (4, 6)]],
    "N": [[(0, 6), (0, 0), (4, 6), (4, 0)]],
    "O": [[(1, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0)]],
    "P": [[(0, 6), (0, 0), (3, 0), (4, 1), (4, 2), (3, 3), (0, 3)]],
    "R": [[(0, 6), (0, 0), (3, 0), (4, 1), (4, 2), (3, 3), (0, 3)], [(2, 3), (4, 6)]],
    "S": [[(4, 1), (3, 0), (1, 0), (0, 1), (0, 2), (1, 3), (3, 3), (4, 4), (4, 5), (3, 6), (1, 6), (0, 5)]],
    "T": [[(0, 0), (4, 0)], [(2, 0), (2, 6)]],
    "U": [[(0, 0), (0, 5), (1, 6), (3, 6), (4, 5), (4, 0)]],
    "Y": [[(0, 0), (2, 3), (4, 0)], [(2, 3), (2, 6)]],
    "Z": [[(0, 0), (4, 0), (0, 6), (4, 6)]],
}


def render_boss_name(lines, height, stroke):
    ss = 4  # disegna in grande e riduce, per avere i bordi morbidi dei nomi vanilla
    u, gap = height / 6, stroke
    rng = random.Random(" ".join(lines))  # stesso testo, stessi PNG
    mask = Image.new("L", (BOSS_NAME_SIZE[0] * ss, BOSS_NAME_SIZE[1] * ss), 0)
    draw = ImageDraw.Draw(mask)
    top = (BOSS_NAME_SIZE[1] - height * len(lines) - 10 * (len(lines) - 1)) / 2
    for n, line in enumerate(lines):
        widths = [2 * u if c == " " else max(x for s in GLYPHS[c] for x, _ in s) * u for c in line]
        x = BOSS_NAME_CENTER - (sum(widths) + gap * (len(line) - 1)) / 2
        y = top + n * (height + 10)
        for c, w in zip(line, widths):
            dx, dy = rng.uniform(-0.5, 0.5), rng.uniform(-1.5, 1.5)  # lettere storte, come a mano
            for s in GLYPHS.get(c, []):
                pts = [((x + dx + px * u) * ss, (y + dy + py * u) * ss) for px, py in s]
                draw.line(pts, fill=255, width=stroke * ss, joint="curve")
                for px, py in (pts[0], pts[-1]):
                    r = stroke * ss / 2
                    draw.ellipse((px - r, py - r, px + r, py + r), fill=255)
            x += w + gap
    alpha = mask.resize(BOSS_NAME_SIZE, Image.LANCZOS).point(lambda a: 0 if a < 64 else 128 if a < 192 else 255)
    im = Image.new("RGBA", BOSS_NAME_SIZE, BOSS_NAME_COLOR + (0,))
    im.putalpha(alpha)
    return im


def write_boss_names(base):
    paths = []
    for rel, (lines, height, stroke) in BOSS_NAMES.items():
        p = Path(base) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        render_boss_name(lines, height, stroke).save(p)
        paths.append(p)
    return paths


def write_all(base):
    write_boss_names(base)
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
        for p in write_boss_names(Path(d)):
            im = Image.open(p)
            assert im.size == BOSS_NAME_SIZE and im.mode == "RGBA", (p, im.size, im.mode)
            x0, y0, x1, y1 = im.getchannel("A").getbbox()
            # x0 e y0 a 0 vorrebbero dire lettere tagliate dal bordo
            assert x0 >= 1 and x1 <= 212 and y0 >= 1 and y1 <= 63, (p, x0, y0, x1, y1)
            colors = [c for _, c in im.getcolors(65536)]
            assert {c[:3] for c in colors if c[3]} == {BOSS_NAME_COLOR}, p
            assert {c[3] for c in colors} == {0, 128, 255}, p
    print("SELFTEST OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        write_all(ROOT)
