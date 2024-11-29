from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/messages_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)


@app.before_first_request
def create_tables():
    db.create_all()
    if not Message.query.first():
        messages = [
            "Today is your lucky day!",
            "Hard work pays off!",
            "Be kind to yourself and others.",
            "Success is around the corner.",
            "You are capable of amazing things!"
        ]
        for msg in messages:
            db.session.add(Message(text=msg))
        db.session.commit()


@app.route("/")
def get_random_message():
    messages = Message.query.all()
    if messages:
        random_message = random.choice(messages)
        return jsonify({"message": random_message.text})
    else:
        return jsonify({"error": "No messages found in the database."}), 404


@app.route("/health")
def health_check():
    return jsonify({"status": "OK"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
