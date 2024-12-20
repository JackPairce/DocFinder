from nltk.tokenize import word_tokenize  # type: ignore
from nltk.corpus import stopwords  # type: ignore
from typing import List


def tokenize_text(text: str, language: str) -> List[str]:
    stop_words = set(stopwords.words(language))  # type: ignore
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]
    return words
