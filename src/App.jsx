import React, { useState } from "react";
import { API_URL } from "./config";

function App() {
  const [username, setUsername] = useState("");
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    const res = await fetch(\`\${API_URL}/analyze\`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username }),
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>InfluencerBase</h1>
      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Instagram kullanıcı adı"
        style={{ padding: "0.5rem", width: "300px" }}
      />
      <button onClick={handleAnalyze} style={{ marginLeft: "1rem", padding: "0.5rem" }}>
        Analiz Et
      </button>

      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h2>@{result.username}</h2>
          <p>Takipçi: {result.follower_count}</p>
          <p>Ortalama Beğeni: {result.average_likes}</p>
          <p>Ortalama Yorum: {result.average_comments}</p>
          <p>Etkileşim Oranı: {result.engagement_rate}%</p>
          <p>İşbirlikleri: {result.last_collaborations.join(", ")}</p>
        </div>
      )}
    </div>
  );
}

export default App;