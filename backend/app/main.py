from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.fifo import fifo_algorithm
from app.lru import lru_algorithm
from app.ai_predictive import ai_predictive_algorithm
import logging

# ----------------------------
# ✅ Basic setup
# ----------------------------
logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Page Replacement Simulator API")

# ✅ Allow frontend access (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# ✅ Pydantic Model
# ----------------------------
class SimulationInput(BaseModel):
    reference_string: str
    frames: int
    algorithm: str | None = None  # Optional for /simulate_all


# ----------------------------
# ✅ Root Endpoint
# ----------------------------
@app.get("/")
def root():
    return {"message": "Welcome to Page Replacement Simulator"}


# ----------------------------
# ✅ Run single simulation (FIFO/LRU)
# ----------------------------
@app.post("/simulate")
def simulate(data: SimulationInput):
    logging.info(f"🧾 Incoming JSON from frontend: {data.dict()}")
    try:
        reference = [int(x.strip()) for x in data.reference_string.split(",")]
        frames = data.frames
        algorithm = data.algorithm.lower() if data.algorithm else "fifo"

        if algorithm == "fifo":
            result = fifo_algorithm(reference, frames)
        elif algorithm == "lru":
            result = lru_algorithm(reference, frames)
        else:
            return {"error": "Invalid algorithm. Use fifo or lru."}

        return result

    except Exception as e:
        logging.error(f"❌ Parsing error: {e}")
        return {"error": str(e)}


# ----------------------------
# ✅ Compare all (FIFO, LRU, AI Predictive)
# ----------------------------
@app.post("/simulate_all")
def simulate_all(data: SimulationInput):
    try:
        reference = [int(x.strip()) for x in data.reference_string.split(",")]
        frames = data.frames

        # Run all three algorithms
        fifo_result = fifo_algorithm(reference, frames)
        lru_result = lru_algorithm(reference, frames)
        ai_result = ai_predictive_algorithm(reference, frames, lookahead=5)

        # Compare based on page faults
        all_faults = {
            "FIFO": fifo_result.get("faults", fifo_result.get("total_faults", 0)),
            "LRU": lru_result.get("faults", lru_result.get("total_faults", 0)),
            ai_result.get("algorithm", "AI"): ai_result.get("faults", 9999)
        }

        # Best = min page faults
        best_algo = min(all_faults, key=lambda k: all_faults[k])

        return {
            "fifo": fifo_result,
            "lru": lru_result,
            "ai": ai_result,
            "ai_recommendation": best_algo,
            "all_faults": all_faults
        }

    except Exception as e:
        logging.error(f"❌ Error in /simulate_all: {e}")
        return {"error": str(e)}
