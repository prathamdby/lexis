import logging
import pandas as pd
import numpy as np
import time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.config.settings import GOOGLE_SHEET_URL, DATA_REFRESH_INTERVAL

logger = logging.getLogger(__name__)


class NLPProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.all_phrases = []
        self.answer_map = []
        self.stop_words = set(stopwords.words("english"))
        self.process_data()

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [
            word for word in tokens if word.isalnum() and word not in self.stop_words
        ]
        return " ".join(tokens)

    def load_data(self):
        try:
            if not GOOGLE_SHEET_URL:
                logger.warning("Google Sheet ID is not set")
                return []

            data = pd.read_csv(GOOGLE_SHEET_URL)

            if data.shape[1] < 2:
                logger.warning("Invalid data format in the Google Sheet")
                return []

            data = data.dropna(subset=[data.columns[1]])

            sheet_data = data.iloc[:, 0:2].values.tolist()
            logger.info(f"Loaded {len(sheet_data)} records from Google Sheet")
            return sheet_data
        except Exception as e:
            logger.error(f"Error loading data from Google Sheet: {e}")
            return []

    def process_data(self):
        sheet_data = self.load_data()
        self.all_phrases = []
        self.answer_map = []

        for row in sheet_data:
            keywords, answer = row
            for keyword in str(keywords).split(","):
                keyword = keyword.strip()
                preprocessed = self.preprocess_text(keyword)
                self.all_phrases.append(preprocessed)
                self.answer_map.append(answer)

        if self.all_phrases:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.all_phrases)
            logger.info("NLP model updated with new data")
        else:
            self.tfidf_matrix = None
            logger.info("NLP model reset - no data available")

    def find_best_match(self, message_text):
        if not self.all_phrases:
            logger.warning("No data loaded for NLP processing")
            return None, 0

        preprocessed_message = self.preprocess_text(message_text)
        message_vector = self.vectorizer.transform([preprocessed_message])

        similarities = cosine_similarity(message_vector, self.tfidf_matrix)
        best_match_idx = np.argmax(similarities[0])
        similarity_score = similarities[0][best_match_idx]

        if similarity_score > 0.3:
            return self.answer_map[best_match_idx], similarity_score
        return None, 0
