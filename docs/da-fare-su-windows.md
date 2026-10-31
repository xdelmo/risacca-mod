# Cosa fare sul PC Windows

Ci vogliono circa 20 minuti. Spunta le caselle man mano. Alla fine mandami quello che è elencato nella sezione **Da inviarmi**.

## 1. Installare la mod

- [ ] Prendi `risacca-mod.zip`:
  - dal Mac copia il file `risacca-mod/dist/risacca-mod.zip`;
  - in alternativa, da GitHub scegli **Code → Download ZIP** e rinomina in `risacca-mod` la cartella che ottieni.
- [ ] Estrai lo zip in `C:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\mods\`. Alla fine deve esistere `mods\risacca-mod\metadata.xml`.
- [ ] Attiva la console di debug:
  1. apri `Documenti\My Games\Binding of Isaac Repentance\options.ini` (oppure `...Repentance+\` se hai Repentance+);
  2. imposta `EnableDebugConsole=1`;
  3. salva.
- [ ] Avvia il gioco, vai in **Mods** e controlla che **Risacca Mod** sia attiva.

## 2. Provare le scritte

Nuova run, con un personaggio qualsiasi:

- [ ] All'inizio compare **"Ciao a tutti, io sono Risacca / Benvenuti sul mio canale"**.
- [ ] Poco dopo compare **"È XL?"**, poi **"No... non è XL"**. In un piano XL deve uscire **"SÌ, È XL!"**.
- [ ] **Controlla le lettere accentate:** guarda se "È" e "Ì" si vedono bene. Se vedi quadratini o lettere sbagliate, fai una foto e segnalo.
- [ ] Raccogli un oggetto di qualità 3 o 4: compare **"GODOR!"** o **"GODOR MAXIMOR!"**.
- [ ] Prendi un oggetto con un patto col diavolo, pagandolo in cuori: compare **"Alla facciazza vostra!"**.
- [ ] Prendi un colpo da un cuore intero: compare **"Tacchino!"**.
- [ ] Scendi a mezzo cuore: compare **"C'ho l'ansia"**.
- [ ] Muori: compare **"Calmati babbuino"**.

## 3. Provare gli oggetti nuovi

Apri la console con il tasto `\` (quello sopra Invio, oppure `ò`/`ù` sulla tastiera italiana). Scrivi i comandi qui sotto. Puoi usare **Tab** per completare il nome dell'oggetto.

- [ ] `giveitem Ho Rotto il Gioco`, poi usa l'oggetto con la barra spaziatrice. Deve comparire un oggetto "glitchato".
- [ ] `giveitem -1 al Dead God`, poi uccidi un boss. Le statistiche (danno, velocità ecc.) devono salire un po'.
- [ ] `giveitem Win Streak`, poi finisci un piano senza essere colpito. Il danno deve salire.
- [ ] Controlla che le icone dei tre oggetti si vedano e non siano quadrati vuoti.
- [ ] Prova il salvataggio:
  1. con -1 al Dead God già potenziato, esci con **Esc → Esci**;
  2. rientra con **Continua**;
  3. controlla che il bonus ci sia ancora.

Facoltativo, se ci arrivi: The Beast deve mostrare **"IL BEASTY BOY"**, Mega Satan **"MEGA STANLEY KUBRICK"**. Battere un boss finale (Satan, The Lamb, Mother…) deve mostrare **"Un bacione grande / dal vostro Risacca"**.

## 4. Estrarre i file del gioco (per le rinomine)

- [ ] Nella cartella del gioco lancia `tools\ResourceExtractor\ResourceExtractor.exe` e aspetta che finisca. Ci vuole qualche minuto.
- [ ] Nelle cartelle `resources` e `resources-dlc3` del gioco, cerca i tre file da mandarmi (sono elencati qui sotto). Se un file è in tutte e due, prendi quello di `resources-dlc3`.

## Da inviarmi

1. **`log.txt`**, che si trova in `Documenti\My Games\Binding of Isaac Repentance\log.txt` (o `...Repentance+\`). Mandalo subito dopo aver giocato, senza riavviare il gioco.
2. **`items.xml`**.
3. **`pocketitems.xml`**.
4. **`stringtable.sta`**.
5. **Le foto delle scritte**, solo se qualcosa si vede male.
6. **Le caselle che non hai spuntato**: per ognuna scrivi una riga su cosa è successo.

Con questi file sistemo gli errori e genero le rinomine (Chiaviz-Chiavoz, Bumbazzo, Ballerino di Flamenco…). Poi prepariamo il caricamento privato sul Workshop.
