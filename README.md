# Il negazionismo climatico: un'analisi testuale della letteratura pseudoscientifica e dei tweet dei complottisti

Questo progetto si prefigge di analizzare i tweet ed alcuni libri scritti dai 
negazionisti climatici attraverso le tecniche di NLP e di machine learning. L'obiettivo è quello
di far luce sulle tesi più accreditate da questa nuova corrente di pensiero pseudoscientifica.

# Struttura del progetto

### [Data collection](https://bitbucket.org/mortu/00307_ena/src/master/data_collection/)

Al fine di raggiungere gli obiettivi preposti per questo progetto la fase di data collection è
stata suddivisa in due fasi: nella prima, una volta selezionati i [libri della letteratura pseudoscientifica](https://bitbucket.org/mortu/00307_ena/src/master/data_cleaning/corpus_complottismo/) 
correlata al Climate Change, sono stati processati i pdf di ciascun libro per poi riportare il loro testo in 
file.txt e in file.csv. Nella seconda fase invece sono stati estratti i tweet correlati alle teorie del complotto sui cambiamenti climatici
attraverso il programma [tweets.py](https://bitbucket.org/mortu/00307_ena/src/master/data_collection/tweets.py).

Sono stati inoltre estrapolati i luoghi di provenienza di ciascun tweet 
estratto dotato di coordinate attraverso il programma [reverse_geocoding.py](https://bitbucket.org/mortu/00307_ena/src/master/data_collection/reverse_geocoding.py).

### [Data cleaning](https://bitbucket.org/mortu/00307_ena/src/master/data_cleaning/)

Nella fase di data cleaning sono stati puliti i corpus estratti da twitter e dai libri attraverso i 
programmi [pdf_cleaner.py](https://bitbucket.org/mortu/00307_ena/src/master/data_cleaning/pdf_cleaner.py)
e [tweets_cleaner.py](https://bitbucket.org/mortu/00307_ena/src/master/data_cleaning/tweets_cleaner.py).


### [Data analysis](https://bitbucket.org/mortu/00307_ena/src/master/data_analysis/)

In questa fase del progetto viene eseguita un'analisi esplorativa dei corpus 
attraverso l'utilizzo delle [word cloud](https://bitbucket.org/mortu/00307_ena/src/master/data_analysis/word_cloud.py), dopodichè 
viene programmato un modello di topic modelling attraverso il programma [topic_modelling.py](https://bitbucket.org/mortu/00307_ena/src/master/data_analysis/topic_modelling.py)
per ambe due i corpus e vengono discussi i risultati ottenuti. Infine viene eseguita una 
sentiment and emotion analysis dei tweet attraverso il programma [sent_emotions_analyser.py](https://bitbucket.org/mortu/00307_ena/src/master/data_analysis/sent_emotions_analyser.py).


