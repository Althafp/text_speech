import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os

# Define the URL of the webpage to scrape
url = 'https://indianexpress.com/section/india/'

# Sending a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first div element with the class 'articles'
    first_article = soup.find('div', class_='articles')

    # If first article is found
    if first_article:
        # Find the h2 tag with class 'title' within the div with class 'img-context'
        h2_title = first_article.find('div', class_='img-context').find('h2', class_='title')
        if h2_title:
            # Find the <a> tag within the h2_title
            a_tag = h2_title.find('a')
            if a_tag:
                # Extract and store the title
                title = a_tag.text.strip()

        # Find all <p> tags within the first article div and extract text
        p_tags = first_article.find_all('p')
        summary = ""
        for p in p_tags:
            # Extract and append to summary
            summary += p.text.strip() + "\n"
            print(summary)

        # Convert the summary to audio
        tts = gTTS(text=summary, lang='en')
        tts.save("article_summary.mp3")

        # Play the audio
        os.system("start article_summary.mp3")

    else:
        print("No articles found.")
else:
    print("Failed to retrieve the webpage.")
