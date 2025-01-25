from flask import Flask, request, jsonify
from recommendation_script import recommend_movies
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app)  # This helps with potential cross-origin issues

@app.route('/recommend', methods=['GET'])
def recommend():
    # Print for debugging
    print("Recommendation endpoint hit!")
    
    # Get the movie title from the query parameters
    title = request.args.get('title')
    print(f"Requested title: {title}")
    
    if not title:
        print("No title provided")
        return jsonify({'error': 'No title provided'}), 400
    
    try:
        # Get recommendations
        recommendations = recommend_movies(title)
        print(f"Recommendations: {recommendations}")
        return jsonify({'recommendations': recommendations})
    
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        return jsonify({'error': str(e)}), 404
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)