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
            
            # The structure in google_scholar_nathan.json is:
            # "cited_by": { "table": [ {"citations": {"all": 76...}}, {"h_index": {"all": 3...}}, {"i10_index": {"all": 2...}} ] }
            stats_table = data.get('cited_by', {}).get('table', [])
            
            value = "0"
            label = "metric"
            color = "blue"

            if metric == 'citations' and len(stats_table) > 0:
                value = str(stats_table[0].get('citations', {}).get('all', 0))
                label = "Citations"
                color = "blue"
            elif metric == 'h_index' and len(stats_table) > 1:
                value = str(stats_table[1].get('h_index', {}).get('all', 0))
                label = "h-index"
                color = "orange"
            elif metric == 'i10_index' and len(stats_table) > 2:
                value = str(stats_table[2].get('i10_index', {}).get('all', 0))
                label = "i10-index"
                color = "brightgreen"

            result = {
                "schemaVersion": 1,
                "label": label,
                "message": value,
                "color": color
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            # Cache for 1 hour to stay within SerpApi limits
            self.send_header('Cache-Control', 's-maxage=3600, stale-while-revalidate')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
        return
