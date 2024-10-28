import os
import json
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import bigrams
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
    try:
        response = requests.get(f'{API_URL}/dreams/{dream_id}', headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        print(f"An error occurred: {err}")
        return None
    return response.json()

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    text = text.lower()
    words = word_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words and word.isalpha()]
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    bi_grams_list = list(bigrams(lemmatized_words))
    bi_grams = [' '.join(bi_gram) for bi_gram in bi_grams_list]

    return lemmatized_words + bi_grams

def identify_common_themes(words):
    theme_keywords = {
        'flying': 'freedom or escape',
        'falling': 'loss of control',
        'chased': 'avoidance',
        'water': 'emotion and subconscious',
        'death': 'end of something',
        'lost': 'searching for direction',
        'found': 'discovery or solution'
    }
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
    if not themes:
        return "No significant themes identified."
    report_lines = []
    for theme, details in themes.items():
        line = f"The theme '{theme}' related to '{details['meaning']}' was found {details['count']} times."
        report_lines.append(line)
    return "\n".join(report_lines)

def analyze_dream(dream_id):
    dream_data = fetch_dream_data(dream_id)
    if dream_data is None:
        return "Failed to fetch dream data."
    dream_text = dream_data['content']
    processed_words = preprocess_text(dream_text)
    themes = identify_common_themes(processed_words)
    report = generate_report(themes)

    return report

if __name__ == "__main__":
    dream_id = "example_dream_id"
    analysis_report = analyze_dream(dream_id)
    print(analysis_report)