def fifo_algorithm(reference, frames):
    pages = []
    faults = 0
    steps = []

    for page in reference:
        fault = False
        if page not in pages:
            fault = True
            faults += 1
            if len(pages) < frames:
                pages.append(page)
            else:
                pages.pop(0)
                pages.append(page)
        steps.append({"page": page, "frames": pages.copy(), "fault": fault})

    total_hits = len(reference) - faults
    fault_rate = faults / len(reference)

    return {
        "faults": faults,
        "hits": total_hits,
        "fault_rate": fault_rate,
        "steps": steps
    }
