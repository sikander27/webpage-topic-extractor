import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import stanza
import nltk
from nltk.corpus import stopwords
from collections import Counter


class URLTopicExtractor:
    def __init__(self, urls=[], max_topics=10):
        # Initialize Stanza NLP pipeline
        stanza.download('en')
        nltk.download('stopwords')
        self.nlp = stanza.Pipeline('en', processors='tokenize,pos')
        self.urls = urls
        self.data = []
        self.max_topics = max_topics

    def extract_text_from_url(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join(soup.stripped_strings)
            # TODO: Handle anti scrapping mechanisms like captcha
            return text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {url}: {str(e)}")
            return None

    def identify_topics(self, text):
        # Creating tokens
        doc = self.nlp(text)
        
        # Create a list of nouns (NN and NNS tags) from the processed text
        nouns = [word.text.lower() for sent in doc.sentences for word in sent.words if "NN" in word.xpos]
        
        # Remove stopwords from the list
        stop_words = set(stopwords.words('english'))
        nouns = [word for word in nouns if word not in stop_words]
        
        return nouns

    def extract_topics(self):
        print("Extracing topics...")
        for url in self.urls:
            print(f"Extracting text from {url}...")
            text = self.extract_text_from_url(url)
            row = {"URL": url}
            if text:
                print("Identifying Topics...")
                topics = self.identify_topics(text)
                top_topics = self.get_top_words(topics)
                row["Topics"] = top_topics
            else:
                print("Data not found")
                row["Topics"] = []
            self.data.append(row)
        return self.data

    def create_csv(self):
        print("Creating CSV....")
        if not self.data:
            self.extract_topics()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"topics_{timestamp}.csv"
        with open(filename, "w", newline="") as csvfile:
            fieldnames = ["URL", "Topics"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)

    def get_top_words(self, topics):
        word_counts = Counter(topics)
        top_words = word_counts.most_common(self.max_topics)
        return ', '.join([word[0] for word in top_words])

# Testing the URLTopicExtractor class
if __name__ == "__main__":
    sample_urls = [
        "http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/",
        "http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/"
    ]
    url_extractor = URLTopicExtractor(sample_urls)
    url_extractor.extract_topics()
    url_extractor.create_csv()
    for row in url_extractor.data:
        print("-------------------------------------------------------")
        print(f"URL: {row['URL']}")
        print(f"Top Topics: {row['Topics']}")
    # for url in sample_urls:
    #     topics = url_extractor.extract_topics_from_url(url)
    #     top_words = url_extractor.get_top_words(topics, n=10)
    #     print(f"URL: {url}")
    #     print(f"Top 10 Common Words: {top_words}")
    #     print("\n")
