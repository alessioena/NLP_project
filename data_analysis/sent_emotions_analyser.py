import pandas as pd
import seaborn as sns
import statistics as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
from nrclex import NRCLex
from collections import defaultdict
import matplotlib.pyplot as plt


class SentAnalyser(object):

    def __init__(self, ds):
        self.ds = ds
        print('Elaborazione in corso..\n')

    def get_tweet_sentiment(self):
        '''
        Calcolo del sentiment
        '''
        text = ds['Token']
        list=[]
        numeric_sent=[]
        for i in text:
            vs = analyzer.polarity_scores(i)
            numeric_sent.append(vs['compound'])
            if vs['compound'] > 0:
                list.append('positive')
            elif vs['compound']== 0:
                list.append('neutral')
            else:
                list.append('negative')

        ds['Sentiment'] = list
        ds['Sentiment_score']=numeric_sent
        print(ds.Sentiment)
        ds.to_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/dsFin_sent.csv', index=False)

    def get_emotion(self):

        list = ds['Token'].to_list()
        c=1
        if type(ds.Token[c]) == str:  # se l'i-esima lista di token è una stringa
            c+=1
            fear,anger,anticip,trust,surprise=[],[],[],[],[]
            positive, negative, sadness, disgust, joy=[],[],[],[],[]
            for i in list:
                #print(i)
                import ast
                l = ast.literal_eval(i)
                l = [i.strip() for i in l]
                word=" ".join(l)
                #print(word)
                emotion = NRCLex(word)
                #print(emotion.affect_frequencies)
                fear.append(emotion.affect_frequencies["fear"])
                anger.append(emotion.affect_frequencies["anger"])
                anticip.append(emotion.affect_frequencies["anticip"])
                trust.append(emotion.affect_frequencies["trust"])
                surprise.append(emotion.affect_frequencies["surprise"])
                positive.append(emotion.affect_frequencies["positive"])
                negative.append(emotion.affect_frequencies["negative"])
                sadness.append(emotion.affect_frequencies["sadness"])
                disgust.append(emotion.affect_frequencies["disgust"])
                joy.append(emotion.affect_frequencies["joy"])

                #print(f'Fear: {len(fear)},Fear: {len(anger)},Anticip: {len(anticip)},'
                      #f'Fear: {len(trust)},Fear: {len(surprise)},Fear: {len(positive)}, Joy: {len(negative)},'
                      #f'Fear: {len(sadness)},Fear: {len(disgust)},Fear: {len(joy)}')
                # Inserimento delle emotion nel dataframe:
            ds["Fear"]=pd.Series(fear)
            ds["Anger"]= pd.Series(anger)
            ds["Anticip"] = pd.Series(anticip)
            ds["Trust"] = pd.Series(trust)
            ds["Surprise"] = pd.Series(surprise)
            ds["Positive"] = pd.Series(positive)
            ds["Negative"] = pd.Series(negative)
            ds["Sadness"] = pd.Series(sadness)
            ds["Disgust"] = pd.Series(disgust)
            ds["Joy"] = pd.Series(joy)

        print(ds)
        ds.to_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/dsFin_emotion.csv', index=False)


    def get_graph(self):
        ds = pd.read_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/dsFin_sent.csv')

        word_freq = defaultdict(int)
        sent=ds.Sentiment.tolist()
        for i in sent:
            word_freq[i] += 1
        sentiment=word_freq.keys()
        values=word_freq.values()

        print(list(sentiment))
        neg,pos,neu=word_freq['negative'],word_freq['positive'],word_freq['neutral']
        print(f'Tweet con sentiment negativo: {neg}\n'
              f'Tweet con sentiment positivo: {pos}\n'
              f'Tweet con sentiment neutrale: {neu}')

        color = ['red','lime','lightgrey']

        plt.bar(list(sentiment),list(values),
                width=0.6,linewidth=1,edgecolor='black',color=color)


        #plt.xlabel("Sentiment")
        plt.ylabel("Number of tweets")
        #plt.title("Sentiment analysis")
        plt.show()

    def get_emotion_graph(self):
        ds = pd.read_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/dsFin_emotion.csv')
        avg_emotions=[st.mean(ds.Fear),st.mean(ds.Anger),st.mean(ds.Anticip),st.mean(ds.Trust),st.mean(ds.Surprise),
                  st.mean(ds.Positive),st.mean(ds.Negative),st.mean(ds.Sadness),st.mean(ds.Disgust),st.mean(ds.Joy)]
        avg_emotions.sort(reverse=True)
        #print(avg_emotions)
        #data = np.array(raw_data)
        #x = np.arange(len(raw_data))

        #index = ['Fear','Anger','Anticip','Trust','Surprise','Positive','Negative','Sadness','Disgust','Joy']
        index = ['Negative', 'Anger', 'Fear', 'Sadness','Surprise','Disgust','Positive','Trust','Joy','Anticip']
        # TODO: fare attenzione a riordinare le emozioni (se si cambia dataset)

        sns.barplot(avg_emotions, index, palette='hls')
        plt.show()


if __name__=='__main__':

    ds = pd.read_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/cleaned_tweets.csv')

    request=SentAnalyser(ds)

    #request.get_tweet_sentiment()
    request.get_emotion()
    #request.get_graph()
    request.get_emotion_graph()