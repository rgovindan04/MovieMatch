import React from "react";

function SearchBar({ movie, setMovie, fetchRecommendations }) {
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Enter a movie title"
        value={movie}
        onChange={(e) => setMovie(e.target.value)}
      />
      <button onClick={fetchRecommendations} disabled={!movie}>
        Get Recommendations
      </button>
    </div>
  );
}

export default SearchBar;
