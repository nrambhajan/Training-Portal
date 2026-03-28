import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()
q = db.query(models.Question).filter(models.Question.module_id == 14, models.Question.order == 23).first()
q.verify_command = 'find /home/*/mail/*/*/ -maxdepth 0 -type d 2>/dev/null | wc -l | xargs test 0 -lt && echo email_exists'
q.verify_expected = 'email_exists'
db.commit()
print(f"Fixed Q23: {q.verify_command}")
db.close()
