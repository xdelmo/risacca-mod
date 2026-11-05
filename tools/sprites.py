"""Disegna gli sprite 32x32 della mod da griglie di caratteri in stile Binding of Isaac: Repentance+
e i nomi dei boss rinominati per la schermata VS.
Standard grafici e regole visive documentati in docs/standard-grafici.md.
Uso: python3 tools/sprites.py [--selftest]
"""
import math
import random
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

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
    "la_trollata": [  # Detonatore a stantuffo con occhi storti e ghigno rosso: le bombe compaiono sui nemici
        "   LYYYYYYYYYYy   ",
        "   YYYYYYYYYYyy   ",
        "        md        ",
        "        md        ",
        "        md        ",
        "        md        ",
        "        md        ",
        "        md        ",
        " Wmmmmmmmmmmmmmmd ",
        "mmddddddddddddddnn",
        "mdddWWddddddWWddnn",
        "mdddWKddddddKWddnn",
        "mddddddddddddddnnn",
        "mddRddddddddddRdnn",
        "mdddRRRRRRRRRRddnn",
        "mddddRWWWWWWRdddnn",
        "ddddddRRRRRRddnnnn",
        " nnnnnnnnnnnnnnnn ",
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


# Costume della trasformazione Tacchino, a coordinate del foglio testa vanilla (32x32): (x, y, righe)
COSTUME_DIR = "resources/gfx/characters"
CRESTA = ["  l  l  ", " lR lRr ", " lRlRRr ", " RRRRRr ", "  RRrr  "]
BARGIGLI = [" Rr ", "lRRr", "lRRr", " rr "]
COSTUME_PARTS = {
    "HeadDown": [(12, 2, CRESTA), (12, 17, [" LYYYYy ", "  YYYy  ", "   yy   "]), (14, 21, BARGIGLI)],
    "HeadRight": [(10, 2, CRESTA), (23, 17, ["LYYYYy", "YYYYy ", "yyy   "]), (22, 21, BARGIGLI)],
    "HeadUp": [(12, 2, CRESTA)],
}
# Posizione della testa nell'anm2, come nei costumi vanilla: da qui si corregge l'allineamento
COSTUME_PIVOT = (16, 28)
COSTUME_Y = -5
ANM2_TINT = 'AlphaTint="255" BlueOffset="0" BlueTint="255" GreenOffset="0" GreenTint="255" Interpolated="false" RedOffset="0" RedTint="255" Rotation="0" Visible="true" XScale="100" YScale="100"'


# Cappello da asino di Sono un Idiota: stesso disegno in ogni direzione. Più alto della cresta, quindi più in alto nell'anm2
CONO = [
    "     Wt     ",
    "     ts     ",
    "    Wtsu    ",
    "    ttsu    ",
    "   lRRRrr   ",
    "   RRRrrr   ",
    "   Wttssu   ",
    "  Wtttssuu  ",
    "  ttttssuu  ",
    "  ttttsssu  ",
    " lRRRRRrrrr ",
    " RRRRRRrrrr ",
    "Wtttttsssuuu",
    "ssssssuuuuuu",
]
CONO_PARTS = {name: [(10, 1, CONO)] for name in ("HeadDown", "HeadRight", "HeadUp")}
CONO_Y = -11


def render_costume_frame(parts):
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    for ox, oy, rows in parts:
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != " ":
                    im.putpixel((ox + x, oy + y), PALETTE[ch] + (255,))
    return outline(im)  # una passata sola: due coprirebbero la faccia


def write_costume(base, name="tacchino", parts=COSTUME_PARTS, offset_y=COSTUME_Y):
    right = render_costume_frame(parts["HeadRight"])
    frames = {
        "HeadDown": render_costume_frame(parts["HeadDown"]),
        "HeadRight": right,
        "HeadUp": render_costume_frame(parts["HeadUp"]),
        "HeadLeft": right.transpose(Image.FLIP_LEFT_RIGHT),
    }
    sheet = Image.new("RGBA", (32 * len(frames), 32), (0, 0, 0, 0))
    anims = []
    for i, (anim, frame) in enumerate(frames.items()):
        sheet.paste(frame, (32 * i, 0))
        # 4 tick come la testa vanilla: il costume resta uguale anche mentre si spara
        anims.append(
            f'    <Animation FrameNum="4" Loop="false" Name="{anim}">\n'
            f'      <RootAnimation><Frame {ANM2_TINT} Delay="4" XPosition="0" YPosition="0"/></RootAnimation>\n'
            f'      <LayerAnimations><LayerAnimation LayerId="0" Visible="true">\n'
            f'        <Frame {ANM2_TINT} Delay="4" Width="32" Height="32" XCrop="{32 * i}" YCrop="0" '
            f'XPivot="{COSTUME_PIVOT[0]}" YPivot="{COSTUME_PIVOT[1]}" XPosition="0" YPosition="{offset_y}"/>\n'
            f"      </LayerAnimation></LayerAnimations>\n"
            f"      <NullAnimations/>\n      <Triggers/>\n    </Animation>\n"
        )
    anm2 = (
        '<AnimatedActor>\n  <Info CreatedBy="tools/sprites.py" CreatedOn="" Fps="30" Version="1"/>\n  <Content>\n'
        f'    <Spritesheets><Spritesheet Id="0" Path="{name}.png"/></Spritesheets>\n'
        '    <Layers><Layer Id="0" Name="head0" SpritesheetId="0"/></Layers>\n'
        '    <Nulls/>\n    <Events/>\n  </Content>\n  <Animations DefaultAnimation="HeadDown">\n'
        + "".join(anims) + "  </Animations>\n</AnimatedActor>\n"
    )
    d = Path(base) / COSTUME_DIR
    d.mkdir(parents=True, exist_ok=True)
    sheet.save(d / f"{name}.png")
    (d / f"{name}.anm2").write_text(anm2, encoding="utf-8")
    return d / f"{name}.png", d / f"{name}.anm2"


# Sostituiscono i PNG vanilla con lo stesso percorso: (righe, altezza delle lettere, spessore del tratto, distanza tra le lettere in tratti)
BOSS_NAMES = {
    "resources/gfx/ui/boss/bossname_68.0_peep.png": (["PIPPOLINS"], 27, 6, 1),
    "resources/gfx/ui/boss/bossname_274.0_megasatan.png": (["MEGA STANLEY"], 23, 5.2, 0.5),
    "resources/gfx/ui/boss/bossname_thebeast.png": (["IL BEASTY BOY"], 23, 5.2, 0.55),  # il vanilla non ha questo PNG, il nome viene da bossportraits.xml
    "resources/gfx/ui/boss/bossname_bumbino.png": (["BUMBAZZO"], 27, 5.6, 1),
}
BOSS_NAME_COLOR = (199, 178, 153)  # l'unico colore dei bossname vanilla
BOSS_NAME_SIZE = (256, 64)         # il ritaglio di BossName in versusscreen.anm2
BOSS_NAME_CENTER = (96, 30)        # la mediana dei nomi vanilla
# Pennellate su una griglia alta 6: si stringono verso la fine, quindi conta il verso. Più di due punti = curva.
GLYPHS = {
    "A": [[(1.7, 0), (0, 6.2)], [(1.6, 0), (3.5, 6)], [(0.5, 4), (3, 3.8)]],
    "B": [[(0.2, 0), (0, 6)], [(0, 0.1), (2.6, 0), (3.1, 1.3), (2.4, 2.6), (0.4, 3)], [(0.4, 3), (2.8, 3.1), (3.4, 4.6), (2.4, 5.8), (0, 6)]],
    "C": [[(3.2, 0.7), (2.4, 0), (0.8, 0.3), (0, 2.8), (0.8, 5.6), (2.4, 6), (3.3, 5.2)]],
    "D": [[(0.2, 0), (0, 6)], [(0, 0.1), (2.2, 0.2), (3.5, 2.4), (3, 5), (0, 6)]],
    "E": [[(0.1, 0), (0, 6)], [(0, 0.1), (3, 0)], [(0, 2.9), (2.4, 2.8)], [(0, 6), (3.2, 5.8)]],
    "F": [[(0.1, 0), (0, 6.3)], [(0, 0.1), (3.1, 0)], [(0, 3), (2.4, 2.8)]],
    "G": [[(3.3, 0.8), (2.4, 0), (0.8, 0.3), (0, 2.9), (0.8, 5.6), (2.4, 6), (3.5, 4.8), (3.4, 3.4)], [(3.5, 3.3), (1.9, 3.3)]],
    "I": [[(0.8, 0), (0.6, 6.2)]],
    "L": [[(0.1, 0), (0, 6)], [(0, 6), (3.2, 5.7)]],
    "M": [[(0.4, 0), (0, 6.2)], [(0.4, 0), (2.1, 4)], [(3.9, 0), (2, 4)], [(3.9, 0), (4.3, 6.2)]],
    "N": [[(0.2, 0), (0, 6.2)], [(0.2, 0), (3.6, 6)], [(3.8, 0), (3.6, 6.1)]],
    "O": [[(1.8, 0), (0.5, 0.6), (0, 3), (0.7, 5.5), (1.9, 6), (3.2, 5.2), (3.6, 2.8), (2.9, 0.6), (1.4, 0.1)]],
    "P": [[(0.2, 0), (0, 6.4)], [(0, 0.1), (2.6, 0), (3.3, 1.4), (2.4, 3), (0.2, 3.5)]],
    "R": [[(0.2, 0), (0, 6.3)], [(0, 0.1), (2.6, 0), (3.2, 1.4), (2.3, 2.8), (0.2, 3.3)], [(1.1, 3.1), (3.4, 6.2)]],
    "S": [[(3.1, 0.7), (2.2, 0), (0.7, 0.4), (0.3, 1.8), (1.7, 3), (3.1, 4), (2.8, 5.5), (1.2, 6), (0, 5.2)]],
    "T": [[(0, 0.2), (3.8, 0)], [(1.9, 0), (1.7, 6.3)]],
    "U": [[(0.1, 0), (0, 3.8), (0.7, 5.6), (1.9, 6), (3, 5.3), (3.3, 3.4)], [(3.3, 0), (3.4, 6.1)]],
    "Y": [[(0, 0), (1.7, 3)], [(3.5, 0), (1.5, 3.4), (1.3, 6.3)]],
    "Z": [[(0, 0.2), (3.2, 0)], [(3.2, 0), (0, 5.9)], [(0, 5.9), (3.4, 5.7)]],
}


def brush_stroke(draw, pts, width, rng, ss):
    """Timbra cerchi lungo il tratto: pieno all'inizio, sottile in fondo, con lo spessore che oscilla."""
    pts = [(x * ss, y * ss) for x, y in pts]
    for _ in range(2 if len(pts) > 2 else 0):  # arrotonda le curve tagliando gli angoli
        cut = [(0.75 * a + 0.25 * c, 0.75 * b + 0.25 * d) for (a, b), (c, d) in zip(pts, pts[1:])]
        cut2 = [(0.25 * a + 0.75 * c, 0.25 * b + 0.75 * d) for (a, b), (c, d) in zip(pts, pts[1:])]
        pts = [pts[0]] + [p for pair in zip(cut, cut2) for p in pair] + [pts[-1]]
    lengths = [((c - a) ** 2 + (d - b) ** 2) ** 0.5 for (a, b), (c, d) in zip(pts, pts[1:])]
    total, done = sum(lengths), 0
    phase, waves = rng.uniform(0, 6.28), rng.uniform(1.5, 3)
    for (a, b), (c, d), length in zip(pts, pts[1:], lengths):
        for i in range(max(1, int(length))):
            t = (done + i) / total
            r = width * ss / 2 * min(1, 0.72 + t * 2.5) * (1 - 0.55 * max(0, t - 0.7) / 0.3) * (1 + 0.1 * math.sin(phase + t * waves * 6.28))
            x, y = a + (c - a) * i / length, b + (d - b) * i / length
            draw.ellipse((x - r, y - r, x + r, y + r), fill=255)
        done += length


def render_boss_name(lines, height, stroke, spacing):
    ss = 4  # disegna in grande e riduce: il bordo a 128 dei nomi vanilla viene da qui
    u = height / 6
    rng = random.Random(" ".join(lines))  # stesso testo, stessi PNG
    w, h = BOSS_NAME_SIZE
    mask = Image.new("L", (2 * w * ss, 2 * h * ss), 0)
    draw = ImageDraw.Draw(mask)
    for n, line in enumerate(lines):
        x, base = 16.0, h + height / 2 + n * (height + 6)
        first = True
        for c in line:
            if c == " ":
                x += 1.4 * u
                first = True
                continue
            scale = 1.18 if first else rng.uniform(0.94, 1.04)  # l'iniziale è più grande, le altre ballano
            tilt, dy = rng.uniform(-0.07, 0.07), rng.uniform(-1, 1)
            for s in GLYPHS[c]:
                pts = []
                for px, py in s:
                    px, py = (px + rng.uniform(-0.1, 0.1)) * u * scale, (py - 6 + rng.uniform(-0.1, 0.1)) * u * scale
                    pts.append((x + px - py * tilt, base + dy + py + px * tilt))
                brush_stroke(draw, pts, stroke, rng, ss)
            x += max(px for st in GLYPHS[c] for px, _ in st) * u * scale + stroke * spacing
            if c == "I":
                x += 0.5 * u  # un tratto dritto accanto a un altro si fonde: IL e IN diventerebbero una macchia
            first = False
    alpha = mask.resize((2 * w, 2 * h), Image.BOX).point(lambda a: 0 if a < 90 else 128 if a < 165 else 255)
    x0, y0, x1, y1 = alpha.getbbox()
    im = Image.new("RGBA", BOSS_NAME_SIZE, BOSS_NAME_COLOR + (0,))
    a = Image.new("L", BOSS_NAME_SIZE, 0)
    a.paste(alpha.crop((x0, y0, x1, y1)), (BOSS_NAME_CENTER[0] - (x1 - x0) // 2, BOSS_NAME_CENTER[1] - (y1 - y0) // 2))
    im.putalpha(a)
    return im


def boss_name_metrics(im):
    """Larghezza, altezza, centro x, spessore medio del tratto e quota di pixel semitrasparenti."""
    alpha = im.getchannel("A")
    solid = alpha.point(lambda v: 255 if v >= 128 else 0)
    x0, y0, x1, y1 = solid.getbbox()
    area = solid.histogram()[255]
    edge = area - solid.filter(ImageFilter.MinFilter(3)).histogram()[255]
    return x1 - x0, y1 - y0, (x0 + x1) / 2, 2 * area / edge, alpha.histogram()[128] / area


def write_boss_names(base):
    paths = []
    for rel, spec in BOSS_NAMES.items():
        p = Path(base) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        render_boss_name(*spec).save(p)
        paths.append(p)
    return paths


def write_all(base):
    write_boss_names(base)
    write_costume(base)
    write_costume(base, "cono", CONO_PARTS, CONO_Y)
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
            assert x0 >= 1 and y0 >= 1 and y1 <= 63, (p, x0, y0, x1, y1)
            # Soglie misurate sui PNG vanilla, tranne la larghezza: il vanilla arriva a 205, ma così il nome non tocca il bordo
            width, tall, center, thick, semi = boss_name_metrics(im)
            assert width <= 190 and 25 <= tall <= 56 and 84.5 <= center <= 104, (p, width, tall, center)
            assert 4.2 <= thick <= 6.9 and 0.07 <= semi <= 0.12, (p, thick, semi)
            colors = [c for _, c in im.getcolors(65536)]
            assert {c[:3] for c in colors if c[3]} == {BOSS_NAME_COLOR}, p
            assert {c[3] for c in colors} == {0, 128, 255}, p
        for png, anm2 in (write_costume(Path(d)), write_costume(Path(d), "cono", CONO_PARTS, CONO_Y)):
            sheet = Image.open(png)
            assert sheet.size == (128, 32) and sheet.mode == "RGBA", sheet.size
            for i in range(4):
                assert sheet.crop((32 * i, 0, 32 * i + 32, 32)).getchannel("A").getbbox(), i
            root = ET.parse(anm2).getroot()
            assert sorted(a.get("Name") for a in root.iter("Animation")) == ["HeadDown", "HeadLeft", "HeadRight", "HeadUp"]
            assert root.find(".//Spritesheet").get("Path") == png.name, anm2
    print("SELFTEST OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    else:
        write_all(ROOT)
