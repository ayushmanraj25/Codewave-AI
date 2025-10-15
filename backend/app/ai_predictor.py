# backend/app/ai_predictor.py
from collections import defaultdict, Counter
import random

class MarkovPredictor:
    def __init__(self):
        # model[curr_page] -> Counter(next_page -> count)
        self.model = defaultdict(Counter)

    def train(self, sequence):
        """Train from a list of pages (ints)."""
        for i in range(len(sequence) - 1):
            curr = sequence[i]
            nxt = sequence[i + 1]
            self.model[curr][nxt] += 1

    def predict_next(self, current_page):
        """Return most likely next page after current_page or None."""
        if current_page not in self.model or not self.model[current_page]:
            return None
        return self.model[current_page].most_common(1)[0][0]

    def predict_probabilities(self, current_page):
        """Return dict of next_page -> probability (normalized)."""
        if current_page not in self.model or not self.model[current_page]:
            return {}
        cnt = self.model[current_page]
        total = sum(cnt.values())
        return {p: c / total for p, c in cnt.items()}

    def predict_sequence(self, current_page, length=5):
        """Return predicted sequence of length `length` starting from current_page."""
        if current_page is None:
            return []
        seq = []
        cur = current_page
        for _ in range(length):
            nxt = self.predict_next(cur)
            if nxt is None:
                break
            seq.append(nxt)
            cur = nxt
        return seq
