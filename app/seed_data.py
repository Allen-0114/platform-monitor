import random
from datetime import datetime
from main import app, db, ServerStatus, SERVICE_NAMES

def record_snapshot():
    with app.app_context():
        for name in SERVICE_NAMES:
            record = ServerStatus(
                name=name,
                status=random.choice(["online", "online", "online", "offline"]),
                cpu=round(random.uniform(10, 90), 1),
                players=random.randint(0, 500)
            )
            db.session.add(record)
        db.session.commit()
        print(f"{datetime.now()}: 寫入一批監控資料")

if __name__ == "__main__":
    record_snapshot()
