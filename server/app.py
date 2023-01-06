#!/usr/bin/env python3

#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price
        }
        games.append(game_dict)

    response = make_response(
        jsonify(games),
        200
    )

    return response

@app.route('/games_by/<title>')
def games_by_title(title):
    games = Game.query.all()
    filtered_games = []

    for game in games:
        # breakpoint()
        if title.lower() in game.title.lower():
            filtered_games.append({
                "id": game.id,
                "title": game.title,
                "genre": game.genre,
                "platform": game.platform,
                "price": game.price 
            })
    resp = make_response(jsonify(filtered_games), 200, {"Content-Type": "application/json"})

    return resp

@app.route("/first-ten")
def first_ten():
    first_10 = Game.query.limit(10).all()
    ten_dicts = []
    for game in first_10:
        ten_dicts.append({
                "id": game.id,
                "title": game.title,
                "genre": game.genre,
                "platform": game.platform,
                "price": game.price 
            })
    resp = make_response(ten_dicts, 200)
    return resp

@app.route("/games/<int:id>")
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    game_dict = game.to_dict()

    resp = make_response(
        jsonify(game_dict),
        200,
    )
    resp.headers["Content-Type"] = "application/json"

    return resp
if __name__ == '__main__':
    app.run(port=5555, debug=True)