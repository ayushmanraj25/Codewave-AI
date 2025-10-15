import axios from "axios";

// ✅ Connect frontend to backend
const api = axios.create({
  baseURL: "http://127.0.0.1:8000", // backend FastAPI URL
});

export default api;

// ▶️ Run one algorithm (FIFO / LRU)
export const simulate = async (referenceString, frames, algorithm) => {
  // referenceString might be an array from frontend input — convert to comma string
  const refString = Array.isArray(referenceString)
    ? referenceString.join(",")
    : referenceString;

  const response = await api.post("/simulate", {
    reference_string: refString, // ✅ backend expects this key
    frames: parseInt(frames),    // ✅ backend expects this key
    algorithm: algorithm,        // ✅ include algorithm
  });

  return response.data;
};

// 🤖 Compare all (AI-based prediction)
export const simulateAll = async (referenceString, frames) => {
  const refString = Array.isArray(referenceString)
    ? referenceString.join(",")
    : referenceString;

  const response = await api.post("/simulate_all", {
    reference_string: refString,
    frames: parseInt(frames),
  });

  return response.data;
};
