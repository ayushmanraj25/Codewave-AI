import { useState } from "react";
import { simulate, simulateAll } from "./api/apiClient"; // ✅ import both helpers

function App() {
  const [input, setInput] = useState("1,2,3,2,4,1,2,5,2,3");
  const [frames, setFrames] = useState(3);
  const [algorithm, setAlgorithm] = useState("fifo");
  const [result, setResult] = useState(null);
  const [aiResult, setAiResult] = useState(null);

  // 🚀 Run single algorithm (FIFO / LRU)
  const runSimulation = async () => {
    try {
      const referenceString = input; // ✅ send string as backend expects
      const res = await simulate(referenceString, frames, algorithm);
      setResult(res);
      setAiResult(null); // clear AI results
    } catch (err) {
      console.error("Simulation error:", err);
      alert("⚠️ Backend not reachable. Make sure it's running on port 8000.");
    }
  };

  // 🤖 Run AI comparison (FIFO + LRU + AI Predictor)
  const handleCompareAll = async () => {
    try {
      const data = await simulateAll(input, frames);
      setAiResult(data);
      setResult(null);
    } catch (error) {
      console.error("AI Compare error:", error);
      alert("⚠️ Backend not reachable. Make sure it's running on port 8000.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-gray-100 flex flex-col">
      {/* 🌈 Navbar */}
      <nav className="w-full bg-gray-800/40 backdrop-blur-md border-b border-gray-700 px-8 py-4 flex justify-between items-center shadow-md">
        <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-400 to-purple-400 text-transparent bg-clip-text">
          🧠 Page Replacement Simulator
        </h1>
        <a
          href="https://github.com/ayushmanraj25"
          target="_blank"
          rel="noreferrer"
          className="bg-gradient-to-r from-pink-500 to-purple-500 text-white px-4 py-2 rounded-lg font-medium hover:scale-105 transition-all shadow-lg"
        >
          GitHub ↗
        </a>
      </nav>

      {/* 🌸 Main */}
      <main className="flex-grow flex items-center justify-center p-6">
        <div className="bg-gray-800/60 backdrop-blur-lg shadow-2xl rounded-2xl p-8 w-full max-w-2xl border border-gray-700 hover:shadow-pink-400/10 transition-all duration-300">
          <h2 className="text-3xl font-semibold text-pink-400 mb-6 text-center">
            ⚙️ Simulation Setup
          </h2>

          {/* Input Section */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Reference String (comma separated)
              </label>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="w-full rounded-lg bg-gray-700 border border-gray-600 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
              />
            </div>

            <div className="flex gap-3">
              <div className="flex-1">
                <label className="text-sm text-gray-300 mb-1 block">
                  Number of Frames
                </label>
                <input
                  type="number"
                  value={frames}
                  onChange={(e) => setFrames(parseInt(e.target.value))}
                  className="w-full rounded-lg bg-gray-700 border border-gray-600 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
                />
              </div>

              <div className="flex-1">
                <label className="text-sm text-gray-300 mb-1 block">
                  Algorithm
                </label>
                <select
                  value={algorithm}
                  onChange={(e) => setAlgorithm(e.target.value)}
                  className="w-full rounded-lg bg-gray-700 border border-gray-600 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-pink-500"
                >
                  <option value="fifo">FIFO (First In First Out)</option>
                  <option value="lru">LRU (Least Recently Used)</option>
                </select>
              </div>
            </div>
          </div>

          {/* 🧠 Buttons */}
          <div className="flex justify-center gap-4 mt-6">
            <button
              onClick={runSimulation}
              className="bg-gradient-to-r from-pink-500 to-purple-500 hover:from-pink-600 hover:to-purple-600 transition-all text-white py-2 px-6 rounded-xl font-semibold shadow-lg hover:shadow-pink-400/40 transform hover:scale-105"
            >
              🚀 Run Simulation
            </button>

            <button
              onClick={handleCompareAll}
              className="bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 transition-all text-white py-2 px-6 rounded-xl font-semibold shadow-lg hover:shadow-cyan-400/40 transform hover:scale-105"
            >
              🤖 Compare All (AI)
            </button>
          </div>

          {/* 📊 Normal Results */}
          {result && (
            <div className="mt-10">
              <h2 className="text-2xl font-semibold mb-4 text-center text-purple-400">
                📊 Simulation Results
              </h2>
              <div className="bg-gray-700/50 p-4 rounded-xl border border-gray-600 mb-4 space-y-2 shadow-inner">
                <p>
                  <span className="font-medium text-pink-400">
                    Total Faults:
                  </span>{" "}
                  {result.faults ?? result.total_faults}
                </p>
                <p>
                  <span className="font-medium text-pink-400">Total Hits:</span>{" "}
                  {result.hits ?? result.total_hits}
                </p>
                <p>
                  <span className="font-medium text-pink-400">Fault Rate:</span>{" "}
                  {(
                    (result.fault_rate ??
                      result.faults / (result.faults + result.hits)) * 100
                  ).toFixed(2)}
                  %
                </p>
              </div>

              <h3 className="text-lg font-semibold mb-2 text-gray-200 flex items-center gap-2">
                🔁 Step-by-Step Execution
              </h3>
              <div className="bg-gray-700/40 p-4 rounded-lg border border-gray-600 max-h-64 overflow-y-auto scrollbar-thin scrollbar-thumb-pink-500/40 scrollbar-track-gray-700/40">
                <ul className="space-y-2 text-sm">
                  {result.steps.map((s, i) => (
                    <li
                      key={i}
                      className={`flex justify-between items-center p-2 rounded-lg ${
                        s.fault
                          ? "bg-red-500/10 border border-red-400/40 text-red-400"
                          : "bg-green-500/10 border border-green-400/40 text-green-400"
                      }`}
                    >
                      <span>
                        <b>Page:</b> {s.page}
                      </span>
                      <span className="text-gray-300">
                        <b>Frames:</b> [{s.frames.join(", ")}]
                      </span>
                      {s.fault && <span>❌</span>}
                      {!s.fault && <span>✅</span>}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* 🧠 AI Comparison Results */}
          {aiResult && (
            <div className="mt-10">
              <h2 className="text-2xl font-semibold mb-4 text-center text-cyan-400">
                🤖 AI Comparison Results
              </h2>

              <div className="bg-gray-700/50 p-4 rounded-xl border border-gray-600 mb-4 space-y-2 shadow-inner">
                <p>
                  <span className="font-medium text-pink-400">
                    FIFO Faults:
                  </span>{" "}
                  {aiResult.fifo.faults}
                </p>
                <p>
                  <span className="font-medium text-pink-400">LRU Faults:</span>{" "}
                  {aiResult.lru.faults}
                </p>
                <p>
                  <span className="font-medium text-cyan-400">
                    AI Predictive Faults:
                  </span>{" "}
                  {aiResult.ai?.faults}
                </p>
                <p className="text-xl font-semibold text-center mt-4">
                  🧠 Best Algorithm (AI Recommendation):{" "}
                  <span className="text-green-400">
                    {aiResult.ai_recommendation}
                  </span>
                </p>
              </div>

              <div className="bg-gray-800/60 p-4 rounded-lg border border-gray-600 mt-4">
                <h3 className="text-lg font-semibold text-cyan-400 mb-2">
                  📊 Fault Comparison
                </h3>
                <pre className="text-gray-300 text-sm">
                  {JSON.stringify(aiResult.all_faults, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* 🌙 Footer */}
      <footer className="bg-gray-900/60 text-gray-400 text-center py-4 text-sm border-t border-gray-700">
        Made with ❤️ by <span className="text-pink-400">Aayu & Ayushman</span>
      </footer>
    </div>
  );
}

export default App;
