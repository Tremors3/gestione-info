import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

"""
Testing della funzionalità dello Stemmer.
Gli stemmer più noti sono Porter e Lancaster, entrambi implementati nella libreria nltk.
"""

if __name__ == "__main__":
    
    """ Fase 1: Tokenizzazione """
    
    # Definizione della frase di esempio
    sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
    
    # Tokenizzazione della frase in parole (token)
    tokens = nltk.word_tokenize(sentence)
    
    # Conversione di tutti i token in minuscolo
    tokens = [token.lower() for token in tokens]
    
    """ Fase 2: Rimozione delle stopwords """
    
    # Recupero delle stopwords in inglese
    stop_words = set(stopwords.words('english'))
    
    # Rimozione delle stopwords dai token
    non_stopword_tokens = [token for token in tokens if token not in stop_words]
    
    """ Fase 3a: Lemmatizzazione dei token """
    
    # Crea un'istanza del lemmatizzatore
    wnl = nltk.WordNetLemmatizer()
    
    # Lemmatizzazione dei token non stopwords
    lemmatized_tokens = [wnl.lemmatize(token) for token in non_stopword_tokens]
    
    """ Fase 3b: Stemming dei token """

    # Crea le istanze degli stemmer
    porter_stemmer = PorterStemmer()  # Porter Stemmer
    lancaster_stemmer = LancasterStemmer()  # Lancaster Stemmer

    # Variabile per scegliere lo stemmer da utilizzare
    use_porter_stemmer = True

    # Stemming dei token lemmatizzati utilizzando lo Stemmer scelto
    if use_porter_stemmer:
        stemmed_tokens = [porter_stemmer.stem(token) for token in lemmatized_tokens]
    else:
        stemmed_tokens = [lancaster_stemmer.stem(token) for token in lemmatized_tokens]

    # Stampa dei token dopo il processo di Stemming
    print(stemmed_tokens)