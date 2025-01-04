from flask import Flask, render_template

app = Flask(__name__ , static_folder='static')

'''@app.route('/')
def login():
    return render_template('login.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')'''

# Route for the homepage (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route for landing.html
@app.route('/masonry.html')
def masonry():
    return render_template('masonry.html')

@app.route('/single-post.html')
def single():
    return render_template('single-post.html')

@app.route('/grid.html')
def grid():
    return render_template('grid.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)