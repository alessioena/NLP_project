import snscrape.modules.twitter as sntwitter
import pandas as pd
import os
import sys

class Tweets(object):

    def __init__(self,limit,until,since,min_retweets):
        '''Prende in ingresso il numero massimo di tweet che si vogliono estrarre, il numero minimo di retweet che deve avere
        ciascun tweet raccolto, la data da cui si vuole iniziare ad effettuare la raccolta e la data in cui il programma deve smettere
        di raccogliere tweet'''
        self.limit = limit
        self.until=until
        self.since=since
        self.min_retweets=min_retweets
        print('Raccolta dei tweet in corso..\n')

    def get_tweets(self):
        '''
        Questa funzione estrapola i tweet e alcune informazioni a loro correlate (id del tweet, id utente, data del tweet,
        contenuto tweet, numero di retweet,numero di like, numero di replies, coordinate del tweet)
         e immagazzina queste informazioni in un csv.
        '''
        tweets = []
        keywords ="climate hoax"
        query = f"({keywords}) min_retweets:{self.min_retweets} lang:en until:{self.until} since:{self.since} -filter:replies"

        try:
            i=0
            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                if len(tweets) == self.limit:
                    break
                else:
                    tweets.append([tweet.id, tweet.user.id,tweet.date, tweet.content,tweet.retweetCount,
                                   tweet.likeCount,tweet.replyCount,tweet.coordinates])
                    i+=1
                    if i % 100 == 0:
                        print(f'Tweet raccolti: {i} ')

            df = pd.DataFrame(tweets, columns=['ID', 'UserID' ,'Date', 'Tweet','Retweet',
                                               'Replies','Likes','Coordinate'])
            print(df)
            df.to_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/raw_tweets.csv',index=False)

        except Exception as e:
            from colorama import Fore
            from colorama import Style
            print(f"{Fore.RED}UNEXPECTED ERROR:")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(str(e), fname, exc_tb.tb_lineno,f'{Style.RESET_ALL}\n')

    def __str__(self):

        ds = pd.read_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/raw_tweets.csv')
        info= f'Collezione di {ds.shape[0]} tweet relativi al Climate Change raccolti dal {self.since} al {self.until}.'
        return info

if __name__=='__main__':

    until = '2022-08-01'
    since = '2020-01-01'
    limit = 500000
    retweets = 0

    request = Tweets(limit,until,since,retweets)
    request.get_tweets()
    print(request)

