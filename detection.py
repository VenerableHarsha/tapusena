import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# data = pd.read_csv('login page 2/helpers/help.csv')

@app.route('/blah.html')
def index():
    return render_template("/blah.html")

@app.route('/filtered-data', methods=['POST'])
def filtered_data():
    if request.method == 'POST':
        
        user_experience = request.form.get('experience')

        if user_experience:
            # Read the CSV file
            dhelp = pd.read_csv("tapusena\\helpers\\help.csv")

            
            df = pd.read_csv("tapusena\\helpers\\cyberbullying_tweets.csv")
            x = df["tweet_text"]

            y_words = user_experience.split()

            vectorizer = TfidfVectorizer(lowercase=False, use_idf=True, max_features=2500)

            vectTrain = vectorizer.fit_transform(x)
            vectTest = vectorizer.transform([' '.join(y_words)])  # Join the words back into a string before transforming
            result = cosine_similarity(vectTrain, vectTest)

            top_indices = np.argsort(result[:, 0])[-5:][::-1]
            top_tweets = df.loc[top_indices, "cyberbullying_type"]

            reference_dict = {'gender':1,
            'ethnicity':2,
            'other_cyberbullying':3,
            'age':4,
            'religion':5,
            'not_cyberbullying': 6}
            result = {}
            res = []

            for i in top_tweets:
                res.append(i)

            for i in top_tweets:
                result[i] = res.count(i)
            result = sorted(result)
            target_condition = result[:1][0]

            
            filtered_rows = dhelp[dhelp["target"] == target_condition]

           
            rows_to_display = filtered_rows.to_dict(orient='records')

            return jsonify(rows_to_display)

    
    rows_to_display = [
        
        {
            "Psychologist Type": "Health Psychologist",
            "Name": "David Williams",
            "Age": 31,
            "Gender": "Male",
            "Ethnicity": "American",
            "Religion": "Christian",
            "NGO": "Mind-Body Connection",
            "Hobbies": "Mindfulness and meditation, holistic health, wellness programs",
            "target": "age"
        },
        
        {
            "Psychologist Type": "Forensic Psychologist",
            "Name": "Aditya Verma",
            "Age": 45,
            "Gender": "Male",
            "Ethnicity": "Indian",
            "Religion": "Hindu",
            "NGO": "Justice Seekers Foundation",
            "Hobbies": "Criminal profiling, forensic assessments, solving complex cases",
            "target": "age"
        }
    ]

    return jsonify(rows_to_display)

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
    pos_tag_word = pos_tags
    pos_map = {
        'N': 'n',  # Noun
        'V': 'v',  # Verb
        'R': 'r',  # Adverb
        'J': 'a'   # Adjective
    }
    pos = pos_map.get(pos_tag_word, 'n')
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
    return words
    # return [lemmatize_word(word) for word in words]

df = pd.read_csv("/Users/krishhashia/PycharmProjects/css_mysite/harras.csv")
loglikelihood = df.set_index('text')['loglikelihood'].to_dict()

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('/homepage.html')

@app.route('/index.html', methods=['GET'])
def predict():
    tweet = "i was beaten up badly and tortured a lot"
    result = npredict(loglikelihood,-2.122046523535116,tweet)
    return render_template('/index.html', prediction_result=result)

@app.route('/contact.html')
def contact():
    return render_template('/contact.html')

@app.route('/aboutus.html')
def about():
    return render_template('/aboutus.html')

def npredict(loglikelihood,logprior,tweet="i was beaten up"):
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
    app.run(debug=True)
