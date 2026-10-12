from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://monitor:monitor123@localhost:5432/platform_monitor"
db = SQLAlchemy(app)

class ServerStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.String(20))
    cpu = db.Column(db.Float)
    players = db.Column(db.Integer)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

SERVICE_NAMES = ["CS-PH-02", "JVD-ND-NB-04", "JVD-ND-NB-05"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/servers")
def get_servers():
    # 每次呼叫，模擬產生一筆新的監控紀錄並存進資料庫
    for name in SERVICE_NAMES:
        record = ServerStatus(
            name=name,
            status=random.choice(["online", "online", "online", "offline"]),
            cpu=round(random.uniform(10, 90), 1),
            players=random.randint(0, 500)
        )
        db.session.add(record)
    db.session.commit()

    # 回傳每個服務「最新一筆」紀錄
    latest = []
    for name in SERVICE_NAMES:
        record = ServerStatus.query.filter_by(name=name).order_by(ServerStatus.recorded_at.desc()).first()
        latest.append({
            "name": record.name,
            "status": record.status,
            "cpu": record.cpu,
            "players": record.players,
            "recorded_at": record.recorded_at.isoformat()
        })
    return jsonify(latest)

@app.route("/api/history/<name>")
def get_history(name):
    records = ServerStatus.query.filter_by(name=name).order_by(ServerStatus.recorded_at.desc()).limit(20).all()
    return jsonify([{
        "status": r.status,
        "cpu": r.cpu,
        "players": r.players,
        "recorded_at": r.recorded_at.isoformat()
    } for r in records])

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
