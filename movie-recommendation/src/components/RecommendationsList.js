import React from "react";

function RecommendationsList({ recommendations, loading, error }) {
  if (loading) return <p>Loading recommendations...</p>;
  if (error) return <p className="error">{error}</p>;
  if (recommendations.length === 0) return <p>No recommendations to display.</p>;

  return (
    <ul className="recommendations-list">
      {recommendations.map((movie, index) => (
        <li key={index}>{movie}</li>
      ))}
    </ul>
  );
}


export default RecommendationsList;
