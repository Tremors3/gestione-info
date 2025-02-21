from serpapi import GoogleSearch

search = GoogleSearch({
    "q": "coffee", 
    "location": "Austin,Texas",
    "api_key": "<your secret api key>"
})

result = search.get_dict()