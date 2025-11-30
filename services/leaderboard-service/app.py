import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///hangman.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Use the same Game model to access completed games
class Game(db.Model):
    __tablename__ = 'games'

    pk = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    tried = db.Column(db.String(50))
    player = db.Column(db.String(50))

    @property
    def errors(self):
        return ''.join(set(self.tried) - set(self.word))

    @property
    def current(self):
        return ''.join([c if c in self.tried else '_' for c in self.word])

    @property
    def points(self):
        return 100 + 2*len(set(self.word)) + len(self.word) - 10*len(self.errors)

    @property
    def won(self):
        return self.current == self.word

    def to_dict(self):
        return {
            'id': self.pk,
            'player': self.player,
            'points': self.points,
            'word': self.word,
            'won': self.won
        }

# API Routes
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'leaderboard-service'}), 200

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    # Get all won games, sorted by points
    games = Game.query.all()
    won_games = [game for game in games if game.won]
    sorted_games = sorted(won_games, key=lambda g: -g.points)[:10]

    leaderboard = [game.to_dict() for game in sorted_games]
    return jsonify(leaderboard), 200

@app.route('/api/leaderboard/player/<player_name>', methods=['GET'])
def get_player_stats(player_name):
    games = Game.query.filter_by(player=player_name).all()
    won_games = [game for game in games if game.won]

    stats = {
        'player': player_name,
        'total_games': len(games),
        'won_games': len(won_games),
        'best_score': max([game.points for game in won_games]) if won_games else 0,
        'games': [game.to_dict() for game in won_games]
    }

    return jsonify(stats), 200

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
