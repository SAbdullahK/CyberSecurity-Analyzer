import sqlite3

class FeedbackLearner:
    def __init__(self, db="feedback/db"):
        self.conn = sqlite3.connect(db)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS feedback (alert_id TEXT, decision TEXT)"
        )

    def process_feedback(self, alert_id, decision):
        self.conn.execute("INSERT INTO feedback VALUES (?, ?)", (alert_id, decision))
        self.conn.commit()
        