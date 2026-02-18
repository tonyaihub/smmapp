import requests
import json

def find_keywords(niche, num_keywords=30):
    # Use SERP API for low-competition keywords
    params = {
        'api_key': config.SERPAPI_KEY,
        'q': f'{niche} low competition keywords',
        'num': num_keywords
    }
    response = requests.get('https://serpapi.com/search', params=params)
    data = json.loads(response.text)
    keywords = [result['title'] for result in data.get('organic_results', [])]  # Extract relevant keywords
    return keywords[:num_keywords]  # Return 30 for monthly plan

def analyze_competitors(keyword):
    # Simple scrape top results
    from bs4 import BeautifulSoup
    params = {'api_key': config.SERPAPI_KEY, 'q': keyword}
    response = requests.get('https://serpapi.com/search', params=params)
    data = json.loads(response.text)
    top_urls = [result['link'] for result in data.get('organic_results', [])[:3]]
    # Analyze lengths, headings, etc. (expand with BS4 parsing)
    return top_urls