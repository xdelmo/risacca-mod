# Standard Grafici e Pixel Art per The Binding of Isaac: Repentance+

Guida di riferimento per la creazione e revisione degli sprite custom della mod `risacca-mod`.

---

## 1. Filosofia Visiva di Repentance+

Lo stile grafico di The Binding of Isaac (in particolare da *Repentance* e *Repentance+*) è un pixel-art moderno a 16-bit con un'identità precisa definita da Edmund McMillen e dal team artistico:
- **Forme corpulente e solide:** Gli oggetti hanno volume, peso e tridimensionalità. Non devono apparire come icone vettoriali stilizzate o piatte, ma come artefatti tangibili posati su un piedistallo o tenuti in mano.
- **Tonalità grottesca/vintage/sacra:** L'universo di Isaac unisce iconografia biblica, reliquie religiose, orrore corporale, frammenti anatomici e giocattoli/oggetti retrò consumati.
- **Leggibilità istantanea a 1x:** Il giocatore deve capire all'istante la silhouette e il materiale dell'oggetto mentre cammina velocemente nella Treasure Room o nel Devil Deal.

---

## 2. Dimensioni e Proporzioni (Canvas 32x32)

Tutti i collezionabili e i trinket del gioco sono salvati come immagini PNG `32x32` con canale alfa (trasparenza).

### Collezionabili (Attivi e Passivi su piedistallo)
- **Ingombro ideale:** tra **20x20 px** e **26x26 px** (inclusi i contorni).
- **Margine di sicurezza:** lasciare almeno 2-4 pixel trasparenti dai bordi del canvas (non toccare mai il bordo 0 o 31 se non per casi eccezionali come fiamme o punte sottili).
- **Presenza su piedistallo:** il piedistallo di Isaac è largo 32px. Uno sprite più piccolo di 18x18 px scompare visivamente, sembrando una pillola o un micro-consumabile anziché un oggetto primario.

### Trinket (Ninnoli)
- **Ingombro tipico:** mediana **20x20 px**, dal 10° al 90° percentile tra **16x15 px** e **25x25 px** (misurato su 128 trinket vanilla).
- Le dimensioni sono quasi le stesse dei collezionabili: si distinguono per il soggetto (monete, pezzi di carta, ossa, spille, vermi, medaglie), non per la taglia.

### Valori misurati sui PNG vanilla
Misure su 548 collezionabili e 128 trinket estratti col ResourceExtractor dalla versione Afterbirth+ per macOS. La tavola di Repentance (724 oggetti) dà valori quasi uguali.

| Misura | 10° percentile | Mediana | 90° percentile |
|---|---|---|---|
| Colori per sprite | 3 | 5 | 9 |
| Pixel scuri sul totale | 38% | 51% | 66% |
| Pixel opachi (collezionabili) | 179 | 283 | 413 |

---

## 3. Contorni e Lineart (L'Outline di Isaac)

Il contorno è l'elemento più caratteristico dello stile grafico del gioco.

1. **Spessore:** **2 pixel** attorno a tutta la silhouette esterna. Ce l'hanno 493 collezionabili vanilla su 548 e 116 trinket su 128; solo 30 oggetti in tutto restano a 1 pixel.
2. **Colore contorno esterno:** `PALETTE["K"] = (8, 0, 0)` (`#080000`), non il nero puro `#000000`. È il colore del bordo in 443 collezionabili vanilla su 548.
3. **Algoritmo di contorno a 4 vicini (Manhattan):**  
   In `tools/sprites.py`, `outline()` aggiunge uno strato di contorno verificando i 4 vicini cardinali (su, giù, sinistra, destra), e `render()` la chiama due volte.
   - **Ogni lato cresce di 2 pixel:** le griglie vanno disegnate sui 16-20 pixel, così lo sprite finito sta sui 20-24.
   - **Gli spazi stretti si chiudono:** uno spazio largo fino a 4 pixel tra due parti diventa tutto nero. È utile per separare parti come campanelle e corpo della sveglia, o i manici della coppa.
   - **I dettagli sottili ingrassano:** una linea da 1 pixel, come una miccia, diventa larga 5 pixel. Vanno tenuti corti.
4. **Bordi interni e simboli (Engravings & Features):**  
   - Per sfumature interne di volume si usano i toni scuri del materiale stesso (`b` per l'oro, `m`/`d` per il ferro, `r` per il sangue, `u` per le ossa).
   - Per elementi grafici chiave che devono essere leggibili all'istante a risoluzione 1x (es. le lancette dell'orologio, il punto interrogativo `?` inciso sulla moneta, crepe e tratti facciali), l'originale usa tratti decisi nel colore contorno `K` (`#080000`), garantendo massima riconoscibilità senza impastare l'icona.

---

## 4. Luce, Ombre e Palette (Cluster Shading)

### Direzione della luce
- La fonte di luce principale proviene sempre da **in alto a sinistra (Top-Left)**.
- Il punto di massima luce e i riflessi speculari stanno in alto a sinistra; le ombre piene e i sottosquadri si concentrano in basso a destra.

### Niente Pillow Shading
- **Errore comune:** scurire concentricamente tutti i bordi dell'oggetto verso il centro.
- **Regola:** la luce crea bande decise e cluster compatti. Il lato sinistro/superiore riceve la luce piena; il lato destro/inferiore raccoglie l'ombra.

### Hue Shifting obbligatorio
Nei giochi retrò ben disegnati e in Isaac, quando un colore diventa più scuro o più chiaro **non si cambia solo la luminosità**, si ruota la tonalità:
- **Verso la luce (Highlight):** vira verso il giallo/oro caldo (tonalità calde).
- **Verso l'ombra (Shadow):** vira verso il bronzo antico, il violaceo o il bluastro freddo.

### Specular Highlights (`W`)
- Punti luce bianchi puri (`W` = `#FFFFFF`) di 1-3 pixel posizionati nei punti di tangenza della luce su materiali lucidi:
  - Vetro di fiale e orologi.
  - Metallo riflettente o monete d'oro.
  - Liquidi e occhi.

### No Dithering a scacchiera
- Isaac Repentance non usa texture a scacchiera (checkerboard dithering tipo Commodore 64).
- Usa transizioni a gradini netti (cel-shading a blocchi) con 3-5 tonalità per materiale.

---

## 5. Ricettario dei Materiali

| Materiale | Colori Palette (`tools/sprites.py`) | Caratteristiche visive |
|---|---|---|
| **Oro / Metallo sacro** | `L` (oro chiaro speculare), `Y` (oro brillante), `y` (oro caldo), `b` (bronzo scuro) | Bordo superiore brillante, ghiera sfaccettata, sottosquadro bronzo profondo. |
| **Ferro / Acciaio (Bombe)** | `w` (luce plastica/ferro), `g` (grigio chiaro), `m` (grigio medio), `d` (ombra scanalature), `n` (ombra fredda) | Riflesso curvo sferico in alto a sinistra, fondo freddo bluastro. |
| **Vetro trasparente** | `w` (luce vetro), `W` (riflesso speculare), `g`, `m` | Fascia diagonale bianca/chiara di riflesso speculare che attraversa la superficie. |
| **Sangue e Liquidi sacri** | `l` (riflesso vermiglio chiaro), `R` (rosso sangue vivo), `r` (sangue scuro coagulato) | Stratificazione orizzontale con menisco, coagulo più denso sul fondo. |
| **Parchment / Avorio / Ossa** | `t` (avorio chiaro), `s` (osso medio), `u` (ombra fessura) | Tonalità calde leggermente ingiallite, cavità in `K` e tacche in `u`. |
| **Fiamma viva** | `W`/`L` (nucleo caldissimo), `O` (arancione vivo intermedio), `F` (rosso esterno) | Strati concentrici dal centro chiaro alla periferia scarlatta. |
| **Monete 3D** | `WW` (luce speculare), `LL`/`YY` (superficie), `y`/`b` (bordo inferiore) | Prospettiva inclinata: il bordo inferiore mostra lo spessore e la coniatura. Simboli interni incisi con ombra sotto e luce sopra. |

---

## 6. Checklist di Revisione per Nuovi Sprite

Prima di confermare un nuovo sprite, verificare:

- [ ] Lo sprite è centrato nel riquadro 32x32 con almeno 2px di respiro dai bordi?
- [ ] L'ingombro è proporzionato (lato massimo 26px, mediana vanilla attorno ai 20px)?
- [ ] Lo sprite usa al massimo 9 colori, contorno compreso?
- [ ] La silhouette è leggibile a colpo d'occhio senza dover zoomare al 400%?
- [ ] Il contorno esterno è da 2px in `(8, 0, 0)` senza pixel sparsi o buchi accidentali?
- [ ] La direzione della luce è coerente (dall'alto a sinistra verso il basso a destra)?
- [ ] Sono presenti i punti luce speculari (`W`) dove opportuno (vetro, metallo)?
- [ ] I simboli interni (numeri, punti interrogativi, crepe) sono leggibili a risoluzione 1x?
- [ ] `python3 tools/sprites.py --selftest` viene superato senza errori?
- [ ] Il confronto visivo in `docs/preview.png` risulta armonico con gli altri oggetti ufficiali?
- [ ] È stato fatto un confronto diretto con gli item vanilla simili presenti nello spritesheet di reference ufficiale (`docs/PC _ Computer - The Binding of Isaac_ Rebirth - Items - Items (Repentance).png`)?
- [ ] `python3 tools/leggibilita.py` non segna l'icona `DA RIVEDERE`?
- [ ] In `dist/leggibilita.png` l'icona si capisce a 1x e il simbolo si vede ancora nella colonna in grigi?
- [ ] Coprendo il nome, si capisce di quale oggetto si tratta e lo si distingue dagli altri della mod?

---

## 7. Come Creare un'Icona Nuova

1. **Scegli un'idea sola.** L'icona mostra un oggetto concreto che richiama il tormentone. Le scritte non servono: a 32x32 non si leggono, al massimo un numero o un simbolo di 1-2 caratteri.
2. **Cerca una forma libera.** Controlla la tavola di riferimento e le icone della mod: se la forma è già presa, cambiala. Un dettaglio interno diverso non basta: `la_trollata` e `potrebbe_stare_qua` sono la stessa bomba con una faccia o un `?`, e a 1x si confondono.
3. **Disegna prima la silhouette.** Riempila con un colore solo nella griglia di `SPRITES` (16-20 pixel per lato, il contorno ne aggiunge 2 per parte). Se così non si riconosce, nessun dettaglio la salverà.
4. **Assegna una tinta dominante.** Sceglila dal ricettario della sezione 5, diversa da quella delle icone con forma simile.
5. **Aggiungi volume e un solo dettaglio chiave.** Luce in alto a sinistra e ombra in basso a destra. Il dettaglio chiave deve differire dallo sfondo per luminosità, non solo per tinta: il rosso sulla pelle sparisce in grigi.
6. **Rigenera e controlla:**

   ```bash
   python3 tools/sprites.py --selftest   # regole tecniche: formato, margini, ingombro, colori, contorno
   python3 tools/sprites.py              # rigenera i PNG
   python3 tools/leggibilita.py          # sosia nella mod e tra i vanilla, più dist/leggibilita.png
   ```

7. **Guarda la tavola, poi prova in gioco.** I numeri non dicono se un'icona si capisce: decide l'occhio, a 1x, e poi la prova su piedistallo e HUD.

### Come leggere `tools/leggibilita.py`

- **Colonne della tavola:** 1x e 2x su HUD, 1x e 2x su piedistallo, 2x in grigi, sosia vanilla a 2x.
- **Punteggio:** va da 0 a 1 e misura quanto si sovrappongono le forme centrate, ridotto dalla differenza di colore. Non vede il significato dell'oggetto.
- **`DA RIVEDERE`:** compare da 0,7 con un'icona della mod e da 0,8 con un oggetto vanilla, e lo script esce con 1. È un motivo per guardare la coppia, non un verdetto: anche tra i vanilla ci sono famiglie volutamente simili. Se la somiglianza è voluta, lascia l'icona com'è e scrivi il motivo nella PR.
- **Riferimento vanilla:** la tavola non ha i nomi degli oggetti, quindi il report indica riga e colonna della cella. Il confronto vale solo per gli oggetti presenti nel foglio.

---

## 8. Workflow nel Repository

Gli sprite della mod **non si disegnano né modificano mai manualmente nei file PNG**.
Vengono compilati via codice da matrici di caratteri in `tools/sprites.py`:

```bash
# 1. Modifica la matrice in tools/sprites.py
# 2. Esegui il selftest automatico (formato, margini, ingombro, numero di colori, contorno da 2px)
python3 tools/sprites.py --selftest

# 3. Rigenera tutti i file PNG in resources/ e aggiorna docs/preview.png
python3 tools/sprites.py

# 4. Apri docs/preview.png per controllare il risultato a 8x affiancato
```

---

## 9. Tavola di Riferimento Visivo Ufficiale

Nella cartella `docs/` è presente il foglio completo (spritesheet) ad alta fedeltà con tutti gli oggetti ufficiali di Repentance, da usare come benchmark costante e fonte di verità visiva per silhouette, shading, palette e spessore dei contorni:

- **File di riferimento:** [`docs/PC _ Computer - The Binding of Isaac_ Rebirth - Items - Items (Repentance).png`]().png)

Quando si progetta o si revisiona un oggetto custom, fare riferimento agli item ufficiali analoghi presenti nello spritesheet:
- **Orologi e strumenti meccanici:** confrontare con *Broken Watch*, *Stop Watch*, *Glowing Hourglass*.
- **Bombe speciali:** confrontare con *Sad Bombs*, *Bobby-Bomb*, *Hot Bombs*, *Blood Bombs*, *Glitter Bombs*.
- **Ampolle, fiaschette e reliquie sacre:** confrontare con *Holy Water*, *The Relic*, *Jar of Flies*, *Blood of the Martyr*, *Eucharist*.
- **Monete e gettoni (Trinket):** confrontare con *Counterfeit Penny*, *Lucky Penny*, *Pay to Play*, *Store Key*, *Silver Dollar*.
