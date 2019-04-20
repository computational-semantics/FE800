#!/usr/bin/env python
# coding: utf-8



import re, unicodedata
import nltk
from nltk.corpus import stopwords
import spacy
nlp = spacy.load('en', disable=['parser', 'ner'])
import gensim


#remove ASCII words, lower the letter, punctuation,stopwords,single letter, numbers

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words

def remove_single_letter(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'^\w{1}$', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def remove_numbers(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'\S*\d+\S*', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_stopwords(words)
    words = remove_single_letter(words)
    words = remove_numbers(words)
    return words


def DC(texts):
    df = []
    for d in texts[0:len(texts)]:
        words = normalize(nltk.word_tokenize(d))
        res = " ".join(words)
        df.append(res)
    return df


#Make sentence to words and make it to list

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations


def word_list(texts):
    df = list(sent_to_words(texts))
    return df



#make bigrams and trigrams

def make_bigrams(texts):
    bigram = gensim.models.Phrases(texts, min_count=5, threshold=100) # higher threshold fewer phrases.
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):

    bigram = gensim.models.Phrases(texts, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[texts], threshold=100)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    return [trigram_mod[doc] for doc in texts]


#lemmatization


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out





