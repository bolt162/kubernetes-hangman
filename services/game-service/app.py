import random
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration - supports both SQLite (local) and PostgreSQL (production)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///hangman.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Helper functions
def random_pk():
    return random.randint(int(1e9), int(1e10))

def random_word():
    words_file = os.environ.get('WORDS_FILE', '/app/words.txt')
    with open(words_file) as f:
        words = [line.strip() for line in f if len(line) > 10]
    return random.choice(words).upper()

# Game Model
class Game(db.Model):
    __tablename__ = 'games'

    pk = db.Column(db.Integer, primary_key=True, default=random_pk)
    word = db.Column(db.String(50), default=random_word)
    tried = db.Column(db.String(50), default='')
    player = db.Column(db.String(50))

    def __init__(self, player):
        self.player = player

    @property
    def errors(self):
        return ''.join(set(self.tried) - set(self.word))

    @property
    def current(self):
        return ''.join([c if c in self.tried else '_' for c in self.word])

    @property
    def points(self):
        return 100 + 2*len(set(self.word)) + len(self.word) - 10*len(self.errors)

    def try_letter(self, letter):
        if not self.finished and letter not in self.tried:
            self.tried += letter
            db.session.commit()

    @property
    def won(self):
        return self.current == self.word

    @property
    def lost(self):
        return len(self.errors) == 6

    @property
    def finished(self):
        return self.won or self.lost

    def to_dict(self):
        return {
            'id': self.pk,
            'word': self.word if self.finished else None,
            'current': self.current,
            'tried': self.tried,
            'errors': self.errors,
            'player': self.player,
            'points': self.points,
            'won': self.won,
            'lost': self.lost,
            'finished': self.finished
        }

# API Routes
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'game-service'}), 200

@app.route('/api/game/new', methods=['POST'])
def new_game():
    data = request.get_json()
    player = data.get('player', 'Anonymous')

    game = Game(player)
    db.session.add(game)
    db.session.commit()

    return jsonify(game.to_dict()), 201

@app.route('/api/game/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify(game.to_dict()), 200

@app.route('/api/game/<int:game_id>/guess', methods=['POST'])
def guess_letter(game_id):
    game = Game.query.get_or_404(game_id)

    data = request.get_json()
    letter = data.get('letter', '').upper()

    if len(letter) == 1 and letter.isalpha():
        game.try_letter(letter)

    return jsonify(game.to_dict()), 200

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
