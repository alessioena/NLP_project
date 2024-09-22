import string
import re
import nltk
from nltk.stem import WordNetLemmatizer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfpage import PDFPage
import pandas as pd
import csv


class CleanerPDF(object):
    '''La classe prende in ingresso il path del libro, il nome del libro, la pagina da dove si vuole far partire l'analisi
    e la pagina alla quale in programma deve fermarsi'''
    def __init__(self, libro,nome,inizio,fine):
        self.libro = libro
        self.nome=nome
        self.inizio=inizio
        self.fine=fine
        print('Elaborazione in corso..\n')

    def get_pdf_file_content(self):
        '''legge il file pdf e ne crea una copia in formato .txt'''

        resource_manager = PDFResourceManager(caching=True)
        out_text = StringIO() # string object
        laParams = LAParams() # object contenente il layout
        text_converter = TextConverter(resource_manager, out_text, laparams=laParams)

        f = open(self.libro, 'rb')
        interpreter = PDFPageInterpreter(resource_manager, text_converter)

        # grazie al seguente ciclo vengono selezionate solo le pagine incluse nel range:self.inizio-self.fine
        i=0
        for page in PDFPage.get_pages(f, pagenos=set(), maxpages=0, password="", caching=True, check_extractable=True):
            if i>=self.inizio:
                if i<=self.fine:
                    interpreter.process_page(page)
                    i+=1
                else:
                    break
            else:
                i+=1
                pass

        text = out_text.getvalue() # contiene l'intero testo selezionato
        f.close()
        text_converter.close()
        out_text.close()
        copia = open(f'{self.nome}.txt', 'w')
        copia.write(text)
        copia.close()
        return text

    def clean_text(self):

        testo= request.get_pdf_file_content()
        '''
        Rimozione dei caratteri speciali e della punteggiatura
        '''
        testo = "".join([char for char in testo if char not in string.punctuation])

        '''
        Tokenizzazione
        '''
        raw_tokens = re.split('\W+', testo)
        nparole=len(raw_tokens)
        print(f'Il pdf in esame è composto da {nparole} parole. \n')

        '''
        Rimozione delle stopwords 
        '''
        stopwords = nltk.corpus.stopwords.words('english')
        tokens=[t for t in raw_tokens if not t in stopwords]

        '''
        Lemmatizzazione
        '''
        wnl=WordNetLemmatizer()
        token=[]
        for w in tokens:
            token.append(wnl.lemmatize(w))
            #print(w,' : ',wnl.lemmatize(w)) # confronto

        '''
        Salvataggio in un dataframe e ritocchi finali
        '''
        df = pd.DataFrame(data=token, columns=['Token'])
        df['Token']=df['Token'].apply(str.lower)
        df['Token'] = df['Token'].replace(['u'], 'us')
        #df.drop(df.loc[df['Token'] == 's'].index, inplace=True)


        print(f'Dopo il processo di cleaning il numero di parole del libro è pari a {df.shape[0]}. \n')
        df.to_csv(f'/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/data_analysis/{self.nome}.csv', index=False)
        print(df)

    def unify_corpus(self):
        file1 = open('The Greatest Hoax.txt', 'r')
        hoax = file1.read()
        file1.close()
        file2 = open('Climate of Corruption.txt', 'r')
        corruption = file2.read()
        file2.close()
        file3 = open('Climate of Extremes.txt', 'r')
        climExt = file3.read()
        file3.close()
        file4 = open('The Hockey Stick Illusion.txt', 'r')
        hockey = file4.read()
        file4.close()

        nuovotxt=hoax+corruption+climExt+hockey # unione dei corpus
        finalfile = open('corpuslibri.txt', 'w')
        finalfile.write(nuovotxt)
        finalfile.close()


    def topmod_preparation(self):
        print('Preparazione del corpus per il topic modelling in corso..')
        file = open('corpuslibri.txt', 'r')
        lines=file.readlines()

        list=[]
        for line in lines:
            if line.rstrip():
                #rimozione punteggiatura
                testo = "".join([char for char in line.strip() if char not in string.punctuation])
                testo_l=testo.lower()
                #tokenizzazione
                raw_tokens = re.split('\W+', testo_l)
                #rimozione stopwords
                stopwords = nltk.corpus.stopwords.words('english')
                tokens = [t for t in raw_tokens if not t in stopwords]
                #lemmatizzazione
                wnl = WordNetLemmatizer()
                token = []
                for w in tokens:
                    if len(w)>1:
                        token.append(wnl.lemmatize(w))
                if token!=[]:
                    list.append(str(token))
        file.close()

        df=pd.DataFrame(list,columns=['Token'])
        df.dropna()
        df.to_csv(f'/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/corpus_x_TM.csv', index=False)


if __name__=='__main__':

    #request = CleanerPDF('./corpus_complottismo/The Greatest Hoax.pdf','The Greatest Hoax',10,292)
    #request = CleanerPDF('./corpus_complottismo/Climate of Corruption.pdf','Climate of Corruption', 9, 286)
    #request = CleanerPDF('./corpus_complottismo/Climate of Extremes.pdf','Climate of Extremes', 7, 252)
    #request = CleanerPDF('./corpus_complottismo/The Hockey Stick Illusion.pdf','The Hockey Stick Illusion', 9, 354)

    request = CleanerPDF('./ISLR.pdf', 'ISLR', 12, 520) #non ci riesce

    request.clean_text()

    #request.unify_corpus()
    #request.topmod_preparation()
