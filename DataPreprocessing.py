
import DataClean
import glob
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim
from nltk.stem import WordNetLemmatizer
import pickle


path = 'C:/Users/Jimit/Desktop/FE800/Finance/Finance/*.txt' #Enter your path where text files are located
files = glob.glob(path)

df=[]
for name in files:
    try:
        with open(name, encoding="utf8") as f:
            li1=[]
            for line in f:
                li1.append(line)
            df.append(" ".join(li1))
                
    except IOError as exc: #Not sure what error this is
        if exc.errno != errno.EISDIR:
            raise


data = [word_tokenize(d.lower()) for d in df]


cleaned_data = []
for d in data:
    x=DataCleaning(d).remove_non_ascii()
    x=DataCleaning(x).remove_punctuation()
    x=DataCleaning(x).remove_stopwords()
    x=DataCleaning(x).remove_numbers()
    x=DataCleaning(x).remove_less_than_three_letters()
    cleaned_data.append(x)



# Build the bigram and trigram models
bigram = gensim.models.Phrases(cleaned_data, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[cleaned_data], threshold=100)  

# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)


def make_trigrams(data):
    return [trigram_mod[bigram_mod[d]] for d in data]



trigram_data = make_trigrams(cleaned_data)



def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas



lemmatized_data = [lemmatize_verbs(d) for d in trigram_data]



with open("cleaned_lemmatized_data.txt", "wb") as fp:   #Pickling
    pickle.dump(lemmatized_data, fp)



#with open("/data/cleaned_lemmatized_data.txt", "rb") as fp:   # Unpickling
    #ids = pickle.load(fp)

