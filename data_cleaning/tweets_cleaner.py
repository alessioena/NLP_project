import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings("ignore")

class Cleaner(object):

    def __init__(self,data):
        self.data=data
        print('Cleaning del corpus in corso..\n')

    def clean_text(self):
        '''
        Pulizia iniziale
        '''
        del self.data['Coordinate']

        '''
        Pulizia dei tweet doppi
        '''
        ntweet=self.data.shape[0]
        df=self.data.drop_duplicates(
            subset=['UserID', 'Tweet'],
            keep='last').reset_index(drop=True)
        ntweet_finale=df.shape[0]
        print(f'Prima della pulizia dei tweet doppi il dataset era composto da  {ntweet} tweet'
              f' ora ha un numero di tweet pari a {ntweet_finale}.\n'
              f'{ntweet-ntweet_finale} tweet doppi sono stati eliminati.\n')
        df.dropna() # Pulizia dei NA risultanti dall'operazione di cleaning
        self.data=df
        del self.data['UserID']

        '''
        #Rimozione dei caratteri speciali e della punteggiatura
        '''
        self.data.Tweet.replace(regex=True, inplace=True,to_replace=r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(https?\S+)',value=' ')

        '''
        #Tokenizzazione
        '''
        def tokenize(tweets):
            tokens = re.split('\W+', tweets)
            return tokens

        raw_tokens=self.data['Tweets_tokenized'] = self.data.Tweet.apply(lambda x: tokenize(x.lower()))

        '''
        #Rimozione delle stopwords 
        '''
        stopwords = nltk.corpus.stopwords.words('english')
        keywords=['climate hoax']
        def remove_stopwords(raw_tokens):
            text = [word for word in raw_tokens if word not in stopwords and word not in keywords]
            return text

        self.data['Tokens'] = raw_tokens.apply(lambda x: remove_stopwords(x))

        '''
        Lemmatizzazione e rimozione delle keyword indesiderate
        '''
        wnl=WordNetLemmatizer()
        ds_intermedio=self.data.dropna() # rimozione NA

        lemmatized_tweet=[] # lista di stringhe
        for i in ds_intermedio.Tokens:
            l=[]
            for word in i:
                lem_word = wnl.lemmatize(word)
                text = "".join(lem_word)
                l.append(text)
                '''
                if text=="chang" or text=="chan" or text=="cha":
                    l.append('change')
                else:
                    l.append(text)'''
            lemmatized_tweet.append(l)

        self.data['Token']=lemmatized_tweet

        '''
        Cleaning finale e creazione del csv
        '''

        del self.data['Tweet']
        del self.data['Tweets_tokenized']
        del self.data['Tokens']
        final_cleanedDS=self.data.dropna()

        final_cleanedDS.to_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/cleaned_tweets.csv',
                               index=False)
        print(final_cleanedDS.Token)
        print(final_cleanedDS.Token.shape[0])


if __name__=='__main__':

    ds = pd.read_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/raw_tweets.csv')

    request = Cleaner(ds)
    request.clean_text()
    


