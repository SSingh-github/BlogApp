from flask import Flask, request, jsonify
from db import get_db_connection
app = Flask(__name__)

# article can have: date of publishing, hashtags, content, id, author

#improve these apis by using better suggestions 
#after that integrate database into it
#after that write unit tests to test these apis

@app.route('/articles', methods=['GET'])
def get_all_articles():
    """
    Endpoint to fetch all articles from the articles table.
    """
    if request.method == 'GET':
        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Fetch all articles
            fetch_query = "SELECT * FROM articles"
            cursor.execute(fetch_query)
            articles = cursor.fetchall()

            # Close the connection
            cursor.close()
            conn.close()

            # Check if articles exist
            if len(articles) > 0:
                return jsonify(articles), 200  # Return articles with a 200 OK status
            else:
                return jsonify({"message": "No articles found"}), 404  # 404 Not Found

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Internal Server Error

    else:
        return jsonify({"error": f"{request.method} is not supported for this URL path"}), 405  # 405 Method Not Allowed

@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    """
    Endpoint to fetch a single article by its ID.
    """
    if request.method == 'GET':
        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Query to fetch the article by ID
            fetch_query = "SELECT * FROM articles WHERE id = %s"
            cursor.execute(fetch_query, (id,))
            article = cursor.fetchone()

            # Close the connection
            cursor.close()
            conn.close()

            # Check if the article exists
            if article:
                return jsonify(article), 200  # 200 OK
            else:
                return jsonify({"message": "No article found with the given ID"}), 404  # 404 Not Found

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Internal Server Error

    
@app.route('/articles_filtered', methods=['GET'])
def get_articles_by_filtering():
    """
    Endpoint to filter articles by hashtag or publishing date.
    """
    if request.method == 'GET':
        try:
            # Parse the request JSON data
            data = request.json
            hashtag = data.get('hashtag')
            date = data.get('publishing_date')

            # Build the base query and filters
            filters = []
            query = "SELECT * FROM articles WHERE"

            if hashtag:
                filters.append("hashtags LIKE %s")
            if date:
                filters.append("date_of_publishing = %s")

            # Join filters with AND
            query += " AND ".join(filters)

            # Prepare query parameters
            params = []
            if hashtag:
                params.append(f"%{hashtag}%")
            if date:
                params.append(date)

            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Execute the query
            cursor.execute(query, params)
            filtered_articles = cursor.fetchall()

            # Close the connection
            cursor.close()
            conn.close()

            # Return results
            if filtered_articles:
                return jsonify(filtered_articles), 200  # 200 OK
            else:
                return jsonify({"message": "No articles found matching the criteria"}), 404  # 404 Not Found

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Internal Server Error
            
@app.route('/create', methods=['POST'])
def create_article():
    """
    Endpoint to create an article and insert it into the articles table.
    Request body example:
    {
        "author": "John Doe",
        "date_of_publishing": "2025-01-05",
        "hashtags": ["#tech", "#python", "#programming"],
        "content": "This is a dummy article about programming and Python. It covers basic concepts and features."
    }
    """
    if request.method == 'POST':
        try:
            # Parse request data
            data = request.json
            author = data['author']
            date = data['date_of_publishing']
            hashtags = ','.join(data['hashtags'])  # Convert list of hashtags to comma-separated string
            content = data['content']

            # Insert the article into the database
            conn = get_db_connection()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO articles (author, date_of_publishing, hashtags, content)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (author, date, hashtags, content))
            conn.commit()

            # Fetch the last inserted ID to return as part of the response
            article_id = cursor.lastrowid
            cursor.close()
            conn.close()

            # Construct response object
            article = {
                "id": article_id,
                "author": author,
                "date_of_publishing": date,
                "hashtags": data['hashtags'],  # Keep the original format
                "content": content
            }
            return jsonify(article), 201  # 201 Created

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Internal Server Error
        

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_article(id):
    """
    Endpoint to delete an article by its ID.
    """
    if request.method == 'DELETE':
        try:
            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the article exists
            fetch_query = "SELECT * FROM articles WHERE id = %s"
            cursor.execute(fetch_query, (id,))
            article = cursor.fetchone()

            if not article:
                cursor.close()
                conn.close()
                return jsonify({"message": "No article found with the given ID"}), 404  # 404 Not Found

            # Delete the article
            delete_query = "DELETE FROM articles WHERE id = %s"
            cursor.execute(delete_query, (id,))
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            return jsonify({"message": "Article deleted successfully", "deleted_article": article}), 200  # 200 OK

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Internal Server Error

    
@app.route('/update/<int:id>', methods=['PUT'])
def update_article(id):
    """
    Endpoint to update an article by its ID.
    """
    if request.method == 'PUT':
        try:
            # Parse request data
            data = request.json
            author = data.get('author')
            date = data.get('date_of_publishing')
            hashtags = ','.join(data.get('hashtags', []))  # Convert list to string if provided
            content = data.get('content')

            # Connect to the database
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the article exists
            fetch_query = "SELECT * FROM articles WHERE id = %s"
            cursor.execute(fetch_query, (id,))
            article = cursor.fetchone()

            if not article:
                cursor.close()
                conn.close()
                return jsonify({"message": "No article found with the given ID"}), 404  # 404 Not Found

            # Update the article
            update_query = """
                UPDATE articles
                SET author = %s, date_of_publishing = %s, hashtags = %s, content = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (author, date, hashtags, content, id))
            conn.commit()

            # Fetch the updated article
            cursor.execute(fetch_query, (id,))
            updated_article = cursor.fetchone()

            # Close the connection
            cursor.close()
            conn.close()

            return jsonify(updated_article), 200  # 200 OK

        except Exception as e:
            return jsonify({"error": str(e)}), 500  # Internal Server Error


if __name__ == '__main__':
    app.run(debug=True)


