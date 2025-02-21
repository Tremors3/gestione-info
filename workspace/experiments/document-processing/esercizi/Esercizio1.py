from urllib import request
import ssl

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

def acquire_test(url: str) -> str:
    """
    Acquisisce il testo da un URL fornito e lo restituisce come stringa.
    
    Parametri:
    url (str): L'URL del testo da scaricare.
    
    Ritorna:
    str: Il contenuto del testo recuperato dall'URL, decodificato in UTF-8.
    """
    
    # Creazione di un contesto SSL che non verifica i certificati, necessario per evitare errori SSL
    context = ssl._create_unverified_context()
    
    # Apertura dell'URL con il contesto SSL non verificato
    response = request.urlopen(url, context=context)
    
    # Lettura del contenuto e decodifica come UTF-8
    return response.read().decode('utf8')

if __name__ == '__main__':
    
    # Lista di URL da cui scaricare i testi
    urls = ["https://www.gutenberg.org/files/2554/2554-0.txt", 
            "https://www.gutenberg.org/files/66419/66419-0.txt"]
    
    # Acquisizione del testo dal secondo URL della lista
    text = acquire_test(urls[1])
    
    # Stampa dei primi cinquecento caratteri del testo acquisito
    #print(text[:500])
    
    """ Fase 1: Tokenizzazione """
    
    # Tokenizzazione della frase in parole (token)
    tokens = nltk.word_tokenize(text)
    
    # Conversione di tutti i token in minuscolo
    tokens = [token.lower() for token in tokens]
    
    # Stampa dei tokens individuati
    print("Tokens before elimination of stopwords: \n", tokens)
    
    """ Fase 2: Rimozione delle stopwords """
    
    # Recupero delle stopwords in inglese
    stop_words = set(stopwords.words('english'))
    
    # Rimozione delle stopwords dai token
    non_stopword_tokens = [token for token in tokens if token not in stop_words]
    
    # Stampa dei tokens dopo la rimozione delle stopwords
    print("Tokens after elimination of stopwords: \n", non_stopword_tokens)
    
    """ Fase 4: Selezione delle parole indice (Parser & Tagger) """

    # Effettua il Part-Of-Speech (POS) tagging dei token stemmati
    tagged_tokens = nltk.pos_tag(non_stopword_tokens)
    
    # Stampa i token con i relativi tag grammaticali
    print("Tokens with their tags before noun selection: \n", tagged_tokens)

    index_tokens = []
    # Ciclo su ogni tupla (token, tag grammaticale) nella lista di token taggati
    # Controlla se il tag grammaticale inizia con 'NN' (che indica i nomi)
    for token in tagged_tokens:
        if token[1][0:2] == 'NN':
            index_tokens.append(token[0])

    # Stampa i token selezionati come parole indice (cioè i nomi)
    print("Tokens after noun selection: \n", index_tokens)
    
    """ Fase 3b: Stemming dei token """

    # Crea le istanze degli stemmer
    porter_stemmer = PorterStemmer()  # Porter Stemmer
    lancaster_stemmer = LancasterStemmer()  # Lancaster Stemmer

    # Variabile per scegliere lo stemmer da utilizzare
    use_porter_stemmer = True

    # Stemming dei token lemmatizzati utilizzando lo Stemmer scelto
    if use_porter_stemmer:
        stemmed_tokens = [porter_stemmer.stem(token) for token in index_tokens]
    else:
        stemmed_tokens = [lancaster_stemmer.stem(token) for token in index_tokens]
    
    print("Token after stemming: \n", stemmed_tokens)