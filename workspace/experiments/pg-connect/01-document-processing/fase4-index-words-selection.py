import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer

"""
Testing della funzionalità di selezione delle parole indice (Index Words Selection).
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

    """ Fase 4: Selezione delle parole indice (Parser & Tagger) """

    # Effettua il Part-Of-Speech (POS) tagging dei token stemmati
    # La funzione nltk.pos_tag() restituisce una lista di tuple dove:
    # - il primo elemento della tupla è il token,
    # - il secondo elemento è il tag grammaticale (es. NN per i nomi).
    tagged_tokens = nltk.pos_tag(stemmed_tokens) # Tagger

    # Stampa i token con i relativi tag grammaticali
    print(tagged_tokens)

    # Inizializza una lista vuota per memorizzare i token selezionati come parole indice
    index_tokens = []

    # Ciclo su ogni tupla (token, tag grammaticale) nella lista di token taggati
    for token in tagged_tokens:
        # Controlla se il tag grammaticale inizia con 'NN' (che indica i nomi, o 'nouns' in inglese)
        # token[0] è il token (parola), token[1] è il tag POS. Confrontiamo i primi due caratteri del tag ('NN')
        if token[1][0:2] == 'NN':
            index_tokens.append(token[0])

    # Stampa i token selezionati come parole indice (cioè i nomi)
    print(index_tokens)