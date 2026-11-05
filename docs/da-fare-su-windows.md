# Cosa fare sul PC Windows

Le caselle spuntate sono già confermate dai log, dal salvataggio della mod o dagli screenshot. Spunta le altre man mano e alla fine manda quello che è elencato nella sezione **Da inviarmi**.

Prima di provare, chiudi e riapri il gioco: le modifiche alla mod si vedono solo dopo il riavvio.

## 1. Installazione

- [x] La mod è in `C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\mods\risacca-mod\`. Non è la repo ma una copia senza `.git`: le modifiche alla repo arrivano in gioco solo copiandole lì. Oggi ha gli stessi 33 file dello zip della release v1.3, a parte i fine riga.
- [x] La console di debug è attiva (`EnableDebugConsole=1` in `Documenti\My Games\Binding of Isaac Repentance+\options.ini`).
- [x] Il gioco carica la mod senza errori Lua.
- [ ] Installazione da zero seguendo solo il `readme.txt` dello zip (prima sposta altrove la cartella della repo): la mod compare nel menu **Mods** e si attiva. Controlla anche se la cartella `mods` esiste già e se Windows chiede l'autorizzazione a copiare. Lo zip della v1.3 ha la struttura descritta dal readme (`risacca-mod/` e `readme.txt`) e `metadata.xml` è `Private`; l'installazione vera non è stata fatta.

## 2. Provare le scritte

Nuova run, con un personaggio qualsiasi:

- [x] Poco dopo compare **"È XL?"**, poi **"No... non è XL"**. In un piano XL deve uscire **"SÌ, È XL!"**. Confermati entrambi, ciascuno in un'unica scritta con "È XL?". Il piano XL si forza con `curse 2` seguito da `stage 2`.
- [x] **Controlla le lettere accentate:** guarda se "È" e "Ì" si vedono bene. Se vedi quadratini o lettere sbagliate, fai uno screenshot. "È", "è" e "Ì" si vedono bene.
- [x] Raccogli un oggetto di qualità 3 o 4: compare **"IL GODOR!"** o **"GODOR MAXIMOR!"**.
- [x] Prendi un oggetto con un patto col diavolo, pagandolo in cuori: compare **"Alla facciazza vostra!"**.
- [x] Prendi un colpo da un cuore intero: compare **"Tacchino!"**.
- [x] Scendi a mezzo cuore: compare **"C'ho l'ansia"**.
- [x] Muori: compare **"Beduins"**.

- [ ] **Meno scritte:** raccogli due oggetti della stessa qualità entro 30 secondi: la scritta compare solo la prima volta. Controlla che le scritte non siano più troppe. Il cooldown è confermato (Sad Onion e Spoon Bender, qualità 3: **IL GODOR!** solo al primo). Resta da giudicare se le scritte sono troppe.

## 3. Provare gli oggetti nuovi

Apri la console con il tasto `\` (quello sopra Invio, oppure `ò`/`ù` sulla tastiera italiana). Puoi usare **Tab** per completare il nome dell'oggetto.

- [x] `giveitem Ho Rotto il Gioco`, poi usa l'oggetto con la barra spaziatrice: compare un oggetto glitchato.
- [x] `giveitem -1 al Dead God`, poi uccidi un boss: le statistiche salgono (danno 3.50 → 3.70).
- [x] `giveitem Win Streak`, poi finisci un piano senza essere colpito: il danno deve salire di 0.5. Confermato con `stage`: danno da 3.50 a 4.00.
- [x] Le icone di Ho Rotto il Gioco, -1 al Dead God e Win Streak si vedono.
- [x] Prova il salvataggio dopo la correzione dei bonus:
  1. con -1 al Dead God già potenziato, esci con **Esc → Esci** e chiudi il gioco;
  2. riapri il gioco e rientra con **Continua**;
  3. controlla che il bonus ci sia ancora (nella run di prova: danno 3.70, velocità 1.03, gittata 9.10).
- [x] External Item Descriptions mostra la descrizione di Win Streak.
- [x] Controlla la descrizione di **Ho Rotto il Gioco** e di **-1 al Dead God**, compresa la "à" di "Velocità".
- [x] **"Unknown" nel menu di pausa** (riquadro Item Info del gioco): compare solo sugli oggetti della mod e resta anche dopo averli raccolti. È un limite noto: l'API Lua del gioco non offre un modo per identificarli. Le descrizioni complete si leggono con External Item Descriptions.
- [x] `giveitem Non Vi Rubo Altro Tempo`, poi usalo in una stanza con nemici: restano fermi per circa 3 secondi. Prova anche su un boss. Confermato sui nemici normali e sul boss.
- [x] `giveitem Potrebbe Stare Qua`, poi scendi di piano: le stanze segrete e super segrete si vedono sulla mappa e hai 2 bombe in più. Entrando in una compare **"Potrebbe stare qua!"**.
- [x] `giveitem Il Miracolo di San Gennaruzzo`, poi usa `goto s.angel.0` per entrare in una stanza dell'angelo: compare **"Il miracolo / di San Gennaruzzo!"** e appare un cuore eterno. Il comando `goto` crea una stanza speciale: se non scatta, prova con una stanza dell'angelo vera.
- [ ] Con lo stesso oggetto, scendi di qualche piano e controlla che le stanze dell'angelo compaiano più spesso. Letto nell'HUD con `stage` sui piani 3 e 4: angelo 0% senza l'oggetto, 100% con l'oggetto; 100% anche con Stats+ disattivata, quindi non è una sua stima. Non sono state contate stanze vere, e il 100% è più del +25% previsto dal codice: da capire perché, potrebbe essere troppo forte.
- [ ] `giveitem Che Fai, Te Ne Privi?`, poi finisci qualche stanza: circa una volta su quattro compare un pickup in più con **"Che fai? Te ne privi?"**. Scritta e pickup confermati (5 volte su 12 stanze); la frequenza non è misurata, perché forse c'erano due copie del trinket. Da codice è 25% per copia.
- [x] `giveitem La Mossa del Pro Player`, poi usalo: il danno sale di 2. Il bonus sparisce cambiando stanza. Riusalo e fatti colpire: il bonus sparisce e compare **"Sono un cretino"**, anche quando il colpo toglie un cuore intero.
- [x] Resta in una stanza con un boss vivo per 60 secondi: compare **"Non muore!"**, una volta sola. Controlla che il tempo sia giusto e che non scatti entrando in stanze senza boss. Con `goto s.boss.5271`: compare dopo circa 64 secondi e non si ripete fino a 150. In una stanza del tesoro non compare in 75 secondi.
- [x] `giveitem La Trollata`, poi usalo in una stanza con nemici: appare una troll bomb su ogni nemico. Controlla che le bombe restino addosso ai nemici abbastanza da colpirli.
- [x] `giveitem Fai Così, Fai Così`: una lacrima su due parte doppia. Controlla che la "ì" si veda bene nel nome e che il comando trovi l'oggetto; prova anche con un'arma che non spara lacrime (Brimstone), che non ha effetto. La "ì" è stata controllata in External Item Descriptions, il comando con l'id `c740`.
- [x] Usa Non Vi Rubo Altro Tempo, La Mossa del Pro Player, La Trollata e il D6: come nel gioco originale non deve comparire nessuna scritta. Il D6 è stato usato senza piedistalli da cambiare.
- [ ] `giveitem Mannaggia a Lui`, poi fatti colpire: il nemico più vicino subisce 4 volte il tuo danno e compare **"Mannaggia a lui!"**. Effetto e scritta confermati con il valore 10, che era troppo forte (Monstro è morto solo con i contatti): ricontrolla il bilanciamento con 4. Con 4 scritta e danno ci sono, ma il moltiplicatore non è misurato: c'erano altri danni nello stesso momento. Il bilanciamento resta da giudicare giocando.
- [x] Le icone degli altri cinque oggetti (Non Vi Rubo Altro Tempo, Potrebbe Stare Qua, Il Miracolo di San Gennaruzzo, Che Fai, Te Ne Privi?, La Mossa del Pro Player) si vedono e le loro descrizioni in External Item Descriptions sono giuste.
- [x] Le icone di La Trollata, Fai Così, Fai Così e Mannaggia a Lui si vedono.
- [ ] `giveitem Tacchinardi`, `giveitem Tacchinibus`, `giveitem Il Tacchino della Domenica`: ognuno dà i suoi cuori; al terzo compare **"SEI UN TACCHINO!"**, si sente il verso del tacchino e il danno sale di 1, la velocità scende di 0.1. Confermati cuori, scritta, danno (3.50 → 4.50) e velocità (1.00 → 0.90). Resta da sentire il verso.
- [x] Sempre al terzo oggetto la testa prende cresta, becco e bargigli. Controlla nelle 4 direzioni che siano allineati alla testa (si corregge con `COSTUME_Y` e `COSTUME_PARTS` in `tools/sprites.py`). Esci e continua la run: il costume deve esserci ancora, una sola volta. Con `remove` di uno dei tre oggetti sparisce.
- [x] `giveitem Sono un Idiota` e `giveitem Fermi Tutti`: compaiono *Sono un idiota!* e *Fermi tutti!*, e le statistiche non cambiano. Provati raccogliendoli dal piedistallo, perché `giveitem` non mostra le scritte al pickup.
- [x] Con Sono un Idiota compare il cono in testa, allineato nelle 4 direzioni (si corregge con `CONO_Y` in `tools/sprites.py`). C'è dopo il Continua; con `remove` dell'oggetto sparisce e con `giveitem` torna. Provato su un solo personaggio.
- [ ] **Modalità Greed:** fai una run Greed e controlla che gli oggetti della mod escano dai piedistalli (tesoro, boss, negozio, angelo). Hanno peso 0.5 perché le pool Greed sono più piccole: annota se escono troppo spesso o troppo poco.
- [ ] Le 16 icone hanno il contorno da 2px: guardale sul piedistallo e nell'HUD, e controlla che siano leggibili accanto agli oggetti vanilla. Fai attenzione al "-1" di -1 al Dead God e a Il Miracolo di San Gennaruzzo, che potrebbe sembrare una pozione, e al nuovo detonatore di La Trollata. Viste sui piedistalli: il contorno c'è, il "-1" si legge, San Gennaruzzo sembra un reliquiario e non una pozione, il detonatore si riconosce. Restano da guardare nell'HUD e da giudicare accanto ai vanilla: nella prova alcune erano sovrapposte tra loro, e il confronto con i vanilla non è stato fatto oggetto per oggetto. Controllo sui PNG: tutte 32x32, con pixel del colore del contorno e nessun pixel sul bordo dell'immagine; lo spessore di 2px non è misurato.

Facoltativo, se ci arrivi: The Beast deve mostrare **"IL BEASTY BOY"**, Mega Satan **"MEGA STANLEY KUBRICK"**, Peep **"PIPPOLINS"** (The Bloat invece niente). Battere un boss finale (Satan, The Lamb, Mother…) deve mostrare **"Un bacione grande / dal vostro Risacca"**.

## 4. Provare le rinomine

- [x] Il ResourceExtractor è stato lanciato: i file originali sono in `extracted_resources\`, nella cartella del gioco, e quelli che servono sono copiati in `extracted\`.
- [x] `resources-dlc3\` è stata generata e il gioco la carica.
- [x] `giveitem c17`: **Skeleton Chiaviz-Chiavoz**.
- [x] `giveitem c125`: **Bobby-Bombiz-Bomboz**.
- [x] `giveitem c360`: **Il buddy più forte del gioco**. Controlla che la "ù" si veda bene.
- [x] `giveitem c385`: **Bumbazzo**.
- [ ] `giveitem c249`, poi apri il riquadro Item Info nel menu di pausa: deve comparire **"Beppe Bossicchi drop 2 items"**. Se resta "Bosses drop 2 items", il gioco non sta caricando `info_display.xml` dalla mod. **Bug aperto:** resta "Bosses drop 2 items", anche se `resources-dlc3/info_display.xml` contiene il testo giusto e nessun'altra mod ha quel file. Provato anche in `resources/info_display.xml`, con gioco riavviato e sola Risacca attiva: resta il testo originale, quindi non è la soluzione (copia tolta).
- [ ] `giveitem c414`, stesso riquadro: **"1 additional item will appear in Stanza d'Auro"**. **Stesso bug:** resta "treasure rooms".
- [x] `giveitem c450`: **Come Cacchio Si Chiama**.
- [x] `giveitem c356`: **Non Si Sa Mai**.
- [x] `giveitem c247`: **Miglior Investimento**. Nome letto dai suggerimenti della console: `giveitem` non mostra il banner di raccolta.
- [x] `giveitem c232`: **Run Vinta**. Come sopra.
- [x] `giveitem k1`: **Col vostro permessico**. L'annunciatore continua a dire "The Fool": la voce non cambia con la rinomina.

- [x] Quando incontri Peep (piani Caves/Catacombs): la schermata VS mostra **PIPPOLINS** al posto del nome originale, leggibile e dentro lo schermo. Durante lo scorrimento il nome tocca il bordo destro, poi rientra: visto in una finestra quasi quadrata e con `goto s.boss.2020`.
- [ ] Quando incontri The Beast: se compare una schermata VS, deve mostrare **IL BEASTY BOY**. Il `bossportraits.xml` vanilla indica `BossName_TheBeast.png` per questo boss, ma il combattimento potrebbe comunque non aprire la schermata: in quel caso segnalalo e basta. La scritta **IL BEASTY BOY** è confermata con `spawn 951`; la schermata VS resta da vedere, perché `goto` non apre la stanza del boss.
- [x] Quando incontri Mega Satan: la schermata VS mostra **MEGA STANLEY**. Se per Peep o Mega Satan resta il nome originale, il gioco non sta usando il PNG della mod: dimmelo e provo a spostarlo in `resources-dlc3/`. Confermato con `goto s.boss.5000`; il banner in stanza dice **MEGA STANLEY KUBRICK**.
- [x] Quando incontri Bumbino: la schermata VS e la scritta mostrano **BUMBAZZO**. Confermato con `goto s.boss.5270`; nella schermata VS il nome arriva fino al bordo destro.
- [ ] Rivedi PIPPOLINS, MEGA STANLEY e BUMBAZZO nella schermata VS dopo il ridisegno delle lettere (#73): devono sembrare scritti come gli altri nomi e non toccare il bordo destro, con `goto s.boss.2020`, `goto s.boss.5000` e `goto s.boss.5270`. PIPPOLINS e BUMBAZZO vanno bene. **MEGA STANLEY arriva ancora al bordo destro** al massimo dello scorrimento (visto in una finestra quasi quadrata). Il PNG è largo 189 px, meno di nomi vanilla come Blighted Ovum (205) e Mask of Infamy (199): probabilmente non è un difetto della mod, ma non ho visto un vanilla sulla stessa schermata.

Le chiavi e le bombe raccolte da terra non cambiano nome: le rinomine riguardano solo nomi e descrizioni di oggetti, trinket, carte e pillole.

## Da inviarmi

1. **`log.txt`**, che si trova in `Documenti\My Games\Binding of Isaac Repentance+\log.txt`. Mandalo subito dopo aver giocato, senza riavviare il gioco.
2. **Gli screenshot delle scritte**, solo se qualcosa si vede male.
3. **Le caselle che non hai spuntato**: per ognuna scrivi una riga su cosa è successo.

Dopo queste prove prepariamo il caricamento privato sul Workshop.
