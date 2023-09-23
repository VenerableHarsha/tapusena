import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Your existing Python code to compute the cosine similarity goes here

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filtered-data', methods=['POST'])
def filtered_data():
    if request.method == 'POST':
        # Check if the request has form data named 'experience'
        user_experience = request.form.get('experience')

        if user_experience:
            # Read the CSV file
            dhelp = pd.read_csv("tapusena\\harsha page\\help.csv")

            # Compute the cosine similarity based on user input
            df = pd.read_csv("tapusena\\harsha page\\cyberbullying_tweets.csv")
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

            # Filter rows based on the "target" condition
            filtered_rows = dhelp[dhelp["target"] == target_condition]

            # Convert the filtered DataFrame to a list of dictionaries
            rows_to_display = filtered_rows.to_dict(orient='records')

            return jsonify(rows_to_display)

    # Default response (predefined data)
    rows_to_display = [
        # Data for the first row
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
        # Data for the second row
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

if __name__ == '__main__':
    app.run()
