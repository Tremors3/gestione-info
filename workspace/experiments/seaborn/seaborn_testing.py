#   document_id  punteggio_rilevanza  rilevanza_normalizzata
# 0     rfc1234             6.577324                       3
# 1     rfc2345             2.261860                       0
# 3     rfc4567             1.439483                       0

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
sns.set_theme("notebook")

# Creazione di un dizionario
data = {
    'document_id':["rfc1234","rfc2345","rfc4567"],
    'punteggio_rilevanza':[6.577324,2.261860,1.439483],
    'rilevanza_normalizzata':[3,0,0]
}

# Creazione del DataFrame
df = pd.DataFrame(data)

# Riorganizzazione dei dati in formato lungo
df_melted = df.melt(id_vars='document_id', 
                     value_vars=['punteggio_rilevanza', 'rilevanza_normalizzata'], 
                     var_name='metrica', 
                     value_name='valore')
print(df_melted)
# Creazione dell'istogramma
plt.figure(figsize=(8, 6))  # Imposta la dimensione della figura
bar_plot = sns.barplot(data=df_melted, x='document_id', y='valore', hue='metrica')

# Aggiunta di un titolo e etichette
plt.title("Istogramma di Punteggio di Rilevanza e Rilevanza Normalizzata")
plt.xlabel("Document ID")
plt.ylabel("Valore")
plt.legend(title='Metrica')

# Aggiunta dei valori sopra le barre
for p in bar_plot.patches:
    bar_plot.annotate(f'{p.get_height():.2f}' if p.get_height() != 0 else '', 
                      (p.get_x() + p.get_width() / 2., p.get_height()), 
                      ha='center', va='bottom', 
                      fontsize=10, color='black', 
                      xytext=(0, 2),
                      textcoords='offset points')

# Mostra il grafico
plt.show()