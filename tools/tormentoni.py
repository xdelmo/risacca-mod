"""Conta i tormentoni di docs/trascrizioni/tormentoni.txt in tutte le trascrizioni
e rigenera docs/trascrizioni/tormentoni.md.
Uso: python3 tools/tormentoni.py | --selftest"""
import re
import sys
from pathlib import Path

DIR = Path("docs/trascrizioni")
STATI = ["nella mod", "proposto", "scartato", "non usato"]


def parse(text):
    rows = []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        stato, frase, regex, nota = [p.strip() for p in (line + " |").split("|")[:4]]
        assert stato in STATI, f"stato sconosciuto: {line}"
        rows.append((stato, frase, re.compile(regex, re.I), nota))
    return rows


def count(rx, texts):
    hits = {vid: len(rx.findall(t)) for vid, t in texts.items()}
    hits = {v: n for v, n in hits.items() if n}
    if not hits:
        return 0, 0, ""
    best = max(hits, key=hits.get)
    t = texts[best]
    m = rx.search(t)
    quote = " ".join(t[max(0, m.start() - 60):m.end() + 60].split()).replace("|", "/")
    return sum(hits.values()), len(hits), f"`{best}`: …{quote}…"


def render(rows, texts):
    out = ["# Tormentoni", "",
           "Generato da `tools/tormentoni.py` partendo da [`tormentoni.txt`](tormentoni.txt): "
           "non modificarlo a mano. Per aggiungere una frase o cambiarne lo stato modifica "
           "`tormentoni.txt` e rilancia lo script dalla root della repo.", "",
           f"Conteggi su {len(texts)} trascrizioni. Sono ricerche nel testo dei sottotitoli automatici, "
           "quindi approssimative: contano anche gli usi non da tormentone. "
           "La citazione viene dal video in cui la frase compare più volte.", ""]
    for stato in STATI:
        sel = [r for r in rows if r[0] == stato]
        if not sel:
            continue
        out += [f"## {stato.capitalize()}", "", "| Frase | Volte | Video | Nota | Citazione |", "|---|---|---|---|---|"]
        stats = [(r, *count(r[2], texts)) for r in sel]
        for (_, frase, _, nota), n, v, q in sorted(stats, key=lambda s: -s[1]):
            out.append(f"| {frase} | {n} | {v} | {nota} | {q} |")
        out.append("")
    return "\n".join(out)


def selftest():
    rows = parse("# c\nproposto | Ciao | ciao\nnella mod | Bu | \\bbu\\b | nota\n")
    md = render(rows, {"a": "Ciao ciao bu", "b": "ciao bue"})
    assert "| Ciao | 3 | 2 |  | `a`: …Ciao ciao bu… |" in md, md
    assert "| Bu | 1 | 1 | nota |" in md, md
    assert md.index("## Nella mod") < md.index("## Proposto")
    print("OK")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        selftest()
    else:
        texts = {p.stem: p.read_text(encoding="utf-8") for p in sorted(DIR.glob("*.txt")) if p.name != "tormentoni.txt"}
        md = render(parse((DIR / "tormentoni.txt").read_text(encoding="utf-8")), texts)
        (DIR / "tormentoni.md").write_text(md + "\n", encoding="utf-8")
        print(f"{DIR / 'tormentoni.md'}: {len(texts)} trascrizioni")
