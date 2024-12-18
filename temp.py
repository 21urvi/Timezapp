from flask import Flask, render_template

app = Flask(__name__)

# Route for the homepage (index.html)
@app.route('/')
def first():
    return render_template('index.html')

# Route for landing.html
@app.route('/landing.html')
def landing():
    return render_template('landing.html')

if __name__ == '__main__':
    app.run(debug=True)
