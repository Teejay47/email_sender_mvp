from app.core.database import SessionLocal
from app.models import Recipient

db = SessionLocal()
for r in db.query(Recipient).all():
    print(r.id, r.email)
db.close()
