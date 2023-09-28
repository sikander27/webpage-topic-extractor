import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
import stanza
import nltk
from nltk.corpus import stopwords
from collections import Counter


class URLTopicClassifier:
    """
    A class for extracting and classifying topics from a list of URLs.

    Attributes:
        urls (list): List of URLs to analyze.
        max_topics (int): Maximum number of top topics to consider.

    Methods:
        extract_text_from_url(url): Extract text content from a given URL.
        identify_topics(text): Identify relevant topics from a given text.
        extract_topics(): Extract topics from specified URLs and store the data.
        create_csv(): Create a CSV file containing URL and corresponding topics data.
        get_top_words(topics): Get the top common words from a list of topics.
    """
    def __init__(self, urls=[], max_topics=10):
        """
        Initialize the URLTopicClassifier.

        Args:
            urls (list): List of URLs to analyze.
            max_topics (int): Maximum number of top topics to consider.
        """
        # Initialize Stanza NLP pipeline
        stanza.download("en")
        nltk.download("stopwords")
        self.nlp = stanza.Pipeline("en", processors="tokenize,pos")
        self.urls = urls
        self.data = []
        self.max_topics = max_topics

    def extract_text_from_url(self, url):
        """
        Extract visible text content from a given URL.

        Args:
            url (str): The URL to extract text from.

        Returns:
            tuple : Extracted text content from the URL and meta content
        """
        try:
            # Add Cookie support
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            }
            # TODO: Handle anti-scrapping mechanisms like captcha for websites like Amazon.
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            meta_topics = []
            for tag in ("description", "keywords", "title"):
                meta_data = soup.find("meta", attrs={"name": tag})
                if meta_data:
                    meta_topics.append(meta_data.get("content", ""))

            text = " ".join(soup.stripped_strings)

            return text, " ".join(meta_topics)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching content from {url}: {str(e)}")
            return None

    def identify_topics(self, text):
        """
        Identify relevant topics from a given text.

        Args:
            text (str): The text to analyze.

        Returns:
            list: List of identified topics.
        """
        # Creating tokens
        doc = self.nlp(text)

        # Create a list of nouns (NN and NNS tags) from the processed text
        nouns = [
            word.text.lower()
            for sent in doc.sentences
            for word in sent.words
            if "NN" in word.xpos
        ]

        # Remove stopwords from the list
        stop_words = set(stopwords.words("english"))
        nouns = [word for word in nouns if word not in stop_words]

        return nouns

    def extract_topics(self):
        """
        Extract topics from the specified URLs and store the data.

        Returns:
            list: List of dictionaries containing URL and corresponding topics.
        """
        print("Extracting topics...")
        for url in self.urls:
            print(f"Extracting text from {url}...")
            text, meta_text = self.extract_text_from_url(url)
            row = {"URL": url}
            if text:
                print("Identifying topics...")
                topics = self.identify_topics(text)
                meta_topics = self.identify_topics(meta_text)
                top_topics = self.get_top_words(topics, meta_topics)
                row["Topics"] = top_topics
            else:
                print("Data not found")
                row["Topics"] = []
            self.data.append(row)
        return self.data

    def create_csv(self):
        """
        Create a CSV file containing URL and corresponding topics data.
        """
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

    def get_top_words(self, topics, meta_topics=[]):
        """
        Get the top common words from a list of topics and meta_topics.

        This function calculates the most common words in a list of topics and returns a
        comma-separated string of the top words. Meta_topics, if provided, will not be
        considered in the max count when determining the top words.
        So the output will be `meta topics count + max count`

        Args:
            topics (list): A list of topics to analyze.
            meta_topics (list, optional): Additional topics that are not considered
                when calculating the top words. Defaults to an empty list.

        Returns:
            str: A comma-separated list of the most common words in the 'topics'  and 'meta_topics' list.
        """
        word_counts = Counter(topics)
        top_words = word_counts.most_common(self.max_topics)
        return ", ".join(dict.fromkeys(meta_topics + [word[0] for word in top_words]))


# Testing the URLTopicClassifier class
if __name__ == "__main__":
    sample_urls = [
        "http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster",
        "http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/",
        "http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/",
        "https://www.freecodecamp.org/news/how-to-write-a-good-software-design-document-66fcf019569c/"
    ]
    url_extractor = URLTopicClassifier(sample_urls)
    url_extractor.extract_topics()
    # If you need data in csv format
    url_extractor.create_csv()
    for row in url_extractor.data:
        print("-------------------------------------------------------")
        print(f"URL: {row['URL']}")
        print(f"Top Topics: {row['Topics']}")
