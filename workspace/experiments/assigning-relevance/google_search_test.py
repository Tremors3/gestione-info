from googlesearch import search

# Esegui una ricerca su Google
results = search("QUIC protocol site:rfc-editor.org", num_results=200)

# Filtra solo i link che corrispondono a un criterio (es. dominio "rfc-editor.org")
filtered_links = [link for link in results if "rfc-editor.org" in link]

links_size = len(filtered_links)

print(f"Link filtrati ({links_size}):", *[link for link in filtered_links], sep='\n')