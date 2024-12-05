from serpapi import GoogleSearch

params = {
  "api_key": "bde68af028f42fd86a8a2b92977ffa46be487b89e0c2d153046df57a5d2129a2",
  "engine": "google_scholar_author",
  "hl": "en",
  "author_id": "RqoQgLYAAAAJ"
}

search = GoogleSearch(params)
results = search.get_dict()
