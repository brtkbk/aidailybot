from flask import Flask, render_template, request
import sqlite3

app = Flask("ai_daily_bot")

# Database connection
def get_db_connection():
    conn = sqlite3.connect("ai_daily_bot.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/news")
def news():
    conn = get_db_connection()
    news_items = conn.execute("SELECT * FROM news ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("news.html", news=news_items)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    conn = get_db_connection()
    quizzes = conn.execute("SELECT * FROM quizzes ORDER BY date DESC").fetchall()
    conn.close()

    results = None
    if request.method == "POST":
        results = []
        for quiz in quizzes:
            user_answer = request.form.get(f"answer_{quiz['id']}")
            if user_answer:
                if user_answer.lower() == quiz['answer'].lower():
                    results.append(f"Correct! {quiz['question']} - {quiz['answer']}")
                else:
                    results.append(f"Incorrect. {quiz['question']} - Correct Answer: {quiz['answer']}")
            else:
                results.append(f"No answer provided for: {quiz['question']}")

    return render_template("quiz.html", quizzes=quizzes, results=results)

@app.route("/topics")
def topics():
    conn = get_db_connection()
    topics = conn.execute("SELECT * FROM topics ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("topics.html", topics=topics)

if __name__ == "__main__":
    app.run(debug=True)