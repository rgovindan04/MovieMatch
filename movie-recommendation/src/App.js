import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import RecommendationsList from "./components/RecommendationsList";
import "./App.css";

function App() {
  const [movie, setMovie] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchRecommendations = async () => {
    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
      const response = await fetch(`http://localhost:5000/recommend?title=${movie}`);
      if (!response.ok) {
        throw new Error("Failed to fetch recommendations.");
      }
      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Movie Recommendation System</h1>
      <SearchBar movie={movie} setMovie={setMovie} fetchRecommendations={fetchRecommendations} />
      <RecommendationsList
        recommendations={recommendations}
        loading={loading}
        error={error}
      />
    </div>
  );
}

export default App;
