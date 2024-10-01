import scrapy
from scrapy.crawler import CrawlerProcess
from facebook_scraper import get_posts
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

class FacebookSpider(scrapy.Spider):
    name = "facebook"

    def start_requests(self):
        page_name = "pubity"  # Change this to the desired Facebook page name
        num_posts = 5  # Number of posts to scrape
        try:
            for post in get_posts(page_name, pages=num_posts):
                if 'post_url' in post:
                    yield scrapy.Request(url=post['post_url'], callback=self.parse)
        except Exception as e:
            self.logger.error("Error:", e)

    def parse(self, response):
        title, description = self.scrape_web_page(response.url)
        yield {
            'url': response.url,
            'title': title,
            'description': description
        }

    def scrape_web_page(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title').text.strip() if soup.find('title') else "N/A"
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description.get('content').strip() if meta_description else "N/A"
            return title, description
        except Exception as e:
            self.logger.error("Error scraping page:", e)
            return "N/A", "N/A"

class FacebookInfluencerIdentifier:
    @staticmethod
    def identify_facebook_influencers(page_name, num_posts, min_likes=1000):
        influencers = defaultdict(int)
        try:
            for post in get_posts(page_name, pages=num_posts):
                if 'likes' in post and post['likes'] >= min_likes:
                    influencers[post['username']] += 1
        except Exception as e:
            print("Error:", e)
        return influencers

if __name__ == "__main__":
    # Task 2: Writing an application for social media mining using Scrapy
    print("Scraping web pages using Scrapy...")
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'LOG_ENABLED': False  # Disable logging for simplicity
    })
    process.crawl(FacebookSpider)
    process.start()

    # Task 3: Identifying Facebook influencers
    print("\nIdentifying Facebook influencers...")
    page_name = "pubity"  # Change this to the desired Facebook page name
    num_posts = 5  # Number of posts to scrape
    influencers = FacebookInfluencerIdentifier.identify_facebook_influencers(page_name, num_posts)
    print("Facebook influencers:")
    for username, count in influencers.items():
        print(f"User: {username}, Posts: {count}")
