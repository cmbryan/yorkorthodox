import requests
from bs4 import BeautifulSoup
import os
import pytest
import socketserver
import threading
from urllib.parse import urljoin
import http.server


SITE_URL = os.environ["SITE_URL"]


@pytest.fixture(scope="module")
def http_server():
    # Set the IP address and port you want the server to listen on
    protocol, url = SITE_URL.split("://")
    host, port = url.split(":")

    # Create a handler for the server
    handler = http.server.SimpleHTTPRequestHandler

    # Create the server with the specified host and port
    try:
        with socketserver.TCPServer((host, int(port)), handler) as httpd:
            # Start the server in a separate thread
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()

            # Provide the server URL to the test
            yield f"http://{host}:{port}"

    except OSError as e:
        # Already running (e.g. in a dev environment)
        yield f"http://{host}:{port}"


def assert_valid(url):
    response = requests.head(url)
    assert response.status_code == 200, f"Invalid URL: {url}"


@pytest.mark.parametrize(
    "page,",
    [
        ("/"),
    ]
)
def test_page_links(http_server, page):
    # Send an HTTP GET request to the URL
    url = urljoin(SITE_URL, page)
    response = requests.get(url)
    response.raise_for_status()

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all hrefs
    hrefs = filter(lambda href: href and href != "javascript:void(0);",
                map(lambda a: a.get('href'), soup.find_all('a')))

    # Validate each link
    for href in hrefs:
        # Construct an absolute URL if it's a relative URL
        absolute_url = urljoin(SITE_URL, href)
        response = requests.head(absolute_url)
        assert response.status_code == 200, f"Invalid URL: {absolute_url}"
