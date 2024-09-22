import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import (WordCloud,get_single_color_func)


class Word_Cloud(object):

    def __init__(self,csv,color_to_words,default_color='grey'):
        self.csv=csv
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}
        self.default_color = default_color
        print('Elaborazione in corso..\n')

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)

    def word_cloud(self):
        '''
        Standard word cloud
        '''
        df = pd.read_csv(f'{self.csv}', encoding ="latin-1")
        #print(df)
        '''
        Conversione del dataframe in stringa e controllo per caratteri non ammessi
        '''
        ds=df.Token.to_string()
        disallowed_characters = "'"
        for character in disallowed_characters:
            ds = ds.replace(character, "")

        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              min_font_size=8).generate(ds)

        # plot the WordCloud image
        plt.figure(figsize=(8, 8), facecolor=None)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        #plt.tight_layout(pad=0) #focus

        plt.show()

    def color_word_cloud(self):
        '''
        Word cloud con selezione colori
        '''
        df = pd.read_csv(f'{self.csv}', encoding ="latin-1")


        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              min_font_size=20).generate(df.Token.to_string())

        wordcloud.recolor(color_func=request2)

        # Plot
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.show()


if __name__=='__main__':

    color_to_words = {
        # black
        '#000000': ['oil', 'petroleum', 'coal','carbon','industry',
                    'carbon dioxide'],

        # viola (scienza)
        'slateblue': ['science', 'scientist','scientific','data','evidence','research'],

        # red (sostenitori o tesi complotto)
        'red': ['phil jones', 'trump','jones cru','mcintyre','hockey stick','illusion',
                'mckitrick','mann','bradley','mbh98'],

        # blu chiaro (dem)
        'deepskyblue': ['democrat','obama','president obama', 'al gore'],

        # Blue navy (Istituzioni e politica)
        'navy': ['president','senate','rules','ipcc','epa','us',
                 'nation','congress','senator','government',
                 'america','united states','un','political','kyoto','cap trade',
                 'regulation'],

        # Green (Climate change e ambiente)
        '#00ff00': ['climate','world','earth','green','environment',
                    'greenhouse gas','environmental','water','greenland',
                    'ocean','antarctica','nature','tree'
                    ],

        # Red (pericoli e problemi)
        'darkred': ['global warming','climate change','warming','problem',
                'hoax','scam','issue', 'implicit', 'complex', 'complicated', 'nested',
                'errors', 'silently', 'ambiguity','hard','hurricane','sea level rise',
                    'extreme']
    }

    #request=Word_Cloud('The Greatest Hoax.csv',{})

    #request2 = Word_Cloud('The Greatest Hoax.csv', color_to_words)
    #request2 = Word_Cloud('Climate of Corruption.csv', color_to_words)
    #request2 = Word_Cloud('Climate of Extremes.csv', color_to_words)
    #request2 = Word_Cloud('The Hockey Stick Illusion.csv', color_to_words)

    #request.word_cloud()
    #request2.color_word_cloud()

    ##############################################################################
    # PER I TWEET
    df = '/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/cleaned_tweets.csv'

    request_T = Word_Cloud(df, {})
    request_T.word_cloud() # richiesta x tweet
