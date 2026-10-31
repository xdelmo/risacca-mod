# Mod Risacca — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Mod Repentance (Lua vanilla, niente REPENTOGON) con 3 oggetti nuovi, 11 scritte-tormentone a schermo e rinomine dei testi vanilla, dedicata a Risacca.
**Architecture:** La logica pura (decisioni senza API di gioco) sta in `logic.lua` e si testa sul Mac con Lua 5.4; `main.lua` collega le callback di Isaac a quelle funzioni e mostra le scritte da una coda con priorità. I tool Python (`rename.py`, `sprites.py`, `build.py`) generano override XML, sprite e pacchetto finale, ognuno con `--selftest`.
**Tech Stack:** Lua (Isaac usa 5.3; test locali con `lua` 5.4 di Homebrew), Python 3 + PIL 13, XML.
**Spec:** `docs/superpowers/specs/2026-11-01-risacca-mod-design.md`

## Global Constraints
- Solo API vanilla Repentance; nessuna dipendenza (REPENTOGON, EID, ecc.).
- Nessun errore Lua: ogni callback ritorna `nil` salvo dove l'API vuole un valore (`MC_USE_ITEM` → `true`).
- Testi degli oggetti nuovi in italiano; testi vanilla restano in inglese tranne le rinomine.
- Rinomine (regex a parola intera, case-insensitive, in quest'ordine): `Mega Satan`→`Mega Stanley Kubrick`; nome esatto `Incubus`→`Il buddy più forte del gioco`; `keys?`→`Chiaviz-Chiavoz`; `bombs?`→`Bombiz-Bomboz`; `boss(es)?`→`Beppe Bossicchio`; `Bumbo`→`Bumbazzo`; `Greed`→`Ballerino di Flamenco` (parola intera: "Greedier" invariato).
- Tutte le stringhe a schermo stanno in un'unica tabella `L.TEXT` in `logic.lua` (per poterle sostituire in un punto se il font non mostra gli accenti).
- Cartella mod: `~/development/hobbies/risacca-mod/`; il pacchetto per il PC contiene solo `metadata.xml`, `main.lua`, `logic.lua`, `content/`, `resources/`, `resources-dlc3/`.

## Review Focus
1. **The Lost / Keeper / personaggi senza cuori rossi** → "C'ho l'ansia" non deve scattare a inizio run né restare in loop: si arma solo dopo che la vita è stata > 1 mezzo-cuore (test `ansia_lost`).
2. **Scritte simultanee** (colpo da cuore intero che porta a mezzo cuore; morte dopo un colpo) → si vede solo quella con priorità più alta, niente sfarfallio (test `queue_suppresses_lower`).
3. **Boss a più fasi/segmenti** (Satan, Mother, Larry Jr) → "Bacione" e il contatore -1 al Dead God scattano al massimo una volta per stanza (test `once_per_room`).
4. **Run continuata** → intro non compare, Win Streak e contatore Dead God ripristinati dal salvataggio (verifica manuale passo 3 di Task 8).
5. **Override `resources-dlc3/items.xml`** → se il gioco ignora l'override o va in crash all'avvio, la mod deve restare usabile togliendo solo quella cartella (verifica manuale Task 8, prima con e poi senza override).

---

### Task 1: Logica pura + test (`logic.lua`)

**Files:**
- Create: `logic.lua`, `tests/test_logic.lua`

**Interfaces:**
- Produces (tabella restituita da `logic.lua`, caricata in gioco con `include("logic")`, nei test con `dofile("logic.lua")`):
  - `L.TEXT` — `GODOR="GODOR!"`, `MAXIMOR="GODOR MAXIMOR!"`, `XL_Q="È XL?"`, `XL_YES="SÌ, È XL!"`, `XL_NO="No... non è XL"`, `BEASTY="IL BEASTY BOY"`, `KUBRICK="MEGA STANLEY KUBRICK"`, `INTRO="Ciao a tutti, io sono Risacca"`, `INTRO_SUB="Benvenuti sul mio canale"`, `ANSIA="C'ho l'ansia"`, `TACCHINO="Tacchino!"`, `FACCIAZZA="Alla facciazza vostra!"`, `BACIONE="Un bacione grande"`, `BACIONE_SUB="dal vostro Risacca"`, `BABBUINO="Calmati babbuino"`
  - `L.PRIO` — `XL=1, INTRO=1, PICKUP=2, TACCHINO=2, ANSIA=3, BOSSNAME=3, BACIONE=4, BABBUINO=5`
  - `L.pickupText(quality: int, devilDeal: bool) -> string|nil` (devil → FACCIAZZA; Q4 → MAXIMOR; Q3 → GODOR; altrimenti nil)
  - `L.xlText(isXL: bool) -> title, subtitle`
  - `L.ansia(armed: bool, halfHearts: int) -> fire: bool, armed: bool` (≤1 e armato → true,false; >1 → false,true; altrimenti false,armed)
  - `L.isDevilPrice(price: int) -> bool` (`price < 0 and price ~= -1000`)
  - `L.isFinalBoss(type: int, variant: int) -> bool` — tabella: 273 Lamb, 102 v0 Isaac, 102 v1 ???, 275 Mega Satan 2, 412 Delirium, 912 v0 Mother, 951 v0 Beast, 407 Hush, 84 Satan, 406 v1 Ultra Greedier. (Satan e Ultra Greed v0 si gestiscono col vincolo una-volta-per-stanza in `main.lua`.)
  - `L.streakOnNewLevel(streak: int, hitThisFloor: bool) -> int` (colpito → 0, altrimenti +1)
  - `L.deadGodBonus(kills: int) -> {damage, speed, range, fireDelay}` con `k = min(kills,10)`: `0.2k`, `0.03k`, `4k` (TearRange, unità pixel), `-0.1k`
  - `L.newQueue() -> q` con `q:push(title, sub, delayFrames, prio)` e `q:tick() -> title, sub` (nil se niente). `tick` avanza di un frame, prende tra gli elementi scaduti quello con prio più alta (a parità, il primo inserito), lo restituisce e scarta gli altri scaduti e quelli in attesa con prio minore che scadono entro 15 frame.

- [ ] **Step 1:** `brew install lua` (serve solo per test/sintassi). Verifica: `lua -v` stampa 5.4.x.
- [ ] **Step 2: Scrivi `tests/test_logic.lua`** (assert semplici, stampa `OK` alla fine). Casi:
  - `pickupText(4,false)=="GODOR MAXIMOR!"`, `(3,false)=="GODOR!"`, `(2,false)==nil`, `(1,true)=="Alla facciazza vostra!"`, `(4,true)=="Alla facciazza vostra!"`
  - `xlText(true)` → `"È XL?","SÌ, È XL!"`; `xlText(false)` → sub `"No... non è XL"`
  - `ansia_lost`: partendo da `armed=false`, chiamate ripetute con 0 o 1 non scattano mai
  - ansia: armed=true, 1 → fire; poi 1 → no; poi 4 → no ma riarmato; poi 1 → fire
  - `isDevilPrice(-1)`, `(-3)` true; `(-1000)`, `(0)`, `(15)` false
  - `isFinalBoss(273,0)`, `(102,1)`, `(951,0)` true; `(951,10)`, `(45,0)` (Mom) false
  - `streakOnNewLevel(2,false)==3`, `(5,true)==0`
  - `deadGodBonus(3).damage≈0.6`, `deadGodBonus(15).damage≈2.0` (cap)
  - `queue_suppresses_lower`: push(TACCHINO,nil,2,2) e push(ANSIA,nil,0,3) → primo tick dà ANSIA, i tick successivi (30) danno nil
  - queue delay: push("A",nil,3,1) → tick 1..3 nil, tick 4 "A" (scade dopo `delay` tick completi)
- [ ] **Step 3:** `lua tests/test_logic.lua` → FAIL (`logic.lua` mancante).
- [ ] **Step 4:** Implementa `logic.lua` con le firme sopra (nessun riferimento a `Isaac`/`Game`).
- [ ] **Step 5:** `lua tests/test_logic.lua` → `OK`.
- [ ] **Step 6:** `git add logic.lua tests/test_logic.lua && git commit -m "feat: logica pura scritte e oggetti"`

### Task 2: Metadata, definizione oggetti e pool

**Files:**
- Create: `metadata.xml`, `content/items.xml`, `content/itempools.xml`, `.gitignore` (`dist/`, `extracted/`)

**Interfaces:**
- Produces: oggetti cercabili con `Isaac.GetItemIdByName("Ho Rotto il Gioco")`, `Isaac.GetItemIdByName("-1 al Dead God")`, `Isaac.GetTrinketIdByName("Win Streak")`; gfx attesi `collectibles/ho_rotto_il_gioco.png`, `collectibles/meno_uno_dead_god.png`, `trinkets/win_streak.png`.

- [ ] **Step 1:** `metadata.xml`: `name` "Risacca Mod", `directory` "risacca-mod", `version` 1.0, `visibility` Private, descrizione Workshop in italiano (2-3 righe, cita il canale).
- [ ] **Step 2:** `content/items.xml`: `<active>` Ho Rotto il Gioco (`maxcharges="6"`, `quality="2"`, description "Ho rotto il gioco!"), `<passive>` -1 al Dead God (`quality="2"`, `cache="damage speed range firedelay"`, description "Un boss alla volta"), `<trinket>` Win Streak (description "Non farti colpire"). Ogni voce con `gfx` come sopra.
- [ ] **Step 3:** `content/itempools.xml`: i due collectible in `treasure` (Weight 1); -1 al Dead God anche in `bossPool`. (I trinket entrano nel pool automaticamente.)
- [ ] **Step 4:** Verifica: `python3 -c "import xml.etree.ElementTree as E;[E.parse(f) for f in ['metadata.xml','content/items.xml','content/itempools.xml']];print('XML OK')"` → `XML OK`.
- [ ] **Step 5:** Commit `feat: metadata e definizione oggetti`.

### Task 3: Sprite (`tools/sprites.py`)

**Files:**
- Create: `tools/sprites.py`; genera `resources/gfx/items/collectibles/ho_rotto_il_gioco.png`, `.../meno_uno_dead_god.png`, `resources/gfx/items/trinkets/win_streak.png`, `docs/preview.png`

**Interfaces:**
- Produces: `python3 tools/sprites.py` scrive i 3 PNG 32×32 RGBA + anteprima 8× affiancata; `--selftest` verifica.

- [ ] **Step 1:** Selftest in `sprites.py` (`--selftest`): genera in una cartella temporanea e asserisce: 3 file, size `(32,32)`, mode `RGBA`, angolo (0,0) trasparente, ≥ 60 pixel opachi ciascuno, contorno scuro presente (almeno un pixel con luminanza < 40).
- [ ] **Step 2:** Esegui `--selftest` → FAIL.
- [ ] **Step 3:** Disegna da griglie di caratteri (una lettera = un colore della palette, contorno nero stile Isaac): Ho Rotto il Gioco = joypad crepato con pixel glitch; -1 al Dead God = lapide con "-1"; Win Streak = coppa con fiammella.
- [ ] **Step 4:** `--selftest` → PASS; poi `python3 tools/sprites.py`; apri `docs/preview.png` e mostrala all'utente per approvazione (modifiche → ritocca le griglie).
- [ ] **Step 5:** Commit `feat: sprite oggetti`.

### Task 4: Rinomine (`tools/rename.py`)

**Files:**
- Create: `tools/rename.py`

**Interfaces:**
- Produces: `rename_text(s: str) -> str` (applica le 6 regole dei Global Constraints in ordine; Incubus solo se il nome è esattamente "Incubus"); CLI `python3 tools/rename.py <cartella_estratta>` legge `<cartella>/items.xml`, `pocketitems.xml`, `stringtable.sta` e scrive `resources-dlc3/items.xml` e `resources-dlc3/pocketitems.xml`; `--selftest`.
- Regole file: attributi `name` e `description` di ogni elemento; se il valore inizia con `#` lo risolve nella prima `<string>` della `<key name="...">` corrispondente in `stringtable.sta` (se non trovato, lascia invariato). Scrive il testo letterale **solo** se `rename_text` lo cambia; tutto il resto del file resta identico all'originale (stessi elementi, stessi attributi, stesso ordine).

- [ ] **Step 1:** `--selftest` con assert: `"Skeleton Key"`→`"Skeleton Chiaviz-Chiavoz"`; `"Bobby-Bomb"`→`"Bobby-Bombiz-Bomboz"`; `"Bomber Boy"` invariato; `"Keeper's Box"` invariato; `"Mom's Key"`→`"Mom's Chiaviz-Chiavoz"`; `"+5 bombs"`→`"+5 Bombiz-Bomboz"`; `"Boss Rush"`→`"Beppe Bossicchio Rush"`; `"Mega Satan"`→`"Mega Stanley Kubrick"` (non "Mega Satan" + Beppe); nome `"Incubus"`→`"Il buddy più forte del gioco"`; `"Bumbo"`→`"Bumbazzo"`; `"Bumbo's Heart"`→`"Bumbazzo's Heart"`; `"Greed's Gullet"`→`"Ballerino di Flamenco's Gullet"`; `"Ultra Greedier"` invariato. Più un mini XML inline (2 voci, una con `#PLACEHOLDER` risolto da una mini stringtable) → controlla che solo la voce toccata diventi letterale e che il numero di elementi sia uguale.
- [ ] **Step 2:** `python3 tools/rename.py --selftest` → FAIL.
- [ ] **Step 3:** Implementa con `re` + `xml.etree.ElementTree` (scrittura con `encoding="utf-8", xml_declaration=True`).
- [ ] **Step 4:** `--selftest` → `OK`.
- [ ] **Step 5:** Commit `feat: generatore rinomine`.
- [ ] **Step 6 (dipende dall'utente):** chiedere all'utente di lanciare `<Isaac>/tools/ResourceExtractor/ResourceExtractor.exe` e mandare `items.xml`, `pocketitems.xml`, `stringtable.sta` (da `extracted_resources/resources-dlc3/` o `resources/`, quelli più recenti). Metterli in `extracted/` (ignorata da git), lanciare il CLI, controllare con `grep -c Chiaviz resources-dlc3/items.xml` (> 0), committare l'output.

### Task 5: `main.lua` — oggetti nuovi

**Files:**
- Create: `main.lua`

**Interfaces:**
- Consumes: `L.deadGodBonus`, `L.streakOnNewLevel`, `L.isFinalBoss` (Task 1); nomi oggetti (Task 2).
- Produces (per Task 6, nello stesso file): `local mod = RegisterMod("Risacca", 1)`, `local L = include("logic")`, `local json = require("json")`, tabella `local run = {streak=0, hitThisFloor=false, deadGodKills=0}` salvata con `save()` / caricata in `MC_POST_GAME_STARTED` (se `isContinued==false` → valori iniziali), `local roomFlags = {}` azzerata in `MC_POST_NEW_ROOM`.

- [ ] **Step 1:** Ho Rotto il Gioco: `MC_USE_ITEM` sull'ID → `player:AddCollectible(CollectibleType.COLLECTIBLE_TMTRAINER, 0, false)`, `Isaac.Spawn(5, 100, 0, Isaac.GetFreeNearPosition(player.Position, 40), Vector.Zero, nil)`, poi `player:RemoveCollectible(CollectibleType.COLLECTIBLE_TMTRAINER)`; se il player aveva già TMTRAINER non rimuoverlo. Ritorna `true`.
- [ ] **Step 2:** Win Streak: `MC_ENTITY_TAKE_DMG` (filtro `EntityType.ENTITY_PLAYER`) → `run.streak=0`, `run.hitThisFloor=true`; `MC_POST_NEW_LEVEL` → se un player ha il trinket `run.streak = L.streakOnNewLevel(run.streak, run.hitThisFloor)`; poi `hitThisFloor=false`, cache damage + `EvaluateItems` su tutti i player, `save()`. `MC_EVALUATE_CACHE` damage: `+0.5 * run.streak * player:GetTrinketMultiplier(id)` se ha il trinket.
- [ ] **Step 3:** -1 al Dead God: `MC_POST_NPC_DEATH` → se `npc:IsBoss()`, non già `roomFlags.deadGod`, e qualcuno ha l'oggetto → `run.deadGodKills+1`, flag, cache all + `EvaluateItems`, `save()`. `MC_EVALUATE_CACHE` applica `L.deadGodBonus(run.deadGodKills)` × `player:GetCollectibleNum(id)` ai campi `Damage`, `MoveSpeed`, `TearRange`, `MaxFireDelay`.
- [ ] **Step 4:** Commit `feat: oggetti nuovi`.

### Task 6: `main.lua` — scritte

**Files:**
- Modify: `main.lua`

**Interfaces:**
- Consumes: tutto `L.*` (Task 1); `mod`, `run`, `roomFlags` (Task 5).

- [ ] **Step 1:** Coda: `local q = L.newQueue()`; `MC_POST_UPDATE` → `local t,s = q:tick(); if t then Game():GetHUD():ShowItemText(t, s or "") end`. Funzione locale `say(t, s, delay, prio)` = `q:push`.
- [ ] **Step 2:** Intro: `MC_POST_GAME_STARTED` con `not isContinued` → `say(INTRO, INTRO_SUB, 30, PRIO.INTRO)`.
- [ ] **Step 3:** È XL?: `MC_POST_NEW_LEVEL` → `isXL = Game():GetLevel():GetCurses() & LevelCurse.CURSE_OF_LABYRINTH ~= 0` → `local t,s = L.xlText(isXL); say(t, s, 90, PRIO.XL)`. Delay 90 (3 s) sempre: così al primo piano l'intro (delay 30) compare prima e non si sovrappongono.
- [ ] **Step 4:** Pickup: `MC_PRE_PICKUP_COLLISION` (variant 100) con `L.isDevilPrice(pickup.Price)` e collider player → `devilPending[playerIndex] = pickup.SubType`. `MC_POST_PLAYER_UPDATE`: `local qi = player.QueuedItem.Item`; quando passa da nil a un `qi` con `qi:IsCollectible()` → `t = L.pickupText(qi.Quality, devilPending[idx] == qi.ID)`, azzera `devilPending[idx]`, se `t` → `say(t, nil, 45, PRIO.PICKUP)`. Indice player: `GetPtrHash(player)`.
- [ ] **Step 5:** Ansia: in `MC_POST_PLAYER_UPDATE`, `half = player:GetHearts() + player:GetSoulHearts()`; stato `armed[idx]` inizializzato a `half > 1` al primo update del player; `fire, armed[idx] = L.ansia(armed[idx], half)`; fire → `say(ANSIA, nil, 0, PRIO.ANSIA)`.
- [ ] **Step 6:** Tacchino: `MC_ENTITY_TAKE_DMG` player con `amount >= 2` e non `roomFlags.tacchino` → flag, `say(TACCHINO, nil, 2, PRIO.TACCHINO)` (la coda lo sopprime se arriva l'ansia).
- [ ] **Step 7:** Babbuino: `MC_POST_PLAYER_UPDATE`, `player:IsDead()` passa da false a true → `say(BABBUINO, nil, 0, PRIO.BABBUINO)`.
- [ ] **Step 8:** Nomi boss: `MC_POST_NPC_INIT` con `npc.Type==EntityType.ENTITY_BEAST and npc.Variant==0` e `not run.beastyShown` → `say(BEASTY,...,30,PRIO.BOSSNAME)`, flag in `run`; uguale per `EntityType.ENTITY_MEGA_SATAN` variant 0 con `run.kubrickShown`.
- [ ] **Step 9:** Bacione: `MC_POST_NPC_DEATH` con `L.isFinalBoss(npc.Type, npc.Variant)` e non `roomFlags.bacione` → flag, `say(BACIONE, BACIONE_SUB, 30, PRIO.BACIONE)`.
- [ ] **Step 10:** Commit `feat: scritte tormentoni`.

### Task 7: Smoke test con API finta + build

**Files:**
- Create: `tests/smoke.lua`, `tools/build.py`

**Interfaces:**
- Consumes: `main.lua`, `logic.lua`.
- Produces: `lua tests/smoke.lua` stampa `SMOKE OK`; `python3 tools/build.py` crea `dist/risacca-mod.zip` con solo i file elencati nei Global Constraints.

- [ ] **Step 1:** `tests/smoke.lua`: definisce stub globali (`RegisterMod` che registra le callback in una tabella, `include` = `dofile(name..".lua")`, `require("json")` stub encode/decode, `Isaac`, `Game`, `Vector`, `GetPtrHash`, enum tramite metatable che restituisce numeri distinti per chiave, player finto con cuori/QueuedItem configurabili, NPC finti). Carica `main.lua`, poi chiama ogni callback registrata con argomenti plausibili e scenari: nuova run, raccolta Q4, colpo da 2 che porta a 1 mezzo-cuore (60 update → solo "C'ho l'ansia" mostrato), morte, Satan ucciso due volte nella stessa stanza (un solo Bacione). Registra le chiamate a `ShowItemText` e le confronta.
- [ ] **Step 2:** `lua tests/smoke.lua` → deve passare; se fallisce correggi `main.lua` (non lo stub, salvo stub sbagliato).
- [ ] **Step 3:** `tools/build.py` (zipfile stdlib) + `--selftest` che controlla che lo zip non contenga `docs/`, `tools/`, `tests/`, `extracted/`. Esegui `--selftest` poi la build.
- [ ] **Step 4:** Esegui tutto: `lua tests/test_logic.lua && lua tests/smoke.lua && python3 tools/rename.py --selftest && python3 tools/sprites.py --selftest && python3 tools/build.py --selftest` → tutti OK.
- [ ] **Step 5:** Commit `feat: smoke test e build`.

### Task 8: Prova sul PC dell'utente (manuale)

- [ ] **Step 1:** Mandare all'utente `dist/risacca-mod.zip` e istruzioni passo-passo in italiano semplice: estrarre in `...\The Binding of Isaac Rebirth\mods\risacca-mod\`, `EnableDebugConsole=1` in `options.ini`, avviare.
- [ ] **Step 2:** Checklist della spec (sezione Verifica, punto 3) una voce alla volta; inoltre verificare che "È"/"Ì" si vedano: se compaiono quadratini, sostituire in `L.TEXT` con `"E' XL?"`, `"SI', E' XL!"`, `"No... non e' XL"` e ricostruire.
- [ ] **Step 3:** Run continuata: salvare e uscire a metà run, riprendere → niente intro, Win Streak e bonus Dead God invariati.
- [ ] **Step 4:** Override: se il gioco crasha/ignora le rinomine, riprovare senza `resources-dlc3/` per isolare il problema (Review Focus 5).
- [ ] **Step 5:** Errori Lua: l'utente manda le righe `[ERROR]`/`Lua` di `Documents\My Games\Binding of Isaac Repentance\log.txt`; correggere, ripetere.
- [ ] **Step 6:** Upload privato con `ModUploader.exe`; pubblico solo dopo l'ok dell'utente.
