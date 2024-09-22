import numpy as np
import pandas as pd
import geopandas as gpd
import re
from geopy import Nominatim
import matplotlib.pyplot as plt


class ReverseGeo(object):
    '''Questa classe si occupa di ricavare il nome di un determinato luogo date in input la latitudine
    e la longitudine'''
    def __init__(self, coord):
        self.coord = coord
        print('Elaborazione in corso..\n')

    def clean_coord(self):
        set_coord=[]
        for i in self.coord:
            coord=i[1]
            disallowed_characters = "()=abCdefghijklmnopqrstuvwxyz"
            for character in disallowed_characters:
                coord = coord.replace(character, "") #rimozione dei caratteri non numerici
            C = re.split(',', coord) #incasellamento delle due coordinate in una lista
            set_coord.append(C)
        return set_coord

    def get_location(self):
        for i in request.clean_coord():
            geolocator=Nominatim(user_agent='test/1')
            location=geolocator.reverse(f'{i[1]},{i[0]}') # 1°latitude, 2°longitude
            print(f'{location} : lat {i[1]} long {i[0]}\n')

    def get_geomap(self):
        ds=pd.DataFrame(request.clean_coord(),
                 columns=["long","lat"])
        ds = ds.astype(np.float16) # converte le coordinate in float
        BBox = (-180, 180, -90, 90) # Bounding Box per delimitare i confini della mappa
        fig, ax = plt.subplots(figsize=(8, 6))
        world = gpd.read_file(
            gpd.datasets.get_path('naturalearth_lowres')) # carica la mappa 2D della Terra
        world.plot(color='whitesmoke', edgecolor='lightgrey',ax=ax)

        # plot scatter plot dei tweet
        ds.plot(x='long',y='lat', kind="scatter",zorder=1,c='deepskyblue',alpha=0.1, ax=ax)
        ax.set_xlim(BBox[0], BBox[1])
        ax.set_ylim(BBox[2], BBox[3])
        #ax.get_xaxis().set_visible(False)
        #ax.get_yaxis().set_visible(False)
        plt.show()


if __name__=='__main__':
    df = pd.read_csv(r'/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/raw_tweets.csv', encoding ="latin-1")
    NaN = df['Coordinate'].isna().sum() # conteggio dei NA
    valide=df['Coordinate'].notna().sum() # valido anche df['Coordinate'].count()
    print(f'Su un totale di {df.shape[0]} coordinate il numero di NaN è pari a {NaN} perciò solo {valide} sono valide per essere interpretate.')
    data=df[df['Coordinate'].notna()]
    del data['UserID'],data['Date'],data['Tweet'],data['Likes'],data['Retweet'],data['Replies']
    coordinate=data.values.tolist()

    request=ReverseGeo(coordinate)
    #request.get_location()
    request.get_geomap()