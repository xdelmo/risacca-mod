# Cosa fare sul PC Windows

Le caselle spuntate sono già confermate dai log, dal salvataggio della mod o dagli screenshot. Spunta le altre man mano e alla fine manda quello che è elencato nella sezione **Da inviarmi**.

Prima di provare, chiudi e riapri il gioco: le modifiche alla mod si vedono solo dopo il riavvio.

## 1. Installazione

- [x] La mod è in `C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\mods\risacca-mod\`, ed è la repo stessa: non serve estrarre lo zip.
- [x] La console di debug è attiva (`EnableDebugConsole=1` in `Documenti\My Games\Binding of Isaac Repentance+\options.ini`).
- [x] Il gioco carica la mod senza errori Lua.

## 2. Provare le scritte

Nuova run, con un personaggio qualsiasi:

- [ ] All'inizio compare **"Ciao a tutti, io sono Risacca / Benvenuti sul mio canale"**.
- [ ] Poco dopo compare **"È XL?"**, poi **"No... non è XL"**. In un piano XL deve uscire **"SÌ, È XL!"**.
- [ ] **Controlla le lettere accentate:** guarda se "È" e "Ì" si vedono bene. Se vedi quadratini o lettere sbagliate, fai uno screenshot.
- [ ] Raccogli un oggetto di qualità 3 o 4: compare **"IL GODOR!"** o **"GODOR MAXIMOR!"**.
- [ ] Prendi un oggetto con un patto col diavolo, pagandolo in cuori: compare **"Alla facciazza vostra!"**.
- [ ] Prendi un colpo da un cuore intero: compare **"Tacchino!"**.
- [ ] Scendi a mezzo cuore: compare **"C'ho l'ansia"**.
- [ ] Muori: compare **"Beduins"**.

## 3. Provare gli oggetti nuovi

Apri la console con il tasto `\` (quello sopra Invio, oppure `ò`/`ù` sulla tastiera italiana). Puoi usare **Tab** per completare il nome dell'oggetto.

- [x] `giveitem Ho Rotto il Gioco`, poi usa l'oggetto con la barra spaziatrice: compare un oggetto glitchato.
- [x] `giveitem -1 al Dead God`, poi uccidi un boss: le statistiche salgono (danno 3.50 → 3.70).
- [ ] `giveitem Win Streak`, poi finisci un piano senza essere colpito: il danno deve salire di 0.5. Il contatore funziona, ma l'aumento del danno non è stato ancora visto.
- [x] Le icone dei tre oggetti si vedono.
- [x] Prova il salvataggio dopo la correzione dei bonus:
  1. con -1 al Dead God già potenziato, esci con **Esc → Esci** e chiudi il gioco;
  2. riapri il gioco e rientra con **Continua**;
  3. controlla che il bonus ci sia ancora (nella run di prova: danno 3.70, velocità 1.03, gittata 9.10).
- [x] External Item Descriptions mostra la descrizione di Win Streak.
- [ ] Controlla la descrizione di **Ho Rotto il Gioco** e di **-1 al Dead God**, compresa la "à" di "Velocità".
- [x] **"Unknown" nel menu di pausa** (riquadro Item Info del gioco): compare solo sugli oggetti della mod e resta anche dopo averli raccolti. È un limite noto: l'API Lua del gioco non offre un modo per identificarli. Le descrizioni complete si leggono con External Item Descriptions.

Facoltativo, se ci arrivi: The Beast deve mostrare **"IL BEASTY BOY"**, Mega Satan **"MEGA STANLEY KUBRICK"**. Battere un boss finale (Satan, The Lamb, Mother…) deve mostrare **"Un bacione grande / dal vostro Risacca"**.

## 4. Provare le rinomine

- [x] Il ResourceExtractor è stato lanciato: i file originali sono in `extracted_resources\`, nella cartella del gioco, e quelli che servono sono copiati in `extracted\`.
- [x] `resources-dlc3\` è stata generata e il gioco la carica.
- [x] `giveitem c17`: **Skeleton Chiaviz-Chiavoz**.
- [ ] `giveitem c125`: **Bobby-Bombiz-Bomboz**.
- [ ] `giveitem c360`: **Il buddy più forte del gioco**. Controlla che la "ù" si veda bene.
- [ ] `giveitem c385`: **Bumbazzo**.

Le chiavi e le bombe raccolte da terra non cambiano nome: le rinomine riguardano solo nomi e descrizioni di oggetti, trinket, carte e pillole.

## Da inviarmi

1. **`log.txt`**, che si trova in `Documenti\My Games\Binding of Isaac Repentance+\log.txt`. Mandalo subito dopo aver giocato, senza riavviare il gioco.
2. **Gli screenshot delle scritte**, solo se qualcosa si vede male.
3. **Le caselle che non hai spuntato**: per ognuna scrivi una riga su cosa è successo.

Dopo queste prove prepariamo il caricamento privato sul Workshop.
