import nltk
from nltk.corpus import stopwords

"""
Testing della funzionalità delle Stop Words.
Questo script dimostra come rimuovere le parole di stop da una frase.
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
    
    # Stampa dei token senza le stopwords
    print(non_stopword_tokens)