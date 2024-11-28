from urllib.parse import urljoin  # Importing module for URL manipulation
import requests  # Importing module for sending HTTP requests
from bs4 import BeautifulSoup  # Importing module for web scraping

from pprint import pprint

class Crawler:
    def __init__(self, urls=[]):
        """
        Constructor for the Crawler class.
        """
        self.visited_urls = []  # List to store visited URLs
        self.urls_to_visit = urls  # List to store URLs yet to be visited

    def download_url(self, url):
        """
        Function to download the content of a webpage given its URL.
        """
        return requests.get(url).text  # Sending a GET request to the URL and returning the HTML content

    def get_linked_urls(self, url, html):
        """
        Function to extract linked URLs from the HTML content of a webpage.
        """
        soup = BeautifulSoup(html, 'html.parser')  # Creating a BeautifulSoup object
        for link in soup.find_all('a'):  # Finding all <a> tags in the HTML
            path = link.get('href')  # Getting the 'href' attribute of the <a> tag
            if path and path.startswith('/'):  # Checking if the URL is relative
                path = urljoin(url, path)  # Resolving the relative URL
            yield path  # Yielding the resolved URL

    def add_url_to_visit(self, url):
        """
        Function to add a URL to the list of URLs to visit if it has not been visited before.
        """
        if url not in self.visited_urls and url not in self.urls_to_visit:  # Checking if the URL is not already visited or in the list of URLs to visit
            self.urls_to_visit.append(url)  # Adding the URL to the list of URLs to visit

    def crawl(self, url):
        """
        Function to crawl a webpage by downloading its content and extracting linked URLs.
        """
        html = self.download_url(url)  # Downloading the content of the webpage
        for url in self.get_linked_urls(url, html):  # Iterating through linked URLs found in the webpage
            self.add_url_to_visit(url)  # Adding each linked URL to the list of URLs to visit

    def run(self):
        """
        Function to start the crawling process.
        """
        while self.urls_to_visit:  # Loop until there are URLs to visit
            url = self.urls_to_visit.pop(0)  # Get the next URL to visit from the list
            try:
                self.crawl(url)  # Crawling the webpage
            except Exception:
                print(f'Failed to crawl: {url}')  # Handling exceptions
            finally:
                self.visited_urls.append(url)  # Adding the visited URL to the list of visited URLs

if __name__ == '__main__':
    
    c = Crawler(urls=['https://www.giallozafferano.it/'])
    try:
        c.run()  # Creating an instance of the Crawler class and starting the crawling process with IMDb's homepage as the starting URL
    except KeyboardInterrupt:
        pprint(c.visited_urls)
    