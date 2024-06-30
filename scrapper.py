import requests
from bs4 import BeautifulSoup
import stanza
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter
# Initialize Stanza NLP pipeline
stanza.download('en')
nltk.download('stopwords')
nlp = stanza.Pipeline('en', processors='tokenize,pos')

# Function to extract text from a URL
def extract_text_from_url(url):
    try:
        print(f"Fetching  {url}")
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract visible text from HTML using BeautifulSoup
        text = ' '.join(soup.stripped_strings)
        return text
    except Exception as e:
        print(f"Error fetching content from {url}: {str(e)}")
        return None

# Function to identify relevant topics in the text
def identify_topics(text):
    # Tokenize and process the text
    doc = nlp(text)
    
    # Create a list of nouns (NN and NNS tags) from the processed text
    # nouns = [word.text.lower() for sent in doc.sentences for word in sent.words if re.match(r'^NN', word.upos)]
    nouns = []
    for sentence in doc.sentences:
        for word in sentence.words:
            if "NN" in word.xpos:
                nouns.append(word.text.lower())
    # You can add additional logic to filter and rank topics as per your requirements
    stop_words = set(stopwords.words('english'))
    nouns = [word for word in nouns if word not in stop_words]
    print(len(nouns))
    print(len(set(nouns)))
    return nouns

# Main function to classify and identify topics from a URL
def classify_url(url):
    text = extract_text_from_url(url)
    if text:
        print("Extracing topics..")
        topics = identify_topics(text)
        return list(topics)
    else:
        print("Topics not found")
        return []

def get_top_words(topics, n=10):
    word_counts = Counter(topics)
    top_words = word_counts.most_common(n)

    return [word[0] for word in top_words]
    # return top_words

# Testing with sample URLs
# sample_urls = [
#     "http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster",
#     "http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/",
#     "http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/"
# ]
sample_urls = [
    "http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/",
]

for url in sample_urls:
    topics = classify_url(url)
    top_words = get_top_words(topics, n=10)
    print(f"URL: {url}")
    print(f"Topics: {', '.join(top_words)}")
    print("\n")

