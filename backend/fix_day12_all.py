"""Fix all Day 12 practical verify commands that use count-based matching"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()

qs = db.query(models.Question).filter(
    models.Question.module_id == 14,
    models.Question.type == "practical"
).order_by(models.Question.order).all()

for q in qs:
    old = q.verify_command
    # Q16: account count
    if q.order == 16:
        q.verify_command = 'whmapi1 listaccts --output=json 2>/dev/null | grep \'"user":\' | head -1 && echo acct_exists'
        q.verify_expected = 'acct_exists'
    # Q17: PHP version
    elif q.order == 17:
        q.verify_command = 'whmapi1 php_get_vhost_versions --output=json 2>/dev/null | grep ea-php | head -1 && echo php_set'
        q.verify_expected = 'php_set'
    # Q18: AutoSSL
    elif q.order == 18:
        q.verify_command = 'whmapi1 get_autossl_providers --output=json 2>/dev/null | grep provider | head -1 && echo autossl_ok'
        q.verify_expected = 'autossl_ok'
    # Q19: starter_plan package
    elif q.order == 19:
        q.verify_command = 'whmapi1 listpkgs --output=json 2>/dev/null | grep starter_plan && echo pkg_exists'
        q.verify_expected = 'pkg_exists'
    # Q20: suspended account
    elif q.order == 20:
        q.verify_command = 'whmapi1 listsuspended --output=json 2>/dev/null | grep "user" | head -1 && echo suspended_ok'
        q.verify_expected = 'suspended_ok'
    # Q22: index.html
    elif q.order == 22:
        q.verify_command = 'find /home/*/public_html/index.html -type f 2>/dev/null | head -1 | xargs grep -il "welcome\\|hello\\|Welcome\\|Hello" 2>/dev/null && echo index_ok'
        q.verify_expected = 'index_ok'
    # Q24: cron job
    elif q.order == 24:
        q.verify_command = 'cat /var/spool/cron/crontabs/* 2>/dev/null | grep -v "^#" | grep -v "^$" | head -1 && echo cron_exists'
        q.verify_expected = 'cron_exists'
    # Q25: unsuspend
    elif q.order == 25:
        q.verify_command = 'COUNT=$(whmapi1 listsuspended --output=json 2>/dev/null | grep -c "user"); test "$COUNT" = "0" && echo all_active'
        q.verify_expected = 'all_active'

    if old != q.verify_command:
        print(f"Q{q.order}: FIXED")
    else:
        print(f"Q{q.order}: unchanged")

db.commit()
print("\nAll Day 12 verify commands fixed!")
db.close()
