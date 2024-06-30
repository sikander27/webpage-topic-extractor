import nltk
import stanza
import requests
import stanfordnlp
from bs4 import BeautifulSoup


# stanfordnlp.download("en")
# stanford_nlp_path = "path/to/stanfordnlp/models/english"

stanford_nlp_path = "/Users/sikanderkhan/stanfordnlp_resources/"
# nlp = stanfordnlp.Pipeline(models_dir=stanford_nlp_path, processors="tokenize,pos,lemma")

nlp = stanza.Pipeline('en', processors='tokenize,mwt,pos,lemma')
# nlp = stanfordnlp.Pipeline()

def extract_topics_from_url(url):
    try:
        print(f"Fetching {url}")
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)
        print(response.status_code)
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')
        webpage_text = soup.get_text()

        # Tokenize the text using Stanford NLP
        doc = nlp(webpage_text)

        # import pdb; pdb.set_trace()

        # # Extract relevant topics (e.g., nouns) from the parsed text
        relevant_topics = []
        keywords = []
        for sentence in doc.sentences:
            for token in sentence.tokens:
                if "NN" in token.words[0].xpos:
                    relevant_topics.append(token.words[0].text)
                if token.words[0].text in ["Cuisinart", "Toaster"]:
                    keywords.append(token.words[0])

        # # Remove stopwords using NLTK
        # stop_words = set(nltk.corpus.stopwords.words('english'))
        relevant_topics = [topic for topic in relevant_topics]
        # relevant_topics = [topic for topic in relevant_topics if topic.lower() not in stop_words]
        print(len(relevant_topics))

        print(len(set(relevant_topics)))
        print("--------keywords-----------")
        print(keywords)
        return set(relevant_topics)

    except Exception as e:
        print(e)
        return str(e)
    

url_list = [
    "http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster",
    "http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/",
    "http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/"
]
# url = "http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster"

data = extract_topics_from_url(url_list[1])
print(data)
# for url in url_list:
#     topics = extract_topics_from_url(url)
    # print(f"URL: {url}")
    # print(f"Topics: {topics}")
    # print()