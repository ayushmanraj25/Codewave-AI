def lru_algorithm(reference_string, frames):
    pages = []
    page_faults = 0
    page_hits = 0
    steps = []

    for page in reference_string:
        fault = False

        if page in pages:
            # ✅ Page hit — move it to most recently used position
            pages.remove(page)
            pages.append(page)
            page_hits += 1
        else:
            # ✅ Page fault
            fault = True
            page_faults += 1
            if len(pages) < frames:
                pages.append(page)
            else:
                # ✅ Remove least recently used (first in list)
                pages.pop(0)
                pages.append(page)

        steps.append({
            "page": page,
            "frames": pages.copy(),
            "fault": fault
        })

    fault_rate = page_faults / len(reference_string)

    return {
        "algorithm": "LRU",
        "faults": page_faults,
        "hits": page_hits,
        "fault_rate": fault_rate,
        "steps": steps
    }
