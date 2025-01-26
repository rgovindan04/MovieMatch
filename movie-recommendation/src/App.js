import React, { useState } from "react";
import axios from "axios"; // Import axios for HTTP requests
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

    if (!movie.trim()) {
      setError("Please enter a movie title.");
      setLoading(false);
      return;
    }

    try {
      const response = await axios.get(`http://127.0.0.1:5001/recommend?title=${movie}`);
      console.log("Response data:", response.data); // Log the response from the backend
      setRecommendations(response.data.recommendations || []);
      console.log("Updated recommendations:", response.data.recommendations); // Debug
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
