import { useState } from "react";

function App() {

  const [loading, setLoading] = useState(false);
  const [fileName, setFileName] = useState("");
  const [progress, setProgress] = useState(0);
  const [selectedFile, setSelectedFile] = useState(null);

  const [result, setResult] = useState({
  score: "0%",
  risk: "WAITING",
  text: "Upload media to begin analysis."
});

  const resetResult = (risk = "WAITING", text = "Upload media to begin analysis.") => {
    setResult({
      score: "0%",
      risk,
      text
    });
  };

  const analyzeMedia = async () => {
  if (!selectedFile) {
    alert("Please upload a file");
    return;
  }

  // Reset before each analysis
  resetResult("ANALYZING", "Scanning media for synthetic voice artifacts...");
  setProgress(0);
  setLoading(true);
  setProgress(10);

  const progressTimer = setInterval(() => {
    setProgress((current) => Math.min(current + 10, 90));
  }, 250);

  try {
    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await fetch("http://127.0.0.1:8000/analyze/audio", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Backend analysis request failed.");
    }

    const data = await response.json();
    setProgress(100);
    setResult({
      score: data.score || "0%",
      risk: data.risk || "ERROR",
      text: data.text || "No analysis details returned."
    });
  } catch (error) {
    console.error(error);
    setResult({
      score: "0%",
      risk: "ERROR",
      text: "Backend connection failed."
    });
  } finally {
    clearInterval(progressTimer);
    setLoading(false);
  }
};

  return (
    <div
      style={{
        minHeight: "100vh",
        margin: 0,
        padding: "40px 16px",
        background:
          "radial-gradient(circle at top, #1f2937 0, #020617 45%, #000 100%)",
        color: "#e5e7eb",
        fontFamily:
          "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "960px",
          display: "grid",
          gridTemplateColumns: "minmax(0, 1.3fr) minmax(0, 1fr)",
          gap: "32px",
        }}
      >

        {/* LEFT SIDE */}
        <div>

          <div style={{ marginBottom: "24px" }}>

            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "4px 10px",
                borderRadius: "999px",
                backgroundColor: "rgba(37, 99, 235, 0.18)",
                border: "1px solid rgba(148, 163, 184, 0.4)",
                fontSize: "12px",
                textTransform: "uppercase",
                letterSpacing: "0.12em",
                color: "#bfdbfe",
              }}
            >
              <span>🛡️</span>
              <span>Real-Time Deepfake Defense</span>
            </div>

            <h1
              style={{
                marginTop: "16px",
                marginBottom: "12px",
                fontSize: "36px",
                lineHeight: 1.1,
                color: "#f9fafb",
              }}
            >
              DeepShield <span style={{ color: "#60a5fa" }}>AI</span>
            </h1>

            <p
              style={{
                maxWidth: "32rem",
                fontSize: "15px",
                lineHeight: 1.6,
                color: "#9ca3af",
              }}
            >
              Upload voice calls, statements, or media clips and let DeepShield
              AI scan for hidden synthetic-voice artifacts before you trust or
              share them.
            </p>

          </div>

          {/* Upload Card */}
          <div
            style={{
              background:
                "linear-gradient(to bottom right, rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.7))",
              borderRadius: "16px",
              padding: "20px",
              border: "1px solid rgba(148, 163, 184, 0.35)",
              boxShadow: "0 18px 45px rgba(15, 23, 42, 0.9)",
            }}
          >

            <p
              style={{
                fontSize: "13px",
                textTransform: "uppercase",
                letterSpacing: "0.14em",
                color: "#9ca3af",
                marginBottom: "8px",
              }}
            >
              Step 1 · Upload media
            </p>

            <label
              style={{
                display: "block",
                borderRadius: "14px",
                border: "1px dashed rgba(148, 163, 184, 0.6)",
                backgroundColor: "rgba(15, 23, 42, 0.7)",
                padding: "18px",
                textAlign: "center",
                cursor: "pointer",
              }}
            >

              
              <input
  type="file"
  accept="audio/*,video/*"
  style={{ display: "none" }}
  onChange={(e) => {

  const file = e.target.files[0];

  if (!file) return;

  setSelectedFile(file);

  setFileName(file.name);

  resetResult("READY", "Ready to analyze.");
  setProgress(0);

  // IMPORTANT
  e.target.value = "";
}}
/>

              <p
                style={{
                  fontSize: "14px",
                  color: "#e5e7eb",
                  marginBottom: 4
                }}
              >
                Drop a file here, or{" "}
                <span
                  style={{
                    color: "#60a5fa",
                    fontWeight: 600
                  }}
                >
                  browse from device
                </span>
              </p>

              <p
                style={{
                  fontSize: "12px",
                  color: "#9ca3af"
                }}
              >
                Supported: audio/video up to 60 seconds
                {fileName && (
  <p
    style={{
      marginTop: "10px",
      color: "#60a5fa",
      fontSize: "12px"
    }}
  >
    Uploaded: {fileName}
  </p>
)}
              </p>

            </label>

            <button
              onClick={analyzeMedia}
              disabled={loading}
              style={{
                marginTop: "16px",
                width: "100%",
                padding: "12px 20px",
                fontSize: "15px",
                fontWeight: 600,
                background:
                  "linear-gradient(to right, #2563eb, #4f46e5, #1d4ed8)",
                color: "white",
                border: "none",
                borderRadius: "999px",
                cursor: loading ? "not-allowed" : "pointer",
                opacity: loading ? 0.8 : 1,
                boxShadow: "0 12px 30px rgba(37, 99, 235, 0.55)",
              }}
            >
              {loading ? "Scanning Media..." : "Analyze Media"}
              {loading && (
  <div
    style={{
      marginTop: "16px",
    }}
  >

    <p
      style={{
        fontSize: "12px",
        color: "#9ca3af",
        marginBottom: "6px"
      }}
    >
      AI scanning in progress... {progress}%
    </p>

    <div
      style={{
        width: "100%",
        height: "8px",
        backgroundColor: "#020617",
        borderRadius: "999px",
        overflow: "hidden"
      }}
    >
      <div
        style={{
          width: `${progress}%`,
          height: "100%",
          background:
  result.risk === "HIGH"
    ? "linear-gradient(to right, #f97316, #ef4444)"
    : result.risk === "MEDIUM"
    ? "linear-gradient(to right, #eab308, #f97316)"
    : "linear-gradient(to right, #22c55e, #16a34a)",
            
          transition: "width 0.2s ease"
        }}
      />
    </div>

  </div>
)}
            </button>

            <p
              style={{
                marginTop: "10px",
                fontSize: "11px",
                color: "#6b7280",
              }}
            >
              We never store your uploads. All analysis happens in a secure
              sandbox in real time.
            </p>

          </div>

        </div>

        {/* RIGHT SIDE */}
        <div
          style={{
            background:
              "linear-gradient(to bottom right, rgba(15, 23, 42, 0.95), rgba(24, 35, 55, 0.95))",
            borderRadius: "18px",
            padding: "20px",
            border: "1px solid rgba(148, 163, 184, 0.4)",
            boxShadow: "0 18px 45px rgba(15, 23, 42, 1)",
          }}
        >

          <h2
            style={{
              fontSize: "16px",
              marginBottom: "12px",
            }}
          >
            Analysis Result
          </h2>

          <div
            style={{
              display: "inline-flex",
              padding: "4px 10px",
              borderRadius: "999px",
              backgroundColor:
                result.risk === "HIGH"
                  ? "rgba(220,38,38,0.15)"
                  : result.risk === "MEDIUM"
                  ? "rgba(234,179,8,0.15)"
                  : result.risk === "LOW"
                  ? "rgba(34,197,94,0.15)"
                  : result.risk === "ERROR"
                  ? "rgba(239,68,68,0.15)"
                  : "rgba(96,165,250,0.15)",
              marginBottom: "10px",
            }}
          >
            {["HIGH", "MEDIUM", "LOW", "ERROR"].includes(result.risk)
              ? `${result.risk} RISK`
              : result.risk}
          </div>

          <div style={{ marginBottom: "12px" }}>

            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                marginBottom: "4px",
              }}
            >
              <span>Authenticity Score</span>

              <span
                style={{
                  color:
  result.risk === "HIGH"
    ? "#f87171"
    : result.risk === "MEDIUM"
    ? "#facc15"
    : result.risk === "LOW"
    ? "#4ade80"
    : result.risk === "ERROR"
    ? "#f87171"
    : "#60a5fa",
                  fontWeight: 600
                }}
              >
                {result.score}
              </span>
            </div>

            <div
              style={{
                height: "8px",
                borderRadius: "999px",
                backgroundColor: "#020617",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: result.score,
                  height: "100%",
                  borderRadius: "999px",
                  background:
  result.risk === "HIGH"
    ? "linear-gradient(to right, #f97316, #ef4444)"
    : result.risk === "MEDIUM"
    ? "linear-gradient(to right, #facc15, #eab308)"
    : result.risk === "LOW"
    ? "linear-gradient(to right, #4ade80, #16a34a)"
    : result.risk === "ERROR"
    ? "linear-gradient(to right, #f97316, #ef4444)"
    : "linear-gradient(to right, #60a5fa, #2563eb)",
    boxShadow:
  result.risk === "HIGH"
    ? "0 0 18px rgba(239,68,68,0.5)"
    : result.risk === "MEDIUM"
    ? "0 0 18px rgba(250,204,21,0.5)"
    : result.risk === "LOW"
    ? "0 0 18px rgba(74,222,128,0.5)"
    : result.risk === "ERROR"
    ? "0 0 18px rgba(239,68,68,0.5)"
    : "0 0 18px rgba(96,165,250,0.45)",
                }}
              />
            </div>

          </div>

          <p
            style={{
              fontSize: "13px",
              color: "#d1d5db",
              lineHeight: 1.6
            }}
          >
            {result.text}
          </p>

        </div>

      </div>
    </div>
  );
}

export default App;
