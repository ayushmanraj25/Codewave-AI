# app/ai_predictor.py
from collections import defaultdict, Counter

class MarkovPredictor:
    def __init__(self):
        self.model = defaultdict(Counter)

    def train(self, reference_string):
        for i in range(len(reference_string) - 1):
            curr_page = reference_string[i]
            next_page = reference_string[i + 1]
            self.model[curr_page][next_page] += 1

    def predict_next(self, current_page):
        if current_page not in self.model:
            return None
        return self.model[current_page].most_common(1)[0][0]

    def predict_sequence(self, sequence, length=3):
        if not sequence:
            return []
        predictions = []
        current = sequence[-1]
        for _ in range(length):
            next_page = self.predict_next(current)
            if not next_page:
                break
            predictions.append(next_page)
            current = next_page
        return predictions
