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


if __name__ == '__main__':
    app.run(debug=True)


