# Cosa fare sul PC Windows

Le caselle spuntate sono già confermate dai log, dal salvataggio della mod o dagli screenshot. Spunta le altre man mano e alla fine manda quello che è elencato nella sezione **Da inviarmi**.

Prima di provare, chiudi e riapri il gioco: le modifiche alla mod si vedono solo dopo il riavvio.

## 1. Installazione

- [x] La mod è in `C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\mods\risacca-mod\`, ed è la repo stessa: non serve estrarre lo zip.
- [x] La console di debug è attiva (`EnableDebugConsole=1` in `Documenti\My Games\Binding of Isaac Repentance+\options.ini`).
- [x] Il gioco carica la mod senza errori Lua.
- [ ] Installazione da zero seguendo solo il `readme.txt` dello zip (prima sposta altrove la cartella della repo): la mod compare nel menu **Mods** e si attiva. Controlla anche se la cartella `mods` esiste già e se Windows chiede l'autorizzazione a copiare.

## 2. Provare le scritte

Nuova run, con un personaggio qualsiasi:

- [x] All'inizio compare **"Ciao a tutti, io sono Risacca / Benvenuti sul mio canale"**.
- [ ] Poco dopo compare **"È XL?"**, poi **"No... non è XL"**. In un piano XL deve uscire **"SÌ, È XL!"**. Confermato "No... non è XL" (in un'unica scritta con "È XL?"); il caso del piano XL è ancora da vedere.
- [ ] **Controlla le lettere accentate:** guarda se "È" e "Ì" si vedono bene. Se vedi quadratini o lettere sbagliate, fai uno screenshot. "È" ed "è" si vedono bene; "Ì" è ancora da vedere.
- [x] Raccogli un oggetto di qualità 3 o 4: compare **"IL GODOR!"** o **"GODOR MAXIMOR!"**.
- [x] Prendi un oggetto con un patto col diavolo, pagandolo in cuori: compare **"Alla facciazza vostra!"**.
- [x] Prendi un colpo da un cuore intero: compare **"Tacchino!"**.
- [x] Scendi a mezzo cuore: compare **"C'ho l'ansia"**.
- [x] Muori: compare **"Beduins"**.

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
- [x] `giveitem Non Vi Rubo Altro Tempo`, poi usalo in una stanza con nemici: restano fermi per circa 3 secondi, compare **"Non vi rubo altro tempo"** e poi **"3, 2, 1... Ah no, aspetta"**. Prova anche su un boss. Confermato sui nemici normali e sul boss.
- [x] `giveitem Potrebbe Stare Qua`, poi scendi di piano: le stanze segrete e super segrete si vedono sulla mappa e hai 2 bombe in più. Entrando in una compare **"Potrebbe stare qua!"**.
- [x] `giveitem Il Miracolo di San Gennaruzzo`, poi usa `goto s.angel.0` per entrare in una stanza dell'angelo: compare **"Il miracolo / di San Gennaruzzo!"** e appare un cuore eterno. Il comando `goto` crea una stanza speciale: se non scatta, prova con una stanza dell'angelo vera.
- [ ] Con lo stesso oggetto, scendi di qualche piano e controlla che le stanze dell'angelo compaiano più spesso.
- [ ] `giveitem Che Fai, Te Ne Privi?`, poi finisci qualche stanza: circa una volta su quattro compare un pickup in più con **"Che fai? Te ne privi?"**. Scritta e pickup confermati (5 volte su 12 stanze); la frequenza non è misurata, perché forse c'erano due copie del trinket.
- [x] `giveitem La Mossa del Pro Player`, poi usalo: compare **"La mossa del pro player!"** e il danno sale di 2. Il bonus sparisce cambiando stanza. Riusalo e fatti colpire: il bonus sparisce e compare **"Sono un cretino"**, anche quando il colpo toglie un cuore intero.
- [ ] Resta in una stanza con un boss vivo per 60 secondi: compare **"Non muore!"**, una volta sola. Controlla che il tempo sia giusto e che non scatti entrando in stanze senza boss. Confermato dopo circa 64 secondi; "una volta sola" è verificato solo fino a circa 70 secondi e le stanze senza boss non sono state controllate apposta.
- [x] `giveitem c105`, poi usa il D6 su un piedistallo: l'oggetto cambia come sempre e compare **"Fammi sognare"**.
- [x] `giveitem La Trollata`, poi usalo in una stanza con nemici: appare una troll bomb su ogni nemico e compare **"M'ha trollato!"**. Controlla che le bombe restino addosso ai nemici abbastanza da colpirli.
- [x] `giveitem Fai Così, Fai Così`: una lacrima su due parte doppia. Controlla che la "ì" si veda bene nel nome e che il comando trovi l'oggetto; prova anche con un'arma che non spara lacrime (Brimstone), che non ha effetto. La "ì" è stata controllata in External Item Descriptions, il comando con l'id `c740`.
- [ ] `giveitem Mannaggia a Lui`, poi fatti colpire: il nemico più vicino subisce 10 volte il tuo danno e compare **"Mannaggia a lui!"**. Controlla il bilanciamento, soprattutto sui boss. Effetto e scritta confermati. Resta da decidere il bilanciamento: Monstro è morto solo con i contatti.
- [x] Le icone degli altri cinque oggetti (Non Vi Rubo Altro Tempo, Potrebbe Stare Qua, Il Miracolo di San Gennaruzzo, Che Fai, Te Ne Privi?, La Mossa del Pro Player) si vedono e le loro descrizioni in External Item Descriptions sono giuste.
- [x] Le icone di La Trollata, Fai Così, Fai Così e Mannaggia a Lui si vedono.
- [ ] `giveitem Tacchinardi`, `giveitem Tacchinibus`, `giveitem Il Tacchino della Domenica`: ognuno dà i suoi cuori; al terzo compare **"SEI UN TACCHINO!"** e il danno sale di 1, la velocità scende di 0.1.
- [ ] Le 14 icone hanno il contorno da 2px: guardale sul piedistallo e nell'HUD, e controlla che siano leggibili accanto agli oggetti vanilla. Fai attenzione al "-1" di -1 al Dead God e a Il Miracolo di San Gennaruzzo, che potrebbe sembrare una pozione.

Facoltativo, se ci arrivi: The Beast deve mostrare **"IL BEASTY BOY"**, Mega Satan **"MEGA STANLEY KUBRICK"**, Peep **"PIPPOLINS"** (The Bloat invece niente). Battere un boss finale (Satan, The Lamb, Mother…) deve mostrare **"Un bacione grande / dal vostro Risacca"**.

## 4. Provare le rinomine

- [x] Il ResourceExtractor è stato lanciato: i file originali sono in `extracted_resources\`, nella cartella del gioco, e quelli che servono sono copiati in `extracted\`.
- [x] `resources-dlc3\` è stata generata e il gioco la carica.
- [x] `giveitem c17`: **Skeleton Chiaviz-Chiavoz**.
- [x] `giveitem c125`: **Bobby-Bombiz-Bomboz**.
- [x] `giveitem c360`: **Il buddy più forte del gioco**. Controlla che la "ù" si veda bene.
- [x] `giveitem c385`: **Bumbazzo**.
- [ ] `giveitem c249`, poi apri il riquadro Item Info nel menu di pausa: deve comparire **"Beppe Bossicchi drop 2 items"**. Se resta "Bosses drop 2 items", il gioco non sta caricando `info_display.xml` dalla mod. **Bug aperto:** resta "Bosses drop 2 items", anche se `resources-dlc3/info_display.xml` contiene il testo giusto.
- [ ] `giveitem c414`, stesso riquadro: **"1 additional item will appear in Stanza d'Auro"**. **Stesso bug:** resta "treasure rooms".
- [x] `giveitem c450`: **Come Cacchio Si Chiama**.
- [x] `giveitem c356`: **Non Si Sa Mai**.
- [ ] `giveitem c247`: **Miglior Investimento**.
- [ ] `giveitem c232`: **Run Vinta**.
- [x] `giveitem k1`: **Col vostro permessico**. L'annunciatore continua a dire "The Fool": la voce non cambia con la rinomina.

- [x] Quando incontri Peep (piani Caves/Catacombs): la schermata VS mostra **PIPPOLINS** al posto del nome originale, leggibile e dentro lo schermo. Durante lo scorrimento il nome tocca il bordo destro, poi rientra: visto in una finestra quasi quadrata e con `goto s.boss.2020`.
- [ ] Quando incontri The Beast: se compare una schermata VS, deve mostrare **IL BEASTY BOY**. Il gioco non ha un'immagine del nome per questo boss, quindi è probabile che la schermata non ci sia: in quel caso segnalalo e basta.
- [x] Quando incontri Mega Satan: la schermata VS mostra **MEGA STANLEY**. Se per Peep o Mega Satan resta il nome originale, il gioco non sta usando il PNG della mod: dimmelo e provo a spostarlo in `resources-dlc3/`. Confermato con `goto s.boss.5000`; il banner in stanza dice **MEGA STANLEY KUBRICK**.
- [ ] Quando incontri Bumbino: la schermata VS e la scritta mostrano **BUMBAZZO**.
- [ ] Quando incontri Ultra Greed (modalità Greed): la schermata VS mostra **ULTRA BALLERINO DI FLAMENCO** su due righe, e la scritta lo stesso nome. Ultra Greedier usa la stessa immagine, quindi nella sua schermata VS comparirà questo nome: controlla che ti vada bene.
- [ ] Quando incontri il mini-boss Greed: compare la scritta **BALLERINO DI FLAMENCO**. Controlla anche il banner del mini-boss, che dovrebbe restare "Greed" perché viene dalla `stringtable.sta` e la mod non la genera.

Le chiavi e le bombe raccolte da terra non cambiano nome: le rinomine riguardano solo nomi e descrizioni di oggetti, trinket, carte e pillole.

## Da inviarmi

1. **`log.txt`**, che si trova in `Documenti\My Games\Binding of Isaac Repentance+\log.txt`. Mandalo subito dopo aver giocato, senza riavviare il gioco.
2. **Gli screenshot delle scritte**, solo se qualcosa si vede male.
3. **Le caselle che non hai spuntato**: per ognuna scrivi una riga su cosa è successo.

Dopo queste prove prepariamo il caricamento privato sul Workshop.
