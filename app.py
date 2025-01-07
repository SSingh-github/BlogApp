from flask import Flask

app = Flask(__name__)


@app.route('/')
#this is a view function
def hello():
    return 'Hello, world!'

#dynamic routing
@app.route('/<name>')
def print_name(name):
    return 'Hi,{}'.format(name)


if __name__ == '__main__':
    app.run(debug=True)