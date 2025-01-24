from flask import Flask, request, jsonify
from recommendation_script import recommend_movies

app = Flask(__name__)

@app.route('/recommend', methods=['GET'])
def recommend():
    # Get the movie title from the query parameters
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'No title provided'}), 400

    try:
        # Get recommendations
        recommendations = recommend_movies(title)
        return jsonify({'recommendations': recommendations})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
