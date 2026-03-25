import requests
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        metric = query.get('metric', ['citations'])[0]
        
        # Get your API key from environment variables for security
        api_key = os.environ.get('SERPAPI_KEY')
        author_id = "RqoQgLYAAAAJ"
        
        url = f"https://serpapi.com/search?engine=google_scholar_author&author_id={author_id}&hl=en&api_key={api_key}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            stats = data.get('cited_by', {}).get('table', [])
            
            if metric == 'citations':
                value = str(stats[0].get('citations', {}).get('all', 0))
                label = "Citations"
                color = "blue"
            elif metric == 'h_index':
                value = str(stats[1].get('h_index', {}).get('all', 0))
                label = "h-index"
                color = "orange"
            elif metric == 'i10_index':
                value = str(stats[2].get('i10_index', {}).get('all', 0))
                label = "i10-index"
                color = "brightgreen"
            else:
                value = "error"
                label = "metric"
                color = "red"

            result = {
                "schemaVersion": 1,
                "label": label,
                "message": value,
                "color": color
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Cache-Control', 's-maxage=3600, stale-while-revalidate') # Cache for 1 hour
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
        return
