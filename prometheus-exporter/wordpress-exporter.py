import time
import requests
from prometheus_client import start_http_server, Gauge
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
URL = os.getenv("URL_WORDPRESS")
WORDPRESS_URL = "https://"+URL+"/wp-json/wp/v2"
EXPORTER_PORT = 8000
SCRAPE_INTERVAL = 15  # in seconds

# Prometheus metrics
post_count_gauge = Gauge('wordpress_post_count', 'Number of posts in WordPress')
page_count_gauge = Gauge('wordpress_page_count', 'Number of pages in WordPress')
comment_count_gauge = Gauge('wordpress_comment_count', 'Number of comments in WordPress')

def fetch_wordpress_data():
    try:
        # Fetch post count
        response = requests.get(f"{WORDPRESS_URL}/posts")
        response.raise_for_status()
        post_count = len(response.json())
        post_count_gauge.set(post_count)

        # Fetch page count
        response = requests.get(f"{WORDPRESS_URL}/pages")
        response.raise_for_status()
        page_count = len(response.json())
        page_count_gauge.set(page_count)

        # Fetch comment count
        response = requests.get(f"{WORDPRESS_URL}/comments")
        response.raise_for_status()
        comment_count = len(response.json())
        comment_count_gauge.set(comment_count)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from WordPress: {e}")

if __name__ == "__main__":
    # Start the Prometheus exporter server
    start_http_server(EXPORTER_PORT)
    print(f"Exporter running on port {EXPORTER_PORT}")

    # Fetch data and update metrics at the specified interval
    while True:
        fetch_wordpress_data()
        time.sleep(SCRAPE_INTERVAL)
