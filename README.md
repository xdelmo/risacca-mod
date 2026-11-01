# Risacca Mod

Mod per **The Binding of Isaac: Repentance** dedicata a [Risacca](https://www.youtube.com/@Risaacca), che ogni giorno carica una run di Repentance.

![preview](docs/preview.png)

## Cosa fa

### Scritte a schermo

| Quando | Scritta |
|---|---|
| Inizio di una nuova run | *Ciao a tutti, io sono Risacca*, poi *Benvenuti sul mio canale* |
| Ogni nuovo piano | *È XL?*, poi *SÌ, È XL!* oppure *No... non è XL* |
| Oggetto di qualità 3 / 4 | *IL GODOR!* / *GODOR MAXIMOR!* |
| Oggetto preso con un patto col diavolo | *Alla facciazza vostra!* |
| Colpo da un cuore intero | *Tacchino!* |
| Resti a mezzo cuore | *C'ho l'ansia* |
| Compare The Beast / Mega Satan | *IL BEASTY BOY* / *MEGA STANLEY KUBRICK* |
| Boss finale sconfitto | *Un bacione grande*, poi *dal vostro Risacca* |
| Morte | *Calmati tacchinardo* |

### Oggetti nuovi

- **Ho Rotto il Gioco** (attivo, 6 cariche): fa comparire un oggetto glitchato, come con TMTRAINER.
- **-1 al Dead God** (passivo): ogni boss sconfitto dà +0.2 danno, +0.03 velocità, +4 gittata e un tiro un po' più rapido. Il bonus arriva al massimo a 10 boss.
- **Win Streak** (trinket): dà +0.5 danno per ogni piano finito senza essere colpiti. Basta un colpo per azzerare la serie.

### Nomi alla Risacca

Gli oggetti originali del gioco vengono rinominati nei nomi e nelle descrizioni:

| Originale | Diventa |
|---|---|
| key / keys | Chiaviz-Chiavoz |
| bomb / bombs | Bombiz-Bomboz |
| boss / bosses | Beppe Bossicchio |
| Mega Satan | Mega Stanley Kubrick |
| Bumbo | Bumbazzo |
| Greed | Ballerino di Flamenco |
| Incubus | Il buddy più forte del gioco |

## Installazione

1. Iscriviti alla mod dallo Steam Workshop. In alternativa, estrai `risacca-mod.zip` dentro `...\steamapps\common\The Binding of Isaac Rebirth\mods\`.
2. Attivala dal menu **Mods** del gioco.

Serve Repentance. La mod non ha bisogno di REPENTOGON né di altre mod.

## Sviluppo

Servono Lua (il codice è compatibile con 5.3) e Python 3 con Pillow. Lancia i comandi dalla root della repo:

```bash
lua tests/test_logic.lua   # test della logica
lua tests/smoke.lua        # test di main.lua con un'API Isaac finta
python3 tools/build.py     # crea dist/risacca-mod.zip
```

Per rigenerare le rinomine:
1. Estrai `items.xml`, `pocketitems.xml` e `stringtable.sta` con il ResourceExtractor del gioco.
2. Mettili in `extracted/`.
3. Lancia `python3 tools/rename.py extracted`.

I dettagli sull'architettura sono in [CLAUDE.md](CLAUDE.md).

---

*Un bacione grande dal vostro Risacca.*
