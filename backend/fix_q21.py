import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()
q = db.query(models.Question).filter(models.Question.module_id == 14, models.Question.order == 21).first()
q.verify_command = "mysql -e 'SHOW DATABASES;' 2>/dev/null | grep -v -E 'Database|information_schema|mysql|performance_schema|sys|cphulkd|eximstats|leechprotect|modsec|roundcube|whmxfer' | head -1 | xargs -I{} echo db_exists"
q.verify_expected = "db_exists"
db.commit()
print(f"Fixed Q21: {q.verify_command}")
db.close()
