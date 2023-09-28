# URL Topic Classifier

The URL Topic Classifier is a Python script that extracts and classifies topics from a list of web URLs. It uses natural language processing (NLP) to analyze the content of the web pages and identify relevant topics. This README provides information on prerequisites, installation, and usage of the script.

## Prerequisites

Before you can run the URL Topic Classifier, ensure that you have the following prerequisites installed on your system:

1. **Python>=3.7**: The script is written in Python `3.9`, so you'll need a Python interpreter. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/).

2. **Required Python Libraries**: You'll need to install several Python libraries to run the script. These libraries include:
   - `requests`: To make HTTP requests.
   - `BeautifulSoup`: For parsing HTML content.
   - `stanza`: For natural language processing (NLP).
   - `nltk`: For working with natural language text.
   - `csv`: For handling CSV files.

   You can install these libraries using `pip`. For example:

   ```
   pip install requirements.txt
   ```
   
3. **Download Required models**: 
    - `nltk corpos stopwords` from  https://github.com/nltk/nltk_data/blob/gh-pages/packages/corpora/stopwords.zip


## Installation
Follow these steps to install and set up the URL Topic Classifier:
1. Clone this repository to your local machine:

```
git clone https://github.com/sikander27/webpage-topic-extractor.git
```

2. Change to the project directory:

```
cd webpage-topic-extractor
```


## How to Run
1. Open the main.py file in a text editor.

2. Modify the sample_urls list to include the URLs you want to analyze:


```
sample_urls = [
    "http://example.com/page1",
    "http://example.com/page2",
    # Add more URLs here
]
```

3. Save the changes to the script.

4. Open a terminal or command prompt and navigate to the project directory.

5. Run the script using Python:

```
python main.py
```

6. The script will extract topics from the specified URLs and create a CSV file containing the results. The CSV file will be named something like `topics_YYYYMMDDHHMMSS.csv`, where `YYYYMMDDHHMMSS` represents the timestamp.


## Configuration and Customization
You can customize the behavior of the URL Topic Classifier by modifying the following variables in the script:

- `max_topics``: The maximum number of top topics to consider.
- User-agent in the headers variable inside the extract_text_from_url function for HTTP requests.


## Troubleshooting
If you encounter any issues or errors while running the script, please check the following:

- Ensure that you have installed all the required Python libraries mentioned in the `Prerequisites` section.
- Verify that the URLs you provided in the sample_urls list are correct and accessible.