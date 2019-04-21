# Importing all packages
import re, unicodedata
import nltk
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from nltk.corpus import stopwords
import gensim

# Creating class DataCleaning. This class has methods that cleans that performs basic data cleaning operations such as removing non ASCII characters, removing punctuations, removing stopwords and many more.
class DataCleaning:
    
    """DataCleaning has following attributes:
            words: A list of tokenized words of a document.
            
    """
    
    def __init__(self, words):
        self.words = words
    
    def remove_non_ascii(self):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in self.words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words
    
    def to_lowercase(self):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in self.words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    def remove_punctuation(self):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in self.words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def remove_stopwords(self):
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in self.words:
            if word not in stopwords.words('english'):
                new_words.append(word)
        return new_words

    def remove_numbers(self):
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in self.words:
            new_word = re.sub(r'\S*\d+\S*', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def remove_single_letter(self):
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in self.words:
            new_word = re.sub(r'^\w{1}$', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words
