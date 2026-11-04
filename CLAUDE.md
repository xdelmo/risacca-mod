# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Mod per The Binding of Isaac: Repentance dedicata allo YouTuber Risacca, provata su Repentance+. È un regalo da pubblicare sullo Steam Workshop. Comunica con l'utente in italiano. Il codice si scrive su macOS o sul PC Windows, dove la repo è anche la cartella della mod (`...\The Binding of Isaac Rebirth\mods\risacca-mod\`). Le prove in gioco le fa l'utente, e quelle ancora da fare sono in `docs/da-fare-su-windows.md`.

Il design è in `docs/superpowers/specs/2026-11-01-risacca-mod-design.md`, il piano in `docs/superpowers/plans/2026-11-01-risacca-mod.md`. I tormentoni vengono dalle trascrizioni dei video in `docs/trascrizioni/`.

## Comandi

Lancia tutto dalla root della repo: i path in `dofile`/`include` sono relativi.

```bash
luac -p main.lua logic.lua            # controllo sintassi
lua tests/test_logic.lua              # unit test della logica pura → "OK"
lua tests/smoke.lua                   # main.lua con un'API Isaac finta → "SMOKE OK"
python3 tools/rename.py --selftest    # rinomine degli oggetti vanilla
python3 tools/sprites.py --selftest   # sprite (serve Pillow)
python3 tools/build.py --selftest     # controllo del contenuto dello zip
python3 tools/build.py                # → dist/risacca-mod.zip (da estrarre in ...\mods\)
python3 tools/sprites.py              # rigenera i PNG in resources/
python3 tools/rename.py extracted     # genera resources-dlc3/ dai file del ResourceExtractor
```

Non c'è un test runner. I test sono script con `assert`: per provarne uno basta lanciare il file. Sul PC Windows `lua` e Pillow non sono installati: i test Lua si possono lanciare con il Lua 5.3 del pacchetto Python `lupa`.

## Architettura

- **Lua.** Il gioco gira con Lua 5.3, su macOS è installato Lua 5.5. Il codice deve restare compatibile con la 5.3: niente `<const>`/`<close>`, niente operatori interi nuovi. Si usa solo l'API vanilla di Repentance, senza REPENTOGON né librerie esterne.
- **`logic.lua`.** È la logica pura e non tocca mai `Isaac`/`Game`, così si testa fuori dal gioco. Contiene:
  - le scritte in `L.TEXT`, le priorità in `L.PRIO` e le descrizioni per External Item Descriptions in `L.EID`;
  - le decisioni (`pickupText`, `ansia`, `isFinalBoss`, `deadGodBonus`, …);
  - la coda delle scritte `newQueue`.
- **`main.lua`.** Fa solo da collegamento con le callback del gioco, e ha tre sezioni:
  - **oggetti nuovi:** Ho Rotto il Gioco, -1 al Dead God, Win Streak;
  - **scritte a schermo:** ognuna fa `say(...)` → la coda → `HUD:ShowItemText` dentro `MC_POST_UPDATE`;
  - **oggetti dei tormentoni:** Non Vi Rubo Altro Tempo, Potrebbe Stare Qua, Il Miracolo di San Gennaruzzo, Che Fai, Te Ne Privi?, La Mossa del Pro Player. Stanno in fondo perché usano anche `say`.

  La stessa callback può essere registrata due volte, una per sezione, ed è voluto.
- **Coda delle scritte.**
  - Mostra una sola scritta per tick: vince la priorità più alta e, a parità, quella aggiunta per prima. Le altre pronte nello stesso tick vengono scartate.
  - Quando esce una scritta, vengono scartate anche quelle con priorità minore che uscirebbero entro i 15 tick successivi.
  - Una scritta con delay N esce al tick N+1.

  Per questo, nello smoke test, gli eventi da distinguere vanno separati da `frames(n)`.
- **Stato della run.** Sta nella tabella `run` di `main.lua` e si salva con `mod:SaveData(json.encode(run))` a inizio run, a ogni nuovo piano, a ogni boss contato da -1 al Dead God, quando compaiono The Beast o Mega Satan e quando si esce dal gioco. In `MC_POST_GAME_STARTED` si ricarica con `pcall(json.decode, ...)`, ma solo se la run è continuata. `roomFlags` invece si azzera a ogni nuova stanza.
- **`tests/smoke.lua`.** Simula un'API Isaac minima:
  - enum finti con id da 10000 e `RegisterMod`;
  - un player finto e un HUD che registra le scritte.

  Alla fine controlla che ogni callback registrata sia stata chiamata. Se aggiungi una callback, aggiungi anche uno scenario che la chiama.
- **Contenuti XML e Sprite.** Gli oggetti nuovi stanno in `content/items.xml` e `content/itempools.xml`. Gli sprite si generano da griglie di caratteri in `tools/sprites.py`: non modificare i PNG a mano. Le immagini degli oggetti devono seguire fedelmente lo stile The Binding of Isaac: Repentance+; la guida completa agli standard visivi (palette, proporzioni 32x32, contorno 2px `(8, 0, 0)`, luce in alto a sinistra, riflessi del vetro e checklist) è documentata in `docs/standard-grafici.md` e supportata dalle skill in `.agents/skills/`. Come tavola di riferimento visivo ufficiale di tutti gli item vanilla c'è `docs/PC _ Computer - The Binding of Isaac_ Rebirth - Items - Items (Repentance).png`.
- **Rinomine dei vanilla.**
  - Esempi: chiavi → Chiaviz-Chiavoz, boss → Beppe Bossicchio, Bumbo → Bumbazzo, Greed → Ballerino di Flamenco.
  - Le genera `tools/rename.py` in `resources-dlc3/` (git-ignored, perché contiene i testi del gioco e la repo non deve ridistribuirli), partendo dagli originali messi in `extracted/` (git-ignored).
  - Gli originali sono `items.xml`, `pocketitems.xml` e `stringtable.sta`, presi dal ResourceExtractor dell'utente.
- **Pacchetto.** `tools/build.py` mette nello zip solo `metadata.xml`, `main.lua`, `logic.lua`, `content/`, `resources/` e `resources-dlc3/`. Esclude `docs/`, `tools/`, `tests/`, `extracted/` e i file nascosti.
- **Pubblicazione.** In `metadata.xml` la visibilità resta `Private` finché l'utente non dà l'ok alla pubblicazione.
- **Repo e release.** La repo GitHub è privata. Lo zip allegato alle release contiene `resources-dlc3/`, quindi i testi del gioco: se la repo diventa pubblica, gli allegati diventano pubblici con lei.

## Testi

- Le scritte a schermo usano lettere accentate, come "È XL?". Se in gioco il font non le mostra, la soluzione prevista è usare `"E' XL?"` in `L.TEXT`, aggiornando anche gli `assert` nei test.
- I commit finiscono con `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
