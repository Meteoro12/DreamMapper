import os
import json
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

API_KEY = os.getenv('DREAM_ANALYSIS_API_KEY')
API_URL = os.getenv('DREAM_ANALYSIS_API_URL')

if not API_KEY or not API_URL:
    raise ValueError("API_KEY and API_URL must be set in your environment.")

def fetch_dream_data(dream_id):
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(f'{API_URL}/dreams/{dream_id}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    words = word_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words]
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    return lemmatized_words

def identify_common_themes(words):
    theme_keywords = {'flying': 'freedom or escape', 'falling': 'loss of control', 'chased': 'avoidance'}
    themes_identified = {}

    for word in words:
        for theme, meaning in theme_keywords.items():
            if theme in word:
                if theme in themes_identified:
                    themes_identified[theme]['count'] += 1
                else:
                    themes_identified[theme] = {'meaning': meaning, 'count': 1}

    return themes_identified

def generate_report(themes):
    report_lines = []
    for theme, details in themes.items():
        line = f"The theme '{theme}' related to '{details['meaning']}' was found {details['count']} times."
        report_lines.append(line)
    return "\n".join(report_lines)

def analyze_dream(dream_id):
    dream_data = fetch_dream_data(dream_id)
    dream_text = dream_data['content']
    processed_words = preprocess_text(dream_text)
    themes = identify_common_themes(processed_words)
    report = generate_report(themes)

    return report

if __name__ == "__main__":
    dream_id = "example_dream_id"
    analysis_report = analyze_dream(dream_id)
    print(analysis_report)