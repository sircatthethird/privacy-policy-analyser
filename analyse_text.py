from flask import Blueprint, render_template
import os
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# Define the analyse_text blueprint
analyse_text = Blueprint('analyse_text', __name__)

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('wordnet')

# Define categories and corresponding phrases
categories = {
    "Contact information": ["email address", "IP address", "telephone number", "address"],
    "Cookies": ["cookies", "cookie policy"],
    "Demographic information": ["nationality", "age", "gender"],
    "Financial information": ["payment", "credit card", "bank account"],
    "Health information": ["health", "medical"],
    "Preferences": ["preferences", "interests"],
    "Purchasing information": ["purchase history", "transactions"],
    "Social security number & government ID": ["social security number", "government ID"],
    "Your activity on this site": ["activity", "interactions", "usage"],
    "Your location": ["location", "geographical"]
}

# Function to get synonyms for a word using WordNet
def get_synonyms(word):
    synonyms = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# Function to check if a word or its synonyms exist in the text
def check_phrases(text, phrases):
    words = word_tokenize(text)
    for word in words:
        if word.lower() in phrases:
            return True
        for synonym in get_synonyms(word.lower()):
            if synonym in phrases:
                return True
    return False

# Function to categorize the text
def categorize_text(text):
    results = {}
    for category, phrases in categories.items():
        results[category] = "Yes" if check_phrases(text, phrases) else "No"
    return results

# Function to color code the output
def color_code_output(text):
    if text == "Yes":
        return "Yes"  
    elif text == "No":
        return "No"  
    else:
        return text


# Function to extract JSON data from the newest JSON file in the folder (including subdirectories)
def extract_json_from_folder(folder_path):
    newest_json_file = None
    newest_creation_time = 0

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                json_file_path = os.path.join(root, file)
                creation_time = os.path.getctime(json_file_path)
                if creation_time > newest_creation_time:
                    newest_creation_time = creation_time
                    newest_json_file = json_file_path

    if newest_json_file:
        with open(newest_json_file, 'r') as f:
            json_data = json.load(f)
        return json_data
    else:
        print("No JSON file found in the output directory and its subdirectories.")
        return None

# Define a route to perform text analysis
@analyse_text.route('/analyse', methods=['GET'])
def analyse():
    # Define the path to the folder containing JSON files
    folder_path = 'policies'

    # Extract JSON data from the folder
    extracted_json = extract_json_from_folder(folder_path)

    if extracted_json:
        # Assuming your JSON data is stored in a dictionary under the key "text"
        text = extracted_json["text"]

        # Categorize the text
        results = categorize_text(text)

        # Prepare results with color coding
        colored_results = {}
        for category, presence in results.items():
            colored_results[category] = color_code_output(presence)

        # Render a template to display the results
        return render_template('results.html', results=colored_results)
    else:
        return "No JSON file found in the output directory."

