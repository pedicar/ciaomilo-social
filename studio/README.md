# Studio Ciao Milo: come si creano i Reel

Motore per i Reel di Ciao Milo (ciaomilo.it, Instagram `ciaomilo.it`). Profilo **senza volto**: Milo è l'avatar e l'unico personaggio. Niente faccia, niente voce di Riccardo.

## Preparazione (una volta per sessione)

```bash
pip install numpy playwright --break-system-packages   # se mancano; Chromium è già installato
which ffmpeg                                           # serve ffmpeg
```

`reel2.py` usa `fonts/` e `img/` di questa cartella. Variabili facoltative: `MILO_OUT` (dove scrivere gli mp4, default `studio/out/`), `MILO_WORK` (file temporanei, default `/tmp/milo-work/`).

## Le serie

| Serie | Giorno, ora | Script di riferimento |
| --- | --- | --- |
| Chat dalla Francia | lunedì 12:30 | `episodi/nuovi.py` (chat-medico, chat-scuola), funzione `chat()` in `chat.py` |
| Il francese fonetico | sabato 12:30 | `episodi/fonetico.py`, `episodi/fonetico2.py` (funzione `episode()`) |
| Milo in 15 secondi | giovedì 12:30 | scene libere con `build()` di `reel2.py` |
| Milo risponde | domenica 12:30 | `episodi/milo_risponde.py spec.json` |

Ricetta fissa: gancio nel primo secondo, sigla 0,9 s, testo grande nelle zone sicure, suoni, 15–25 s, chiusura «Tocca a te» con domanda + consiglio di Milo che porta alla guida.

## Pubblicazione

1. Copiare l'mp4 in `reels/` e fare commit + push su `main`.
2. URL pubblico: `https://raw.githubusercontent.com/pedicar/ciaomilo-social/main/reels/<file>.mp4`
3. Metricool, brand `blogId` 6754005, sempre **bozza** (`draft: true`), Riccardo conferma:
   `{autoPublish:true, draft:true, descendants:[], media:[url], providers:[{network:"instagram"}], publicationDate:{dateTime:"AAAA-MM-GGT12:30:00", timezone:"Europe/Paris"}, text:<didascalia>, instagramData:{type:"REEL", showReelOnFeed:true}, videoCoverMilliseconds:1500}`

## Regole

- Solo fatti verificati su fonti ufficiali (service-public.fr, ameli.fr, caf.fr, consolati). Nel dubbio non si pubblica.
- Niente aneddoti personali inventati; niente marchi (chat «stile messaggi», senza logo); niente alcol.
- Prendere in giro le situazioni, mai le persone.
- Didascalie in italiano, prima persona di Milo, 3–5 hashtag (#italianiinfrancia #francia #ciaomilo …).
