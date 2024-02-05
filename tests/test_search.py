from src.plant_puller.util.search import google_search

def test_google_search(query="What are the best houseplants"):
  results = google_search(query)
  print(results)
  assert len(results) != 0