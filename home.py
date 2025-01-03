from flask import Flask

app =Flask (__name__)

@app.route('/')

def first():
    return "Hey urvi..."

app.run(debug=True)