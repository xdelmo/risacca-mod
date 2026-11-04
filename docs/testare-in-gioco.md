# Testare la mod a gioco aperto (guida per agenti)

Vale per qualsiasi agente (Claude Code, Antigravity, ...) che giri sul PC Windows dove è installato il gioco. Le prove da fare sono in `docs/da-fare-su-windows.md`: aggiornalo dopo ogni prova.

## Prerequisiti

- Il gioco è aperto dall'utente e la mod è attiva.
- La finestra del gioco deve restare in primo piano: l'input arriva solo lì. Se l'utente cambia finestra, si apre il menu di pausa. `run.ps1` si ferma con codice di uscita 2.
- L'input è reale: non scrivere mentre l'utente sta usando il PC, e avvisalo prima di iniziare.

## Script (`tools/gioco/`, da PowerShell)

| Script | Uso |
| --- | --- |
| `run.ps1 -Name x [-Thaw] [-Commands 'a','b'] [-Keys 57] [-HoldMs 80] [-FirstMs 150] [-Shots 3] [-EveryMs 700] [-Freeze]` | Esegue i comandi in console, preme i tasti, salva `x-N.png` |
| `sheet.ps1 -Name x -Count n -Out x.png` | Unisce gli scatti in un foglio |
| `wait.ps1 -Seconds 45` | Aspetta che il gioco torni in primo piano |
| `. .\peek.ps1 -Texts 'giveitem c73' -Name p` | Fotografa i suggerimenti della console, senza Invio: mostra i nomi veri |

Gli screenshot finiscono in `tools/gioco/` e sono ignorati da git. Vanno guardati: sono l'unico riscontro.

## Input

- Tasti a scancode con `SendInput`, perché il gioco ignora i virtual key: console `0x29`, Invio `0x1C` (28), Esc `0x01` (1), Backspace `0x0E` (14), spazio `0x39` (57), D `0x20`. Il testo passa da `KEYEVENTF_UNICODE`.
- `-Keys` vuole numeri decimali.

## Comportamenti del gioco da conoscere

- Il gioco gira in tempo reale tra un comando dell'agente e l'altro, e i nemici possono uccidere Isaac. Chiudi ogni raffica con `-Freeze`, che lascia aperta la console e quindi mette in pausa.
- Riprendi con `-Thaw` **solo se la console è davvero aperta**: `-Thaw` preme Esc, e senza console aperta Esc apre il menu di pausa. Con il menu aperto lo spazio seleziona solo "Resume Game" e i comandi non vanno a buon fine.
- Dopo Invio la console resta aperta. `run.ps1` la chiude con Esc dopo ogni comando.
- Esc sulla schermata di morte torna al menu; spazio lì riavvia la run.
- Lo spazio a volte viene ignorato subito dopo `giveitem`: aspetta almeno 800 ms e tieni premuto 300-400 ms (`-FirstMs 800 -HoldMs 400`) prima di dichiarare un bug.
- Un foglio bianco o uno script fermato per il focus non sono un risultato di prova.
- Prima di giudicare una prova, controlla negli scatti che il comando abbia avuto effetto: l'icona dell'oggetto attivo è cambiata? la stanza è quella giusta? è aperto un menu?

## Comandi di console utili

- `giveitem c735` oggetto, `giveitem t191` trinket, `spawn 5.100.1` piedistallo con oggetto, `goto s.angel.0` stanza speciale, `restart` nuova run, `debug 3` invulnerabilità (si disattiva ripetendolo).
- Id attuali: Non Vi Rubo c735, Mossa c736, Potrebbe Stare Qua c737, San Gennaruzzo c738, Trollata c739, Fai Così c740, Che Fai t191, Mannaggia t192. Gli id possono cambiare se si aggiungono oggetti: verificali con `peek.ps1`.
- Con `debug 3` attivo non scattano le prove sui colpi subiti (Tacchino, Sono un cretino, Mannaggia a Lui, C'ho l'ansia).

## Effetti collaterali

- Morire e ricominciare può cambiare le statistiche del profilo dell'utente, come la Win Streak nella selezione personaggio. Con `debug 3` si evita. Segnala all'utente ogni morte di prova.
- Non chiudere il gioco e non modificare i salvataggi senza chiedere.
- La mod gira dalla cartella `...\mods\risacca-mod\`: le modifiche in un worktree non sono caricate dal gioco finché non arrivano lì.
- Il log è `Documents\My Games\Binding of Isaac Repentance+\log.txt`: cercaci gli errori Lua dopo ogni prova.

## Cosa non si può verificare così

L'audio, il feeling e il bilanciamento, e la leggibilità per un giocatore: lasciali all'utente.
