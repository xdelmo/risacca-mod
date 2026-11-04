# Mod "Risacca" per The Binding of Isaac: Repentance

## Context
Fan-mod regalo per lo youtuber Risacca (youtube.com/@Risaacca, ~3,9K iscritti, una run Repentance al giorno).
Obiettivo dell'utente: pubblicarla sullo Steam Workshop e fargliela giocare in un video → deve essere stabile, non crashare, e far ridere per riferimenti riconoscibili.
L'utente non ha esperienza: Claude scrive tutto (Lua + sprite). L'utente prova su PC Windows con Isaac su Steam; lo sviluppo avviene su questo Mac.

Riferimenti presi dai titoli del canale: "ho rotto il gioco", Win Streak, "-N al Dead God", DEVASTO / si ASFALTA TUTTO, funghi, Incubus/Twisted Pair, Tainted Jacob/Lost, Eden.

## Goals
1. **3 oggetti nuovi** (l'utente ha tolto DEVASTO, Asfalto, Due Funghi Bastano):
   | Nome | Tipo | Effetto |
   |---|---|---|
   | Ho Rotto il Gioco | attivo, 6 cariche | genera un oggetto glitchato casuale (stile TMTRAINER) |
   | Win Streak | trinket | +danno per ogni piano finito senza essere colpito; si azzera al primo colpo |
   | -1 al Dead God | passivo | piccolo bonus a tutte le stat per ogni boss ucciso |
2. **"GODOR!"** (tormentone di Risacca quando succede qualcosa di buono): scritta grande a schermo quando il player raccoglie un oggetto di qualità 3 o 4. Solo testo, niente voce (servirebbe una clip fornita da Risacca stesso).
3. **"È XL?"** (Risacca chiede sempre se un piano è XL): all'inizio di OGNI piano compare "È XL?" con sottotitolo "SÌ, È XL!" oppure "No... non è XL".
4. **Rinomine dei testi vanilla** (nomi + descrizioni di oggetti, trinket, carte, pillole; testi inglesi, Risacca gioca in inglese) — scelte dell'utente:
   - key / keys → **Chiaviz-Chiavoz**
   - bomb / bombs → **Bombiz-Bomboz**
   - boss → **Beppe Bossicchio**, bosses → **Beppe Bossicchi** (solo la parola nei testi, NON schermata VS)
   - Incubus → **Il buddy più forte del gioco**
   - Bumbo → **Bumbazzo** (parola intera, ovunque nei testi)
   - Greed → **Ballerino di Flamenco** (parola intera, ovunque nei testi; "Greedier" resta)
5. **"Il Beasty Boy"** (nome che Risacca dà a The Beast, confermato dai video): il nome di The Beast non compare mai come testo, quindi all'inizio dello scontro compare a schermo "IL BEASTY BOY" (rilevato con `MC_POST_NPC_INIT` su `EntityType.ENTITY_BEAST`, variant 0, una volta per run).
6. **"Mega Stanley Kubrick"** (richiesta dell'utente): stesso meccanismo di Beasty Boy, all'inizio dello scontro con Mega Satan (`EntityType.ENTITY_MEGA_SATAN`) compare "MEGA STANLEY KUBRICK". In più `rename.py` sostituisce "Mega Satan" → "Mega Stanley Kubrick" nei testi, se compare (regola applicata prima di quella su "boss").
8. **"GODOR MAXIMOR!"**: quando raccogli un oggetto di qualità 4 compare GODOR MAXIMOR! al posto di GODOR!, che resta per la qualità 3.
9. **"C'ho l'ansia"**: compare quando la vita del player scende a mezzo cuore o meno, contando cuori rossi e cuori soul/black. Scatta una volta sola, e può riscattare solo dopo che il player è risalito sopra il mezzo cuore. Il controllo si fa in `MC_POST_PLAYER_UPDATE`.
10. **"Tacchino!"**: compare quando il player perde un cuore intero o più in un colpo solo (`MC_ENTITY_TAKE_DMG`, amount ≥ 2). Al massimo una volta per stanza, il contatore si azzera con `MC_POST_NEW_ROOM`. Se nello stesso momento scatta anche "C'ho l'ansia", vince l'ansia.
11. **"Alla facciazza vostra!"**: compare quando prendi un oggetto pagato con i cuori, cioè un patto col diavolo. Si rileva in `MC_PRE_PICKUP_COLLISION` su un collectible con `Price < 0` e `Price ~= PickupPrice.PRICE_FREE`. Se l'oggetto è anche di qualità 3 o 4, questa scritta prende il posto di GODOR.
12. **"Un bacione grande dal vostro Risacca"**: compare quando muore un boss finale (`MC_POST_NPC_DEATH` su The Lamb, ??? (Isaac variant 1), Isaac, Mega Satan 2, Delirium, Mother, The Beast, Hush, Satan, Ultra Greed). La lista esatta dei tipi la decide il builder. Non uso `MC_POST_GAME_END`, perché lì la scritta finirebbe coperta dalla schermata finale.
13. **"Calmati babbuino"**: compare alla morte del player, il primo frame in cui `player:IsDead()` è vero in `MC_POST_PLAYER_UPDATE`. La scritta resta visibile durante l'animazione della morte. Se il player rinasce con 1up o Lazarus la scritta compare lo stesso, ed è voluto.
7. **Intro**: all'inizio di ogni run (`MC_POST_GAME_STARTED` con `isContinued == false`, dopo ~1s) compare "Ciao a tutti, io sono Risacca" con sottotitolo "Benvenuti sul mio canale". La frase è confermata dai video.

## Tormentoni confermati (15 trascrizioni YouTube)
Sono salvate per ora nel localStorage di Chrome su youtube.com, chiavi `tx_<videoId>`. **Primo passo dell'implementazione:** salvarle in `risacca-mod/docs/trascrizioni/<videoId>.txt`, perché in modalità piano posso scrivere solo questo file.

Cosa ho trovato:
- **Parole e nomi suoi:**
  - "chiaviz" / "chiavozzal" (usate davvero)
  - "bombiz" / "bombozza"
  - "Beppe Bossicchio"
  - "Beasty Boy"
  - "godo" (67 volte) e "godor maximor"
  - "Mega Satana", detto in italiano
- **Frasi più frequenti:**
  - "c'ho l'ansia" (32 volte)
  - "schiattati" (38)
  - "sminchiare la build/run" (17)
  - "sono illegale, devo essere bannato da questo gioco" e "run illegale totale"
  - "spidappiamo"
  - "tutta salute"
  - "vai via"
  - "il mio amico Abdomination"
  - "ahi ahi ahi"
  - "ti prego, dammi qualcosa"
- **Seconda passata** (frasi più ripetute):
  - "mamma mia" (171 volte), "vai via" (111), "vai vai vai" (71)
  - "ti prego" (85), "per favore" (85)
  - "facciamo così" (98), "ce ne possiamo andare" (76), "non mi interessa" (67)
  - "tacchino!" (16), quando sbaglia
  - "babbuino": "calmati babbuino", "sono un babbuino"
  - "alla facciazza vostra/tua!"
  - "signor X": signor War, signor Krampus, signor gioco
  - "bravo, fenomeno", "fermi tutti", "chillatela"
  - "un bacione grande dal vostro Risacca"
- **Intro e outro fissi:**
  - "Ciao a tutti, io sono Risacca. Benvenuti sul mio canale"
  - "Per oggi è tutto. Un caro saluto. Ciao, alla prossima."

## Non-goals
- Personaggio giocabile, boss nuovi, schermata VS, icone HUD.
- Traduzione italiana del gioco.
- Dipendenza da REPENTOGON (i fan devono poterla usare senza installare nulla).

## Anti-goals
- Crash o errori Lua durante un video.
- Battute generiche non legate a Risacca.

## Struttura (cartella `~/development/hobbies/risacca-mod/`)
```
metadata.xml                       nome, descrizione Workshop, versione
main.lua                           tutta la logica dei 3 oggetti (un file solo)
content/items.xml                  definizione 3 oggetti nuovi
resources/gfx/items/collectibles/  2 sprite 32x32
resources/gfx/items/trinkets/      1 sprite 32x32
resources-dlc3/items.xml           override vanilla con nomi rinominati (generato)
resources-dlc3/pocketitems.xml     override carte/pillole (generato, se servono)
tools/rename.py                    genera gli override dai file estratti del gioco + assert self-check
tools/sprites.py                   disegna gli sprite pixel-art da griglie in codice (PIL)
```

## Approccio
**Oggetti nuovi** – API Lua vanilla Repentance (`RegisterMod`, callbacks):
- Ho Rotto il Gioco: `MC_USE_ITEM` → dai temporaneamente TMTRAINER, spawna pedestal casuale, rimuovi TMTRAINER (trucco noto per oggetti glitchati). Se instabile: fallback a reroll caotico dell'oggetto (scelta del builder).
- Win Streak: `MC_ENTITY_TAKE_DMG` sul player azzera, `MC_POST_NEW_LEVEL` incrementa se pulito, `MC_EVALUATE_CACHE` +0.5 danno × streak. Stato persistito con `mod:SaveData` (json).
- -1 al Dead God: `MC_POST_NPC_DEATH` con `npc:IsBoss()` → contatore → `MC_EVALUATE_CACHE` (+0.2 danno, +0.03 velocità, +0.1 range, +0.05 tears per boss; cap 10).

- GODOR!: Repentance vanilla non ha un callback "oggetto aggiunto" → in `MC_POST_PLAYER_UPDATE` osservare `player.QueuedItem.Item`; quando passa da nil a un oggetto (per player), leggere `Isaac.GetItemConfig():GetCollectible(id).Quality`; se ≥3 → `Game():GetHUD():ShowItemText("GODOR!")`. Ritardare di ~1s per non sovrapporsi al nome dell'oggetto (scelta del builder).

- È XL?: `MC_POST_NEW_LEVEL` → `Game():GetLevel():GetCurses() & LevelCurse.CURSE_OF_LABYRINTH ~= 0`; dopo ~2s (contatore frame in `MC_POST_UPDATE`, per non coprire il nome del piano) → `HUD:ShowItemText("È XL?", risposta)`. Verificare che il font del gioco mostri "È"/"Ì"; se no usare "E' XL?" / "SI'".

**Rinomine** – in Repentance `items.xml`/`pocketitems.xml` contengono segnaposto `#XXX_NAME` risolti da `stringtable.sta`. `tools/rename.py`:
1. legge i file estratti (ResourceExtractor in `<Isaac>/tools/ResourceExtractor`, eseguito dall'utente sul PC: ci servono `items.xml`, `pocketitems.xml`, `stringtable.sta` da `resources-dlc3/`);
2. risolve i nomi inglesi, applica le regole con regex a parola intera, case-insensitive (es. "Bomber Boy" NON cambia);
3. scrive l'override con testo letterale solo per le voci toccate (le altre restano segnaposto).
Limite noto: override intero del file → conflitto con altre mod che sostituiscono `items.xml`, da rigenerare dopo patch del gioco.

**Sprite** – pixel art 32×32 disegnata da `tools/sprites.py`; anteprima ingrandita mostrata all'utente in Chrome per approvazione prima del pacchetto finale.

## Lasciato al builder
Valori numerici esatti, palette sprite, testo descrizioni (in italiano, tono Risacca), ordine dei task.

## Verifica
1. `python3 tools/rename.py --selftest` (assert: Skeleton Key→"Skeleton Chiaviz-Chiavoz", Bobby-Bomb→"Bobby-Bombiz-Bomboz", Bomber Boy invariato, Incubus→"Il buddy più forte del gioco").
2. Utente copia la cartella in `C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\mods\risacca-mod\`, attiva la console (`EnableDebugConsole=1` in `options.ini`).
3. In gioco: `giveitem` per ogni oggetto nuovo; `giveitem c175` (Skeleton Key), `c360` (Incubus), `c125` (Bobby-Bomb) per le rinomine. GODOR!: spawnare un oggetto Q4 (`spawn 5.100.331` Godhead) e raccoglierlo dal piedistallo → compare GODOR!; uno Q1 (`spawn 5.100.1` Sad Onion) → non compare. È XL?: `stage 2` → risposta corretta; `curse 2` (Labyrinth) + `stage 1` → "SÌ, È XL!". Beasty Boy: `stage 13` (Home), poi si va avanti fino a The Beast → compare la scritta. Mega Stanley Kubrick: `spawn 274` → compare la scritta. Intro: nuova run → "Ciao a tutti, io sono Risacca"; continuando una run salvata la scritta non deve comparire. GODOR MAXIMOR: `spawn 5.100.331` (Godhead, qualità 4) → MAXIMOR; un oggetto di qualità 3 → GODOR!. Ansia: farsi colpire fino a mezzo cuore → la scritta compare una volta sola; dopo una cura e un nuovo colpo ricompare. Tacchino: farsi colpire da un nemico che toglie un cuore intero (dal Basement 3 in su, o un boss del Womb) → la scritta compare una volta per stanza. Facciazza: `stage 2`, poi `goto s.devil` e comprare un oggetto → compare. Bacione: `stage 8`, battere Mom's Heart non deve far comparire niente; `stage 10` (Sheol) + Satan → compare. Babbuino: `kill` del player in modalità debug (o farsi uccidere) → compare.
4. Controllo errori: `Documents\My Games\Binding of Isaac Repentance\log.txt` (nessun `[ERROR]` Lua) — l'utente ci manda le righe rilevanti.
5. Upload: `<Isaac>/tools/ModUploader/ModUploader.exe`, visibilità "privata" finché non approvata, poi pubblica.
