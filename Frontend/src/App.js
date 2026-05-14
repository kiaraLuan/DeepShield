import { useState } from "react";

function App() {

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState({
    score: "28%",
    risk: "HIGH",
    text: "Detected strong signs of vocoder artifacts and spectral anomalies commonly left by neural TTS systems."
  });

  const analyzeMedia = () => {

    setLoading(true);

    setTimeout(() => {

      const fakeResults = [
        {
          score: "28%",
          risk: "HIGH",
          text: "Detected strong signs of vocoder artifacts and spectral anomalies commonly left by neural TTS systems."
        },
        {
          score: "44%",
          risk: "MEDIUM",
          text: "Suspicious modulation and inconsistent phoneme energy patterns detected."
        },
        {
          score: "91%",
          risk: "LOW",
          text: "Media appears authentic with natural environmental noise patterns."
        }
      ];

      const random =
        fakeResults[Math.floor(Math.random() * fakeResults.length)];

      setResult(random);

      setLoading(false);

    }, 2500);
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
              </p>

            </label>

            <button
              onClick={analyzeMedia}
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
                cursor: "pointer",
                boxShadow: "0 12px 30px rgba(37, 99, 235, 0.55)",
              }}
            >
              {loading ? "Scanning Media..." : "Analyze Media"}
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
                  : "rgba(34,197,94,0.15)",
              marginBottom: "10px",
            }}
          >
            {result.risk} RISK
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
                  color: "#60a5fa",
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
                    "linear-gradient(to right, #2563eb, #ef4444)",
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