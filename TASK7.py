from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("bowling.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)
        conn.commit()
init_db()


@app.route('/scores', methods=['POST'])
def submit_score():
    data = request.json
    player, score = data.get("player"), data.get("score")
    
    if not player or score is None:
        return jsonify({"error": "Player name and score are required"}), 400

    with sqlite3.connect("bowling.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (player, score) VALUES (?, ?)", (player, score))
        conn.commit()

    return jsonify({"message": "Score submitted successfully"}), 201  
@app.route('/scores', methods=['GET'])
def view_leaderboard():
    with sqlite3.connect("bowling.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scores ORDER BY score DESC")
        scores = [{"id": row[0], "player": row[1], "score": row[2]} for row in cursor.fetchall()]

    return jsonify(scores), 200

# حذف النتيجة (DELETE /scores/:id)
@app.route('/scores/<int:score_id>', methods=['DELETE'])
def delete_score(score_id):
    with sqlite3.connect("bowling.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM scores WHERE id = ?", (score_id,))
        if cursor.rowcount == 0:
            return jsonify({"error": "Score not found"}), 404
        conn.commit() 
    return jsonify({"message": "Score deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True) 
