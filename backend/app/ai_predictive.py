# backend/app/ai_predictive.py
from typing import List, Dict, Any
from app.ai_predictor import MarkovPredictor

def ai_predictive_algorithm(reference: List[int], frames: int, lookahead: int = 5) -> Dict[str, Any]:
    """
    Predictive page replacement using a Markov model:
    - Train predictor on the given reference sequence (simple approach).
    - For each page fault, if frames full, use predictor to predict the next `lookahead` pages
      from the current (last seen) page and evict the page whose predicted next occurrence
      is farthest in the predicted list (or not present at all).
    """
    predictor = MarkovPredictor()
    # Train on the whole reference to make model knowledge of transitions
    predictor.train(reference)

    pages: List[int] = []
    faults = 0
    hits = 0
    steps: List[Dict[str, Any]] = []

    # We'll maintain "last_seen" as previous page in stream (for prediction seed)
    last_seen = None

    for i, page in enumerate(reference):
        fault = False

        if page in pages:
            hits += 1
            # move page to MRU (optional to keep stable behavior)
            pages.remove(page)
            pages.append(page)
        else:
            fault = True
            faults += 1
            if len(pages) < frames:
                pages.append(page)
            else:
                # Look-ahead prediction from last_seen (or current page if last_seen None)
                seed = last_seen if last_seen is not None else page
                predicted = predictor.predict_sequence(seed, length=lookahead)

                # For each candidate page in frames, find index of first occurrence in predicted
                # If not found, treat index as large (prefer to evict pages not predicted soon)
                def predicted_index(candidate):
                    try:
                        return predicted.index(candidate)
                    except ValueError:
                        return 10**6  # not predicted in lookahead -> high score (evict this)

                # Choose victim with maximum predicted_index (farthest or never predicted)
                victim = max(pages, key=predicted_index)
                # Replace victim
                idx = pages.index(victim)
                pages[idx] = page

        # update last_seen
        last_seen = page

        steps.append({
            "page": page,
            "frames": pages.copy(),
            "fault": fault
        })

    fault_rate = faults / len(reference) if reference else 0.0

    return {
        "algorithm": "AI-Predictive-Markov",
        "faults": faults,
        "hits": hits,
        "fault_rate": fault_rate,
        "steps": steps
    }
