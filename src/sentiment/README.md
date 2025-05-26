# Sentiment Analysis Section

---

## Sentiment Analysis – `sentiment_multilingual.py`

### Descrizione
Questo script applica un'analisi del sentiment multilingua ai commenti raccolti dal dataset social unificato, utilizzando il modello pre-addestrato `nlptown/bert-base-multilingual-uncased-sentiment`. I risultati vengono salvati in un nuovo file CSV con una colonna aggiuntiva `sentiment` che etichetta ciascun commento come `positive`, `neutral` o `negative`.

### Modello utilizzato
- [`nlptown/bert-base-multilingual-uncased-sentiment`](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment)

### Dipendenze
- `transformers`
- `pandas`
- `tqdm`

### File coinvolti
- **Input**: `data/f1_social_clean.csv`
- **Output**: `data/f1_social_sentiment_multilingua.csv`
- **Script**: `sentiment_bert_multilingua.py`

### Come funziona
1. Carica il dataset pulito con i commenti social.
2. Applica il modello di sentiment su ogni commento (limite di 512 caratteri).
3. Converte le etichette numeriche in classi testuali: `positive`, `neutral`, `negative`.
4. Salva il nuovo dataset in formato CSV con una colonna aggiuntiva `sentiment`.

---

## Toxicity Scoring – `toxic_analysis.py`

### Descrizione
Questo script applica un modello BERT specializzato nel rilevare contenuti tossici (`unitary/toxic-bert`) sui commenti del dataset unificato. Per ogni commento viene assegnato un punteggio di tossicità continuo tra 0 e 1, che rappresenta la probabilità che il testo sia tossico.

### Modello utilizzato
- [`unitary/toxic-bert`](https://huggingface.co/unitary/toxic-bert)

### Dipendenze
- `transformers`
- `torch`
- `pandas`
- `tqdm`

### File coinvolti
- **Input**: `data/f1_social_clean.csv`
- **Output**: `data/sentiment_score_toxicbert.csv`
- **Script**: `toxic_analysis.py`

---

## Analisi Sentiment per Nomi e Fasi Temporali – `report_sentiment_bert.py`

### Descrizione
Questo script esegue due analisi sul dataset etichettato con sentiment:

1. **Sentiment per nome di guidatore**: calcola il sentiment medio per ciascun pilota menzionato nei commenti.
2. **Sentiment temporale**: analizza il sentiment medio prima, durante e dopo la gara del GP di Monaco 2025.

### Dipendenze
- `pandas`
- `matplotlib`

### File coinvolti
- **Input**: `data/f1_social_sentiment_multilingua.csv`
- **Output**:
  - `report/sentiment_medio_per_nome.png`
  - `report/sentiment_medio_per_fase.png`
- **Script**: `report_sentiment_bert.py`

---

## Analisi Tossicità per Social Media – `analisi_tossicita.py`

### Descrizione
Analizza la tossicità media dei commenti per ciascuna piattaforma social, basandosi sui punteggi generati con `unitary/toxic-bert`. I risultati sono visualizzati in un grafico a barre.

### Dipendenze
- `pandas`
- `matplotlib`

### File coinvolti
- **Input**: `data/sentiment_score_toxicbert.csv`
- **Output**: `data/tossicita_media_social.png`
- **Script**: `analisi_tossicita.py`

---

## Clustering Tematico e Etichettatura – `cluster_theme_labeling.py`

### Descrizione
Applica clustering basato su TF-IDF ai commenti in lingua inglese per identificare temi principali. Assegna a ciascun commento un cluster (`theme_cluster`) e genera etichette testuali sintetiche per ciascun gruppo.

### Dipendenze
- `pandas`
- `scikit-learn`
- `nltk`

### Moduli personalizzati
- `src/utils/tfidf_utils.py`
- `src/utils/clustering_utils.py`
- `src/utils/keyword_utils.py`

### File coinvolti
- **Input**: `data/f1_social_clean.csv`
- **Output**:
  - `data/f1_social_labeled.csv`
  - `data/cluster_descriptions.json`
- **Script**: `cluster_theme_labeling.py`

---

## Sentiment Analysis con RoBERTa – `roberta_sentiment.py`

### Descrizione
Applica il modello `cardiffnlp/twitter-roberta-base-sentiment` per classificare ogni commento come `positive`, `neutral`, o `negative`, includendo anche i punteggi associati a ciascuna classe.

### Modello utilizzato
- [`cardiffnlp/twitter-roberta-base-sentiment`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)

### Dipendenze
- `transformers`
- `torch`
- `pandas`
- `scipy`
- `tqdm`

### File coinvolti
- **Input**: `data/f1_social_labeled.csv`
- **Output**: `data/f1_social_sentiment_roberta.csv`
- **Script**:
  - `roberta_sentiment.py`
  - `run_roberta_sentiment.py`

### Come funziona
1. Tokenizza e processa i commenti in batch.
2. Applica il modello RoBERTa per ottenere le probabilità di sentiment.
3. Salva etichetta e score per ogni commento.

---

## Analisi Temporale del Sentiment per Cluster – `time_series_sentiment.py`

### Descrizione
Analizza l’andamento giornaliero del sentiment positivo (`roberta_pos`) per ciascun `theme_cluster`. Include la generazione di grafici aggregati e separati per ogni cluster.

### Funzionalità
- `generate_theme_daily_sentiment`: calcola e salva i valori medi giornalieri per cluster.
- `plot_sentiment_trend`: visualizza l’andamento di tutti i cluster in un unico grafico.
- `plot_sentiment_trend_by_cluster`: salva un grafico PNG per ciascun cluster.

### File coinvolti
- **Input**: `data/f1_social_sentiment_roberta.csv`
- **Output**:
  - `data/theme_daily_sentiment.json`
  - `report/plots/cluster_<id>_sentiment.png`

---

## Estrazione Entità e Like Aggregati per Cluster – `entity_likes_extraction.py`

### Descrizione
Utilizza `spaCy` per estrarre entità di tipo `PERSON` e `ORG` dai commenti e sommare il numero di like ricevuti da ogni entità in ciascun cluster.

### Dipendenze
- `pandas`
- `spacy`
- Modello: `en_core_web_sm`

### File coinvolti
- **Input**: `data/f1_social_sentiment_roberta.csv`
- **Output**: `data/cluster_entity_likes.json`
- **Script**: `entity_likes_extraction.py`

---

## Esecuzione degli Script

Tutti gli script devono essere eseguiti dalla directory `sentiment/`.

```bash
# Sentiment multilingua con BERT
python sentiment/sentiment_bert_multilingua.py

# Analisi tossicità con Toxic-BERT
python sentiment/toxic_analysis.py

# Report su sentiment per nomi e fasi temporali
python sentiment/report_sentiment_bert.py

# Analisi tossicità per piattaforma social
python sentiment/analisi_tossicita.py

# Clustering tematico e generazione etichette
python sentiment/cluster_theme_labeling.py

# Sentiment con RoBERTa
python sentiment/run_roberta_sentiment.py

# Andamento temporale del sentiment per cluster
python sentiment/run_time_series_sentiment.py

# Estrazione entità e like aggregati
python sentiment/entity_likes_extraction.py











