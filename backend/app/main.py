from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.fifo import fifo_algorithm
from app.lru import lru_algorithm
from app.ai_predictor import MarkovPredictor

app = FastAPI(title="Page Replacement Simulator API")

# ✅ Allow frontend access (CORS setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include algorithm in request model
class SimulationInput(BaseModel):
    reference_string: str
    frames: int
    algorithm: str | None = "fifo"

@app.get("/")
def root():
    return {"message": "Welcome to Page Replacement Simulator"}

from fastapi import Request

@app.post("/simulate")
async def simulate(request: Request):
    body = await request.json()
    print("\n🧾 Incoming JSON from frontend:", body, "\n")  # 👈 debug print
    try:
        reference = [int(x.strip()) for x in body["reference_string"].split(",")]
        frames = int(body["frames"])
        algo = body.get("algorithm", "fifo").lower()
    except Exception as e:
        print("❌ Parsing error:", e)
        return {"error": "Bad request", "detail": str(e)}

    if algo == "fifo":
        return fifo_algorithm(reference, frames)
    elif algo == "lru":
        return lru_algorithm(reference, frames)
    else:
        return {"error": "Invalid algorithm"}


# @app.post("/simulate")
# def simulate(data: SimulationInput):
#     reference = [int(x.strip()) for x in data.reference_string.split(",")]
#     frames = data.frames
#     algo = data.algorithm.lower() if data.algorithm else "fifo"

#     if algo == "fifo":
#         return fifo_algorithm(reference, frames)
#     elif algo == "lru":
#         return lru_algorithm(reference, frames)
#     else:
#         return {"error": "Invalid algorithm selected"}

@app.post("/simulate_all")
def simulate_all(data: SimulationInput):
    reference = [int(x.strip()) for x in data.reference_string.split(",")]
    frames = data.frames

    fifo_result = fifo_algorithm(reference, frames)
    lru_result = lru_algorithm(reference, frames)

    predictor = MarkovPredictor()
    predictor.train(reference)
    predicted_next = predictor.predict_sequence(reference, length=3)

    # ✅ Ensure response structure matches frontend
    return {
        "fifo": fifo_result,
        "lru": lru_result,
        "predicted_next": predicted_next,
        "ai_recommendation": "FIFO" if fifo_result["faults"] < lru_result["faults"] else "LRU",
    }
