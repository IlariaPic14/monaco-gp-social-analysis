# Ingestion Section

Questa cartella contiene gli script per raccogliere dati da diverse piattaforme social (YouTube, Reddit, Instagram, ecc.) relativi al Gran Premio di Monaco 2025. Ogni modulo salva i commenti in formato JSON all'interno della cartella `data/`, strutturati secondo lo schema del dataset unificato.

---

##  YouTube – `youtube_ingestion.py`

### Descrizione
Estrae commenti da video pubblici di YouTube relativi al GP di Monaco, utilizzando query di ricerca e salvataggio incrementale dei risultati. I commenti vengono arricchiti con metadati coerenti con lo schema standard del dataset.

### Dipendenze
- [`youtube_comment_downloader`](https://pypi.org/project/youtube-comment-downloader/)
- [`youtube-search-python`](https://pypi.org/project/youtube-search-python/)

### File coinvolti
- `youtube_ingestion.py` (in `src/ingestion`)
- `youtube_search.py` (in `src/utils`)

### Come funziona
1. Esegue una ricerca video su YouTube (default: `"Monaco GP 2025"`).
2. Estrae i primi 50 video con `youtube-search-python`.
3. Per ogni video, scarica fino a 100 commenti.
4. I commenti vengono formattati secondo lo schema richiesto e salvati in JSON.
5. I nuovi commenti vengono aggiunti solo se non duplicati (basati su `content_id`).

### Esecuzione
```bash
python src/ingestion/youtube_ingestion.py


## Reddit – `reddit_praw_ingestion.py`

### Descrizione
Estrae commenti da post pubblici del subreddit `r/formula1` in base a una query di ricerca, utilizzando le API ufficiali di Reddit via `PRAW`. I commenti vengono salvati in formato JSON, conformi allo schema del dataset.

### Dipendenze
- [`praw`](https://pypi.org/project/praw/)

### File coinvolti
- `reddit_praw_ingestion.py` (in `src/ingestion`)
- `config.py` (in `src/utils`)
- `reddit_login.py` (in `src/utils` – facoltativo, per generare manualmente il refresh token)

### Come funziona
1. Cerca i post su Reddit con la query `"Monaco GP 2025"` nel subreddit `r/formula1`.
2. Estrae i commenti da ciascun post (ignora risposte a commenti nidificati).
3. Converte ogni commento in una struttura coerente con lo schema del progetto.
4. Salva i dati in `data/reddit_monaco_gp.json`, evitando duplicati tramite `content_id`.

### Esecuzione
```bash
python src/ingestion/reddit_praw_ingestion.py

## 📸 Instagram – `instagram_profiles_scraper.py`

### Descrizione
Estrae i **post pubblici** da un elenco di profili Instagram ufficiali (es. `@f1`, `@scuderiaferrari`, ecc.) tramite la libreria `instaloader`, utilizzando un file di cookie precedentemente salvato per bypassare il login interattivo. I post vengono formattati secondo lo schema del dataset e salvati in formato JSON.

### Dipendenze
- [`instaloader`](https://pypi.org/project/instaloader/)
- [`selenium`](https://pypi.org/project/selenium/) (per la generazione dei cookie)

### File coinvolti
- `instagram_profiles_scraper.py` (in `src/ingestion`)
- `instagram_manual_cookie_login.py` (in `src/utils`)
- `instagram_cookies_scraper.json` (generato automaticamente)

---

### Come funziona
1. Accede a ciascun profilo Instagram nella lista `profile_names`.
2. Scarica i post più recenti (default: 5 per profilo).
3. Estrae metadati.
4. Unisce i post a quelli già presenti, evitando duplicati (`content_id`).
5. Salva tutto in `data/instagram_multi_profiles.json`.

---

### Esecuzione
```bash
python src/ingestion/instagram_profiles_scraper.py


## 🖱️ Instagram (GUI) – `interactive_gui_comment_scraper.py`

### Descrizione
Questo script consente di **estrarre manualmente i commenti da post Instagram** visitati tramite browser. Dopo aver caricato i cookie utente per accedere a Instagram, l’interfaccia GUI ti permette di:

- Navigare su un post Instagram dal browser aperto automaticamente
- Cliccare “Estrai Commenti” per analizzare la pagina corrente
- Salvare i commenti validi in formato JSON

È utile per l’estrazione semi-automatica da post specifici, non gestibili via API o `instaloader`.

---

### Dipendenze
- [`selenium`](https://pypi.org/project/selenium/)
- [`tkinter`](https://docs.python.org/3/library/tkinter.html) *(incluso in Python standard)*
- `chromedriver` installato e configurato

---

### File coinvolti
- `interactive_gui_comment_scraper.py` (in `src/ingestion`)
- `instagram_cookies_scraper.json` (in `src/utils` o `root`, generato manualmente)

---

### Funzionamento
1. Apre una finestra di Chrome e carica Instagram con i cookie salvati.
2. L’utente **naviga manualmente su un post pubblico**.
3. Nella GUI, clicca “Estrai Commenti e Salva”.
4. Lo script individua e salva i commenti visibili con metadati coerenti con il dataset.

---

### Esecuzione
```bash
python src/ingestion/interactive_gui_comment_scraper.py

##  TikTok – Ingestion via strumenti esterni (Make.com + Actor)

### Descrizione
A differenza delle altre piattaforme, l’ingestion dei dati da TikTok **non è avvenuta tramite script Python**, ma sfruttando servizi esterni per uno scraping affidabile ed efficiente. Questo approccio ha permesso di superare le limitazioni tecniche imposte da TikTok alle API pubbliche.

---

###  Metodo utilizzato

1. **TikTok Data Extractor Actor**  
   È stato utilizzato un actor (strumento cloud-based per scraping) per estrarre:
   - Commenti
   - Contenuti dei video
   - Metadati pubblici associati

2. **Make.com**  
   Una volta estratti, i dati sono stati integrati automaticamente su **Google Sheets** usando Make (ex Integromat), per facilitarne:
   - La visualizzazione
   - La validazione manuale
   - L’esportazione in CSV

3. **Conversione finale**  
   I dati in Google Sheets sono stati esportati in un file CSV conforme allo schema del progetto e salvati in:



