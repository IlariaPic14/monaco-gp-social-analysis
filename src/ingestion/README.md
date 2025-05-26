# Ingestion Section

Questa cartella contiene gli script per raccogliere, unificare e pulire i dati provenienti da diverse piattaforme social (YouTube, Reddit, Instagram, TikTok) relativi al Gran Premio di Monaco 2025. Ogni modulo salva i commenti in formato JSON o CSV nella cartella `data/`, strutturati secondo lo schema del dataset unificato.

---

## YouTube – `youtube_ingestion.py`

### Descrizione
Estrae commenti da video pubblici di YouTube relativi al GP di Monaco, utilizzando query di ricerca e salvataggio incrementale dei risultati.

### Dipendenze
- `youtube-comment-downloader`
- `youtube-search-python`

### File coinvolti
- `src/ingestion/youtube_ingestion.py`
- `src/utils/youtube_search.py`

---

## Reddit – `reddit_praw_ingestion.py`

### Descrizione
Estrae commenti da post pubblici del subreddit `r/formula1` usando le API ufficiali di Reddit (`PRAW`). I risultati sono salvati in formato JSON conforme allo schema standard.

### Dipendenze
- `praw`

### File coinvolti
- `src/ingestion/reddit_praw_ingestion.py`
- `src/utils/config.py`
- `src/utils/reddit_login.py` (facoltativo)

---

## Instagram (profili) – `instagram_profiles_scraper.py`

### Descrizione
Estrae post pubblici da profili Instagram ufficiali tramite `instaloader`, con autenticazione via cookie.

### Dipendenze
- `instaloader`
- `selenium`

### File coinvolti
- `src/ingestion/instagram_profiles_scraper.py`
- `src/utils/instagram_manual_cookie_login.py`
- `instagram_cookies_scraper.json`

---

## Instagram (GUI manuale) – `interactive_gui_comment_scraper.py`

### Descrizione
Permette di estrarre manualmente i commenti da post Instagram pubblici tramite un’interfaccia grafica (GUI) che sfrutta Selenium e Tkinter.

### Dipendenze
- `selenium`
- `tkinter` (incluso in Python)
- `chromedriver` installato

### File coinvolti
- `src/ingestion/interactive_gui_comment_scraper.py`
- `instagram_cookies_scraper.json`

---

## TikTok – Ingestion via strumenti esterni (Make.com + Actor)

### Descrizione
L'ingestion da TikTok è stata effettuata usando strumenti esterni (es. Apify Actor + Make.com). I dati sono stati esportati in Google Sheets, validati e poi salvati in formato CSV conforme.

---

## Merge e Normalizzazione – `merge_and_clean.py`

### Descrizione
Unisce i dati raccolti da tutte le piattaforme in un unico dataset CSV (`f1_social_dataset.csv`), applicando uno schema coerente, completamento dei campi mancanti e filtraggio per l’anno 2025.

### Dipendenze
- `pandas`
- `json`

### File coinvolti
- `merge_and_clean.py`
- Input JSON/CSV:  
  - `data/gui_extracted_comments.json`  
  - `data/instagram_multi_profiles.json`  
  - `data/youtube_monaco_gp.json`  
  - `data/reddit_monaco_gp.json`  
  - `data/tiktok_ingestion.csv`  
- Output: `data/f1_social_dataset.csv`

---

## Preprocessing Testuale e Linguistico – `preprocessing.py`

### Descrizione
Applica la rilevazione della lingua e pulizia del testo (rimozione emoji, punteggiatura, link, stemming, stopword) per ogni commento. Il testo pulito viene salvato nella colonna `text_clean`.

### Dipendenze
- `pandas`
- `nltk`
- `re`
- `src/utils/language_detection.py`

### File coinvolti
- `preprocessing.py`
- Output: `data/f1_social_clean.csv` (con colonne `language` e `text_clean`)

---

## Esecuzione degli Script

Tutti gli script devono essere eseguiti dalla **root del progetto**.

```bash
# YouTube
python src/ingestion/youtube_ingestion.py

# Reddit
python src/ingestion/reddit_praw_ingestion.py

# Instagram – profili ufficiali
python src/ingestion/instagram_profiles_scraper.py

# Instagram – scraping manuale via GUI
python src/ingestion/interactive_gui_comment_scraper.py

# Merge dei file raccolti e normalizzazione
python merge_and_clean.py

# Preprocessing del testo + rilevazione lingua
python preprocessing.py
