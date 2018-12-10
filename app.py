#!/usr/bin/env python
import flask
from flask import request
app = flask.Flask(__name__)
from userbased import get_recommendation as get_rec


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/get_recommendations', methods=['GET', 'POST'])
def get_recommendations():
    params = request.form
    try:
        ans = get_rec(params.get("user_id"))
        return "<br>".join(["Moive name: %s, rating: %s" % (i[0], i[1]) for i in ans])
    except Exception as e:
        return "error: %s" % e


if __name__ == '__main__':
    app.run(debug=True, port=6000)
