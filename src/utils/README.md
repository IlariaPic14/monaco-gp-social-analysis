#  Utils Section

Questa cartella raccoglie moduli di supporto utilizzati nei processi di scraping, autenticazione, elaborazione linguistica e clustering dei commenti.  
Ogni modulo è pensato per essere **riutilizzabile** e **modulare**, e viene importato da altri script nelle cartelle `ingestion/` e  `sentiment/` 

---

##  Reddit Auth – `config.py` & `reddit_login.py`

### Descrizione
Questi file gestiscono l’autenticazione alle API di Reddit tramite [PRAW](https://pypi.org/project/praw/).  
La configurazione è separata per motivi di sicurezza e riusabilità.

---

###  File coinvolti

| File              | Funzione                                                                 |
|-------------------|--------------------------------------------------------------------------|
| `config.py`       | Contiene le credenziali API Reddit. Deve essere compilato a partire dal template fornito. |
| `reddit_login.py` | Script che guida l’utente nella generazione di un **refresh token** via browser. |

---

###  Funzionamento
Se Reddit blocca le richieste per limiti di autenticazione o sessioni scadute, puoi rigenerare un `refresh_token` in modo sicuro:

1. Esegui `reddit_login.py`
2. Verrà aperta una finestra del browser per autenticarti su Reddit
3. Dopo il login, copia il parametro `code` dal link di reindirizzamento
4. Incollalo nel terminale: verrà restituito un `refresh_token`
5. Inseriscilo nel file `config.py`

---

##  YouTube Search – `youtube_search.py`

### Descrizione
Questo modulo fornisce una funzione per cercare video su YouTube tramite API non ufficiali.  
Restituisce una lista di ID, titoli e link, usata da `youtube_ingestion.py` per avviare lo scraping.

---

###  Dipendenze
- [`youtube-search-python`](https://pypi.org/project/youtube-search-python/)

---

##  Instagram Login – `instagram_cookie_login.py`

### Descrizione
Script per eseguire un login **manuale** su Instagram tramite Selenium e salvare i **cookie di sessione** in un file `.json`.  
Questi cookie possono poi essere caricati da moduli scraping come `instagram_profiles_scraper.py`.

---

###  Dipendenze
- [`selenium`](https://pypi.org/project/selenium/)
- Google Chrome + [ChromeDriver](https://chromedriver.chromium.org/)

---

###  File generati

| File                         | Descrizione                                   |
|------------------------------|-----------------------------------------------|
| `instagram_cookie_login.py`  | Script principale per login e salvataggio     |
| `instagram_cookies_scraper.json` | File di output con i cookie autenticati |
| `chromedriver.exe`           | Necessario per Selenium (non incluso nel repo)|

---

###  Come funziona
1. Apre una finestra di Chrome su `https://www.instagram.com/accounts/login/`
2. Inserisce username e password nei campi login
3. Attende 60 secondi per 2FA o CAPTCHA
4. Salva i cookie di sessione nel file `.json`

---

##  Language Detection – `language_detection.py`

### Descrizione
Fornisce due funzioni leggere per rilevare automaticamente la **lingua di ogni commento**.  
Essenziale per filtrare contenuti per lingua prima di sentiment analysis o clustering.

---

###  Dipendenze
- [`langdetect`](https://pypi.org/project/langdetect/)

---

##  TF-IDF Vectorizer – `tfidf_utils.py`

### Descrizione
Modulo utility per trasformare un corpus testuale in una **matrice TF-IDF**, utile per attività di clustering, topic modeling e selezione di feature.

---

###  Dipendenze
- [`scikit-learn`](https://scikit-learn.org/)

---

##  Clustering Tematico – `clustering_utils.py`

### Descrizione
Applica l’algoritmo `KMeans` di scikit-learn su una matrice TF-IDF per segmentare i commenti in **gruppi tematici**.

---

###  Dipendenze
- [`scikit-learn`](https://scikit-learn.org/)
- `numpy`

---

##  Etichettatura dei Cluster – `keyword_utils.py`

### Descrizione
Fornisce due funzioni per assegnare etichette semantiche a ciascun cluster tematico:

- Estrazione delle parole chiave più frequenti per cluster
- Generazione di etichette testuali leggibili

---

###  Dipendenze
- `numpy`
- `collections` (standard)

---


