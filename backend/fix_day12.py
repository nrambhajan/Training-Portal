"""Fix Day 12 practical verify commands"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal
import models

db = SessionLocal()

qs = db.query(models.Question).filter(
    models.Question.module_id == 14,
    models.Question.type == "practical"
).order_by(models.Question.order).all()

qs_map = {q.order: q for q in qs}

# Q16: Create cPanel account
qs_map[16].text = "Create a new cPanel account in WHM with any domain name, username, and a strong password using the default package.\n\nUse WHM > Account Functions > Create a New Account."
qs_map[16].verify_command = 'whmapi1 listaccts --output=json 2>/dev/null | grep -c \'"user":\''
qs_map[16].verify_expected = "1"

# Q17: PHP version
qs_map[17].text = "Using WHM MultiPHP Manager, verify or change the PHP version for any account. Ensure at least one domain has a PHP version assigned.\n\nGo to WHM > Software > MultiPHP Manager."
qs_map[17].verify_command = "whmapi1 php_get_vhost_versions --output=json 2>/dev/null | grep -c ea-php"
qs_map[17].verify_expected = "1"

# Q18: AutoSSL
qs_map[18].text = "Navigate to WHM > SSL/TLS > Manage AutoSSL and verify AutoSSL is configured with a provider. Run AutoSSL check for any account."
qs_map[18].verify_command = "whmapi1 get_autossl_providers --output=json 2>/dev/null | grep -c provider"
qs_map[18].verify_expected = "1"

# Q19: Create hosting package starter_plan
qs_map[19].verify_command = "whmapi1 listpkgs --output=json 2>/dev/null | grep -c starter_plan"
qs_map[19].verify_expected = "1"

# Q20: Suspend account
qs_map[20].text = "Suspend any one cPanel account from WHM with the reason 'Payment overdue'.\n\nGo to WHM > Account Functions > Suspend/Unsuspend Account."
qs_map[20].verify_command = 'whmapi1 listsuspended --output=json 2>/dev/null | grep -c "user"'
qs_map[20].verify_expected = "1"

# Q21: Create MySQL DB
qs_map[21].text = "Log into cPanel as any user and create a MySQL database and a database user. Grant ALL PRIVILEGES to the user on the database.\n\nIn cPanel, go to Databases > MySQL Databases."
qs_map[21].verify_command = "mysql -e 'SHOW DATABASES;' 2>/dev/null | grep -v -c -E 'Database|information_schema|mysql|performance_schema|sys|cphulkd|eximstats|leechprotect|modsec|roundcube|whmxfer'"
qs_map[21].verify_expected = "1"

# Q22: Create index.html
qs_map[22].text = "Using cPanel File Manager for any user, create or edit the index.html file in public_html with a welcome message.\n\nExample: <h1>Welcome to my website</h1>"
qs_map[22].verify_command = "find /home/*/public_html/index.html -type f 2>/dev/null | wc -l"
qs_map[22].verify_expected = "1"

# Q23: Email account
qs_map[23].text = "Create an email account in cPanel for any domain (e.g., support@yourdomain.com) with a mailbox quota of 500 MB.\n\nGo to cPanel > Email > Email Accounts > Create."
qs_map[23].verify_command = "whmapi1 listaccts --output=json 2>/dev/null | grep -o '\"domain\"' | head -1 && find /home/*/mail/*/ -maxdepth 0 -type d 2>/dev/null | wc -l"
qs_map[23].verify_expected = "1"

# Q24: Cron job
qs_map[24].text = "Create a cron job in cPanel for any user that runs at any schedule.\n\nExample: 0 2 * * * /usr/bin/date >> /home/youruser/cron.log\n\nGo to cPanel > Advanced > Cron Jobs."
qs_map[24].verify_command = "cat /var/spool/cron/crontabs/* 2>/dev/null | grep -v '^#' | grep -v '^$' | grep -c '.'"
qs_map[24].verify_expected = "1"

# Q25: Unsuspend
qs_map[25].text = "Unsuspend the account you suspended in the previous task. All accounts should be active (not suspended).\n\nGo to WHM > Account Functions > Unsuspend Account."
qs_map[25].verify_command = 'whmapi1 listsuspended --output=json 2>/dev/null | grep -c "user"'
qs_map[25].verify_expected = "0"

db.commit()
print("Fixed all 10 Day 12 practical verify commands!")
db.close()
