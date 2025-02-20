import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from esercizi.Esercizio1 import acquire_test

"""
Script per:
1. Tokenizzazione e POS tagging
2. Conversione dei token in minuscolo
3. Rimozione delle stopwords
4. Applicazione di lemmatizzazione e stemming (solo per i nomi - NN)
"""

if __name__ == "__main__":
    
    # Lista di URL da cui scaricare i testi
    urls = ["https://www.gutenberg.org/files/2554/2554-0.txt", 
            "https://www.gutenberg.org/files/66419/66419-0.txt"]
    
    # Esempio di frase
    #sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
    sentence  = acquire_test(urls[0])

    # Crea le istanze per lemmatizzazione e stemming
    wnl = nltk.WordNetLemmatizer()
    porter_stemmer = PorterStemmer()

    # Recupera le stopwords inglesi una sola volta
    stop_words = set(stopwords.words('english'))

    # Inizializza la lista per le parole indice (nomi)
    index_tokens = []

    # 1. Tokenizzazione e POS tagging
    for token, tag in nltk.pos_tag(nltk.word_tokenize(sentence)):
        
        # 2. Converte il token in minuscolo
        token = token.lower()
        
        # 3. Rimuove le stopwords
        if token not in stop_words:
            
            # 4. Se il tag è di tipo nome (NN), applica lemmatizzazione e stemming
            if tag.startswith('NN'):
                
                lemmatized_token = wnl.lemmatize(token)  # Lemmatizza il token
                
                stemmed_token  = porter_stemmer.stem(lemmatized_token)  # Applica lo stemming
                
                index_tokens.append(stemmed_token)  # Aggiungi il token alla lista delle parole indice
    
    # Stampa il risultato finale
    print(index_tokens)