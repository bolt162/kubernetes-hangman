import os
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Service URLs - can be overridden by environment variables
GAME_SERVICE_URL = os.environ.get('GAME_SERVICE_URL', 'http://localhost:5001')
LEADERBOARD_SERVICE_URL = os.environ.get('LEADERBOARD_SERVICE_URL', 'http://localhost:5002')

@app.route('/')
def home():
    try:
        response = requests.get(f'{LEADERBOARD_SERVICE_URL}/api/leaderboard', timeout=5)
        games = response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        games = []

    return render_template('home.html', games=games)

@app.route('/play')
def new_game():
    player = request.args.get('player', 'Anonymous')

    try:
        response = requests.post(
            f'{GAME_SERVICE_URL}/api/game/new',
            json={'player': player},
            timeout=5
        )
        game_data = response.json()
        game_id = game_data['id']
    except Exception as e:
        print(f"Error creating game: {e}")
        return "Error creating game", 500

    return redirect(url_for('play', game_id=game_id))

@app.route('/play/<int:game_id>', methods=['GET', 'POST'])
def play(game_id):
    try:
        if request.method == 'POST':
            letter = request.form.get('letter', '').upper()
            if len(letter) == 1 and letter.isalpha():
                requests.post(
                    f'{GAME_SERVICE_URL}/api/game/{game_id}/guess',
                    json={'letter': letter},
                    timeout=5
                )

        response = requests.get(f'{GAME_SERVICE_URL}/api/game/{game_id}', timeout=5)
        game = response.json()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(
                current=game['current'],
                errors=game['errors'],
                finished=game['finished']
            )
        else:
            return render_template('play.html', game=game)

    except Exception as e:
        print(f"Error in play route: {e}")
        return "Error loading game", 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'frontend'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
