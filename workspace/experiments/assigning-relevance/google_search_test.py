from googlesearch import search

# Esegui una ricerca su Google
results = search("QUIC protocol site:rfc-editor.org", num_results=200)

# Filtra solo i link che corrispondono a un criterio (es. dominio "rfc-editor.org")
filtered_links = [link for link in results if "rfc-editor.org" in link]

print("Link filtrati:")
for link in filtered_links:
    #if link.split(".")[-1] == "html":
    print(link)
print(len(filtered_links))


















