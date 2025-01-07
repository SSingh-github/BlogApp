from flask import Flask, request, jsonify

app = Flask(__name__)

# article can have: date of publishing, hashtags, content, id, author
articles = [
    {
        "id": 1,
        "author": "John Doe",
        "date_of_publishing": "2025-01-05",
        "hashtags": [
            "#tech",
            "#python",
            "#programming"
        ],
        "content": "This is a dummy article about programming and Python. It covers basic concepts and features."
    },
    {
        "id": 2,
        "author": "Jane Smith",
        "date_of_publishing": "2025-01-06",
        "hashtags": [
            "#health",
            "#fitness",
            "#wellness"
        ],
        "content": "This article discusses the importance of staying fit and eating healthy to lead a balanced lifestyle."
    },
    {
        "id": 3,
        "author": "Alex Johnson",
        "date_of_publishing": "2025-01-07",
        "hashtags": [
            "#travel",
            "#adventure",
            "#wanderlust"
        ],
        "content": "Traveling to new places opens your mind to different cultures and experiences. Here's why you should travel more."
    },
    {
        "id": 4,
        "author": "Emily Brown",
        "date_of_publishing": "2025-01-08",
        "hashtags": [
            "#finance",
            "#investment",
            "#stocks"
        ],
        "content": "In this article, we explore the basics of stock market investments and how to get started in finance."
    },
    {
        "id": 5,
        "author": "Michael Davis",
        "date_of_publishing": "2025-01-09",
        "hashtags": [
            "#music",
            "#entertainment",
            "#reviews"
        ],
        "content": "Music is a vital part of our daily lives. This article reviews the latest album by one of the top artists in the industry."
    }
]


# routes can be: get api to fetch all the articles
# get api to fetch the articles with given hashtag or publishing date
# get api to fetch the article with a particular id
# post api to create an article with given details
# delete an article with given id
# update an article with given id and details 


@app.route('/articles', methods=['GET'])
def get_all_articles():
    if request.method == 'GET':
        if len(articles) > 0:
            return jsonify(articles)
        else:
            return 'Nothing found'
    else:
        return '{} is not supported for this url path'.format(request.method)

@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):
    if request.method == 'GET':
        if len(articles) > 0:
            for article in articles:
                if article['id'] == id:
                    return jsonify(article)
            return 'No article found with given id'
        else:
            return 'Nothing found'
    else:
        return '{} is not supported for this url path'.format(request.method)
    
@app.route('/articles_filtered', methods=['GET'])
def get_articles_by_filtering():
    if request.method == 'GET':
        data = request.json
        hashtag = data['hashtag']
        date = data['publishing_date']

        for article in articles:
            if hashtag in article['hashtags']:
                return jsonify(article)
            elif date == article['date_of_publishing']:
                return jsonify(article)

@app.route('/create', methods=['POST'])
def create_article():
    """
    "id": 1,
        "author": "John Doe",
        "date_of_publishing": "2025-01-05",
        "hashtags": [
            "#tech",
            "#python",
            "#programming"
        ],
        "content": "This is a dummy article about programming and Python. It covers basic concepts and features."
    """
    if request.method =='POST':
        data = request.json
        author = data['author']
        date = data['date_of_publishing']
        hashtags = data['hashtags']
        content = data['content']

        article = {
            "id": len(articles) + 1,
            "author": author,
            "date_of_publishing": date,
            "hashtags": hashtags,
            "content": content
        }
        articles.append(article)
        return jsonify(articles[len(articles) -1])

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_article(id):
    if request.method =='DELETE':
        for article in articles:
            if article['id'] == id:
                articles.remove(article)
                return jsonify(article)
    else:
        return "not a valid method"
    

@app.route('/update/<int:id>', methods=['PUT'])
def update_article(id):
    if request.method == 'PUT':
        for article in articles:
            if article['id'] == id:
                data = request.json
                article['author'] = data['author']
                return jsonify(article)
            else:
                return "no article with given id"

if __name__ == '__main__':
    app.run(debug=True)


