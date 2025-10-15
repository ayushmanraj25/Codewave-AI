import axios from "axios";

// ✅ Connect frontend to backend
const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // backend FastAPI URL
});

export default api;

// ▶ Run one algorithm (FIFO/LRU)
export const simulate = async (referenceString, frames, algorithm) => {
  const response = await api.post("/simulate", {
    reference_string: referenceString,
    frames: parseInt(frames),
    algorithm,
  });
  return response.data;
};

// 🤖 Compare all (AI-based prediction)
export const simulateAll = async (referenceString, frames) => {
  const response = await api.post("/simulate_all", {
    reference_string: referenceString,
    frames: parseInt(frames),
  });
  return response.data;
};
