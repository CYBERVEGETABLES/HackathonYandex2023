from json import load
from typing import Callable

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

import skills


class Recognizer:
    def __init__(
        self, file_name: str
    ) -> None:
        with open(file_name, 'r', encoding='utf-8') as file:
            self.data_learn = load(file)

        self.vectorizer = CountVectorizer()
        self.vectors = self.vectorizer.fit_transform(list(self.data_learn.keys()))

        self.clf = LogisticRegression()
        self.clf.fit(self.vectors, list(self.data_learn.values()))

    def get_answer(self, source: str) -> str | tuple[str, Callable] | None:
        text_vector = self.vectorizer.transform([source]).toarray()[0]
        answer: str = self.clf.predict([text_vector])[0]

        func_name = answer.split()[0]
        func = getattr(skills, func_name)
        if func:
            answer = answer.replace(func_name, '').lstrip()
            return answer, func
        else:
            return answer


recognizer = Recognizer('data_set.json')
