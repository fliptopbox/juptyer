

# %% [markdown]
# Following the article posted here.
# https://stackabuse.com/text-summarization-with-nltk-in-python/

import bs4 as bs
import urllib.request
import re
import nltk
import heapq

nltk.download('punkt')
nltk.download('stopwords')


# %% [markdown]
# ## Slurp an artivle off the Internet

URL = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
scraped_data = urllib.request.urlopen(URL)
article = scraped_data.read()

article = '''
So, keep working. Keep striving. Never give up. Fall down seven times, get up eight. Ease is a greater threat to progress than hardship. Ease is a greater threat to progress than hardship. So, keep moving, keep growing, keep learning. See you at work.
'''


print(len(article))

# %% [markdown]
# ## Parse the HTML into plain text blocks

parse_article = bs.BeautifulSoup(article, 'lxml')
paragraphs = parse_article.find_all('p')
article_text = ""

for p in paragraphs:
    article_text += p.text

# ## Remove the [1] artifacts from the text
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)

# ## Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

print(article_text)


# %% [markdown]
# ## Convert the article into sentences
# Remember nltk needs Punkt corpus, a pre-trained model for English and it also needs the stopword dictionary
# Both assets need to be downloaded

sentence_list = nltk.sent_tokenize(article_text)
stopwords = nltk.corpus.stopwords.words('english')

print(len(stop_words))

word_frequencies = {}

for word in nltk.word_tokenize(formatted_article_text):
    if word not in word_frequencies.keys():
        word_frequencies[word] = 0

    word_frequencies[word] += 1

print(word_frequencies)


# %% [markdown]
# ## Assign the word weight by normalizing the counts to the max frequent word

maximum_frequency = max(word_frequencies.values())
print("Maximum word use", maximum_frequency)

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word] / maximum_frequency)


# %% [markdown]
# ## Iterate over the sentences and give them importance
# The improtance is based on most frequent words occuring in a given sentence

sentence_scores = {}
max_word_per_sentence = 20

for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < max_word_per_sentence:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]


# %% [markdown]
# ## Summerize the results
summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
summary = ' '.join(summary_sentences)

# ## And the summary is ....
print(summary)

# %%
