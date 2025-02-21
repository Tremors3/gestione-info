import nltk

"""
Testing della funzionalità di Word Tokenize.
Questa funzione suddivide una frase in parole (token).
"""

if __name__ == "__main__":
    
    """ Fase 1: Tokenizzazione """
    
    # Definizione della frase di esempio
    sentence = "At eight o'clock on Thursday morning Arthur didn't feel very good."
    
    # Tokenizzazione della frase in parole (token)
    tokens = nltk.word_tokenize(sentence)
    
    # Conversione di tutti i token in minuscolo
    tokens = [token.lower() for token in tokens]
    
    print(tokens)