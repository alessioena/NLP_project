import sys
import os
import gensim
from gensim import corpora, models
import pandas as pd
import matplotlib.pyplot as plt
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import seaborn as sns
import warnings
from gensim.models import CoherenceModel

warnings.filterwarnings("ignore", category=DeprecationWarning)


def topic_modelling(csv,num_top):
    ds=pd.read_csv(csv, encoding ="latin-1")
    ds.dropna(subset=['Token'], inplace=True)

    tokens=[] # lista di liste
    if type(ds.Token[1])==str: # se l'i-esima lista di token è una stringa
        lista = ds['Token'].to_list()
        for i in lista:
            import ast
            l = ast.literal_eval(i)
            l = [i.strip() for i in l]
            word=" ".join(l)
            tokens.append(word.split()) # prende ciascuna lista di token e li inserisce nella lista tokens

    try:
        dic = gensim.corpora.Dictionary(tokens) # prende in ingresso una lista di liste
        corpus_matrix= [dic.doc2bow(x) for x in tokens]
        #print([[(dic[id], freq) for id, freq in cp] for cp in corpus_matrix[:1]]) # controllo della bag of word


        LDA= gensim.models.ldamodel.LdaModel
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus_matrix,
                                                            id2word=dic,
                                                            num_topics=num_top, # numero di topic
                                                            random_state=100, # seed
                                                            update_every=1,
                                                            chunksize=100,
                                                            passes=5,
                                                            alpha='auto',
                                                            per_word_topics=True)

        print(lda_model.print_topics()) # print dei topic
        coherence_model_lda = CoherenceModel(model=lda_model, texts=tokens, dictionary=dic, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        print('\nCoherence Score: ', coherence_lda)
        print('\nPerplexity: ', lda_model.log_perplexity(corpus_matrix)) # misurano quanto il modello è buono

        ''' x salvare le performance
        perp=lda_model.log_perplexity(corpus_matrix)
        dataframe=pd.DataFrame({'NTopics':[num_top],'Coherence':[coherence_lda],'Perplexity':[perp]})
        if (os.path.exists("/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/data_analysis/coherence_tweet.csv")):
            dataframe.to_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/data_analysis/coherence_tweet.csv',
                             mode='a', index=False, header=False)
        else:
            dataframe.to_csv('/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/data_analysis/coherence_tweet.csv', index=False)'''

        vis= gensimvis.prepare(lda_model,corpus_matrix,dic)#, mds='tsne') #mmds
        pyLDAvis.save_html(vis, 'LDA.html') # salvataggio in formato HTML


    except Exception as e:
        from colorama import Fore
        from colorama import Style
        print(f"{Fore.RED}UNEXPECTED ERROR:")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(str(e), fname, exc_tb.tb_lineno, f'{Style.RESET_ALL}\n')


def performance_graph(csv):
    ds=pd.read_csv(csv)
    sns.set_theme(style="darkgrid")
    sns.lineplot(
        data=ds, x=ds.NTopics, y=ds.Coherence,
        markers=True, dashes=False
    )
    sns.scatterplot(x=ds.NTopics, y=ds.Coherence, data=ds)
    plt.show()

    sns.set_theme(style="darkgrid")
    sns.lineplot(
        data=ds, color='purple', x=ds.NTopics, y=ds.Perplexity,
        markers=True, dashes=False
    )
    sns.scatterplot(x=ds.NTopics, y=ds.Perplexity, data=ds, color='purple')
    plt.show()




if __name__=='__main__':

    num_top=9
    ###x i tweet
    #csv='/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/cleaned_tweets.csv'
    #topic_modelling(csv, num_top)

    ###x i libri
    csv='/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/corpus_x_TM.csv'
    topic_modelling(csv,num_top)

    ##########################################################################
    #GRAFICO PERFORMANCE
    #csv_coherence = '/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/data_analysis/coherence_libri.csv'
    #csv_coherence = '/Users/alessio/PycharmProjects/NLP_Climate/00307_ena/data_analysis/coherence_tweet.csv'
    #performance_graph(csv_coherence)