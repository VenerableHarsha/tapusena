import pandas as pd
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
import string
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from flask import Flask, render_template, request
nltk.download('stopwords')
l = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def lemmatize_word(word):
    tokens = word_tokenize(word)
    tokens = [word for word in tokens if word.lower() not in stop_words]
    pos_tags = pos_tag(tokens)
    pos_tag_word = pos_tags[0][1]
    pos_map = {
        'N': 'n',  # Noun
        'V': 'v',  # Verb
        'R': 'r',  # Adverb
        'J': 'a'   # Adjective
    }
    pos = pos_map.get(pos_tag_word[0], 'n')
    lemma = l.lemmatize(word, pos=pos)
    return lemma

def remove_punctuation(line):
    translator = str.maketrans('', '', string.punctuation)
    cleaned_line = line.translate(translator)
    return cleaned_line

def process_text(text):
    text = str(text)
    text = text.lower()
    text = remove_punctuation(text)
    words = text.split()
    return [lemmatize_word(word) for word in words]

df = pd.read_csv("C:\\Users\\harsh\\OneDrive\\Documents\\tp1\\tapusena\\cyberbullying\\harras.csv")
loglikelihood = df.set_index('text')['loglikelihood'].to_dict()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', prediction_result='')

@app.route('/predict', methods=['POST'])
def predict():
    tweet = request.form['tweet']
    result = npredict(loglikelihood,-2.122046523535116,tweet)
    return render_template('index.html', prediction_result=result)

def npredict(loglikelihood,logprior,tweet="niggers are cotton pickers"):
    word_l = process_text(tweet)
    p = logprior
    for word in word_l:
        if word in loglikelihood:
            p += loglikelihood[word]

    m = (p / len(tweet)) + 0.71  
    if m>0:
        n=1
    else:
        n=0
    return (m,n)

if __name__ == '__main__':
    app.run()
