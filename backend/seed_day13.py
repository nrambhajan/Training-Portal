"""
Day 13 — LAMP Setup & WordPress Troubleshooting (RHCE-style)
Run once: python3 seed_day13.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

module = models.Module(
    title="Day 13 - LAMP Setup & WordPress Troubleshooting",
    description="Build a LAMP stack from scratch, install WordPress, then fix real-world server issues. Complete tasks in order — each task builds on the previous one.",
    sort_order=13,
    unlock_percent=0,
    is_published=False,
    time_limit=120,
)
db.add(module)
db.commit()
db.refresh(module)

questions = [
    # ── Phase 1: LAMP Setup ────────────────────────────────────────────────
    {
        "type": "practical",
        "text": "SETUP 1 - Install Apache Web Server\n\nInstall the Apache2 web server on your server and make sure it is running.\n\nSteps:\n1. Update package lists: sudo apt update\n2. Install Apache: sudo apt install apache2 -y\n3. Start and enable Apache: sudo systemctl enable --now apache2\n4. Verify by opening your server IP in browser — you should see the Apache default page.",
        "verify_command": "systemctl is-active apache2",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 2.0,
        "order": 1,
        "hint": "Use: sudo apt update && sudo apt install apache2 -y && sudo systemctl enable --now apache2",
    },
    {
        "type": "practical",
        "text": "SETUP 2 - Install MySQL Database Server\n\nInstall MySQL server and make sure it is running.\n\nSteps:\n1. Install MySQL: sudo apt install mysql-server -y\n2. Start and enable: sudo systemctl enable --now mysql\n3. Verify MySQL is running: sudo systemctl status mysql",
        "verify_command": "systemctl is-active mysql",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 2.0,
        "order": 2,
        "hint": "Use: sudo apt install mysql-server -y && sudo systemctl enable --now mysql",
    },
    {
        "type": "practical",
        "text": "SETUP 3 - Install PHP and Required Modules\n\nInstall PHP along with the modules needed for WordPress.\n\nSteps:\n1. Install PHP and common modules:\n   sudo apt install php libapache2-mod-php php-mysql php-curl php-gd php-mbstring php-xml php-xmlrpc php-zip -y\n2. Restart Apache: sudo systemctl restart apache2\n3. Verify PHP is working: php -v",
        "verify_command": "php -v 2>&1 | head -1",
        "verify_expected": "PHP",
        "verify_type": "contains",
        "points": 2.0,
        "order": 3,
        "hint": "Use: sudo apt install php libapache2-mod-php php-mysql php-curl php-gd php-mbstring php-xml php-xmlrpc php-zip -y",
    },
    {
        "type": "practical",
        "text": "SETUP 4 - Create MySQL Database and User for WordPress\n\nCreate a database called 'wordpress' and a user called 'wpuser' with password 'WPpass@123' that has full access to it.\n\nSteps:\n1. Login to MySQL: sudo mysql\n2. Run these SQL commands:\n   CREATE DATABASE wordpress;\n   CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'WPpass@123';\n   GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost';\n   FLUSH PRIVILEGES;\n   EXIT;",
        "verify_command": "sudo mysql -e \"SHOW DATABASES;\" 2>/dev/null | grep -c wordpress",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 2.0,
        "order": 4,
        "hint": "Login with 'sudo mysql' then run CREATE DATABASE wordpress; and create user wpuser@localhost",
    },
    {
        "type": "practical",
        "text": "SETUP 5 - Download and Install WordPress\n\nDownload WordPress and set it up in /var/www/html/\n\nSteps:\n1. cd /tmp\n2. wget https://wordpress.org/latest.tar.gz\n3. tar -xzf latest.tar.gz\n4. sudo cp -r wordpress/* /var/www/html/\n5. sudo chown -R www-data:www-data /var/www/html/\n6. sudo chmod -R 755 /var/www/html/\n7. Remove default index.html: sudo rm -f /var/www/html/index.html",
        "verify_command": "test -f /var/www/html/wp-login.php && echo 'wordpress_installed'",
        "verify_expected": "wordpress_installed",
        "verify_type": "contains",
        "points": 2.0,
        "order": 5,
        "hint": "Download from https://wordpress.org/latest.tar.gz, extract and copy contents to /var/www/html/",
    },
    {
        "type": "practical",
        "text": "SETUP 6 - Configure WordPress (wp-config.php)\n\nCreate the WordPress configuration file with the correct database details.\n\nSteps:\n1. cd /var/www/html/\n2. sudo cp wp-config-sample.php wp-config.php\n3. Edit wp-config.php and set:\n   - DB_NAME: wordpress\n   - DB_USER: wpuser\n   - DB_PASSWORD: WPpass@123\n   - DB_HOST: localhost\n4. Save the file\n5. Open your server IP in browser — you should see the WordPress setup wizard.",
        "verify_command": "grep -c 'wpuser' /var/www/html/wp-config.php 2>/dev/null",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 2.0,
        "order": 6,
        "hint": "Copy wp-config-sample.php to wp-config.php, then use nano to edit DB_NAME, DB_USER, DB_PASSWORD",
    },

    # ── Phase 2: Troubleshooting (Admin breaks things first) ───────────────
    {
        "type": "practical",
        "text": "TROUBLE 1 - Website Not Loading!\n\nA client reports their website is completely down — nothing loads in the browser. The web server seems to have stopped.\n\nDiagnose the issue and get the website back online.",
        "verify_command": "systemctl is-active apache2",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 3.0,
        "order": 7,
        "hint": "Check if the web server service is running. Use systemctl to check and start services.",
    },
    {
        "type": "practical",
        "text": "TROUBLE 2 - Error Establishing Database Connection\n\nThe website loads but shows 'Error establishing a database connection'. The database server has stopped.\n\nFix it and get the database running again.",
        "verify_command": "systemctl is-active mysql",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 3.0,
        "order": 8,
        "hint": "The MySQL service has stopped. Use systemctl to start it.",
    },
    {
        "type": "practical",
        "text": "TROUBLE 3 - Wrong Database Credentials\n\nMySQL is running but WordPress still can't connect. Someone changed the database password in wp-config.php to 'wrongpassword'.\n\nFix the wp-config.php file to use the correct database password: WPpass@123",
        "verify_command": "grep 'DB_PASSWORD' /var/www/html/wp-config.php | grep -c 'WPpass@123'",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 9,
        "hint": "Edit /var/www/html/wp-config.php and fix the DB_PASSWORD value back to WPpass@123",
    },
    {
        "type": "practical",
        "text": "TROUBLE 4 - 403 Forbidden Error\n\nThe website shows '403 Forbidden'. The file permissions on /var/www/html have been changed to 000 (no access).\n\nFix the permissions:\n- Directories should be 755\n- Files should be 644\n- Owner should be www-data:www-data",
        "verify_command": "stat -c '%a' /var/www/html",
        "verify_expected": "755",
        "verify_type": "contains",
        "points": 3.0,
        "order": 10,
        "hint": "Use chmod 755 for directories and chown www-data:www-data for ownership",
    },
    {
        "type": "practical",
        "text": "TROUBLE 5 - PHP Shows Raw Code\n\nThe website is showing raw PHP code instead of rendering the page. The PHP Apache module has been disabled.\n\nRe-enable PHP and get the site rendering properly.",
        "verify_command": "apache2ctl -M 2>/dev/null | grep -c php",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 11,
        "hint": "The PHP module was disabled with a2dismod. Use a2enmod to enable it, then restart Apache.",
    },
    {
        "type": "practical",
        "text": "TROUBLE 6 - Disk Space Full!\n\nThe server is running out of disk space. Someone created large junk files in /tmp.\n\nFind and remove the files named junk_* from /tmp to free up space.",
        "verify_command": "ls /tmp/junk_* 2>/dev/null | wc -l",
        "verify_expected": "0",
        "verify_type": "contains",
        "points": 3.0,
        "order": 12,
        "hint": "Use 'ls -lh /tmp/junk_*' to see the files, then 'rm /tmp/junk_*' to delete them",
    },
    {
        "type": "practical",
        "text": "TROUBLE 7 - Malware Found!\n\nA security scan flagged a suspicious file in the WordPress uploads directory. A file containing malicious PHP code (eval/base64_decode) was planted in /var/www/html/wp-content/uploads/.\n\nFind the malicious file and remove it.",
        "verify_command": "grep -rl 'eval(base64_decode' /var/www/html/wp-content/uploads/ 2>/dev/null | wc -l",
        "verify_expected": "0",
        "verify_type": "contains",
        "points": 3.0,
        "order": 13,
        "hint": "Use: grep -rl 'eval(base64_decode' /var/www/html/wp-content/uploads/ to find it, then rm to delete",
    },
    {
        "type": "practical",
        "text": "TROUBLE 8 - .htaccess Broken (500 Error)\n\nWordPress inner pages return 500 Internal Server Error. The .htaccess file has been corrupted with invalid directives.\n\nFix the .htaccess file by replacing its contents with the standard WordPress rules:\n\n# BEGIN WordPress\n<IfModule mod_rewrite.c>\nRewriteEngine On\nRewriteBase /\nRewriteRule ^index\\.php$ - [L]\nRewriteCond %{REQUEST_FILENAME} !-f\nRewriteCond %{REQUEST_FILENAME} !-d\nRewriteRule . /index.php [L]\n</IfModule>\n# END WordPress",
        "verify_command": "grep -c 'RewriteEngine On' /var/www/html/.htaccess 2>/dev/null",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 14,
        "hint": "Edit /var/www/html/.htaccess and replace contents with the standard WordPress rewrite rules",
    },
    {
        "type": "practical",
        "text": "TROUBLE 9 - DNS Resolution Broken\n\nThe server cannot resolve domain names. Commands like 'apt update' or 'curl google.com' fail. The /etc/resolv.conf has been corrupted.\n\nFix DNS by adding Google's nameserver (8.8.8.8) to /etc/resolv.conf.",
        "verify_command": "grep -c '8.8.8.8' /etc/resolv.conf",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 15,
        "hint": "Edit /etc/resolv.conf and add: nameserver 8.8.8.8",
    },
    {
        "type": "practical",
        "text": "TROUBLE 10 - Apache Config Error\n\nApache crashed and won't restart. A bad configuration file was added to /etc/apache2/conf-enabled/.\n\nFind the bad config file, remove it, and get Apache running again.\n\nTip: Use 'apache2ctl configtest' to find the error.",
        "verify_command": "systemctl is-active apache2 && apache2ctl configtest 2>&1 | grep -c 'Syntax OK'",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 16,
        "hint": "Run 'apache2ctl configtest' to see which file has the error, then remove that file and restart Apache",
    },

    # ── Phase 3: Knowledge MCQs ────────────────────────────────────────────
    {
        "type": "mcq",
        "text": "Which command checks Apache configuration for syntax errors?",
        "options": ["apache2 --check", "apache2ctl configtest", "apachectl validate", "systemctl test apache2"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 17,
    },
    {
        "type": "mcq",
        "text": "What is the default document root for Apache on Ubuntu?",
        "options": ["/var/www/", "/var/www/html/", "/usr/share/apache2/", "/etc/apache2/www/"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 18,
    },
    {
        "type": "mcq",
        "text": "Which file contains WordPress database connection settings?",
        "options": ["wp-settings.php", "wp-config.php", "wp-database.php", ".htaccess"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 19,
    },
    {
        "type": "mcq",
        "text": "What does '503 Service Unavailable' typically mean?",
        "options": ["Page not found", "User not authorized", "Server overloaded or backend service down", "SSL certificate expired"],
        "correct_answer": "2",
        "points": 1.0,
        "order": 20,
    },
    {
        "type": "mcq",
        "text": "Which command enables the Apache mod_rewrite module on Ubuntu?",
        "options": ["apache2ctl mod_rewrite enable", "a2enmod rewrite", "mod_rewrite --enable", "apachectl enable rewrite"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 21,
    },

    # ── Phase 4: Theory ────────────────────────────────────────────────────
    {
        "type": "short_answer",
        "text": "A client reports their WordPress site is extremely slow. List at least 5 things you would check to diagnose and fix the issue.",
        "correct_answer": "Check server resources (CPU, RAM, disk), check slow MySQL queries, check PHP error logs, check plugins for issues, check .htaccess for redirect loops, check for malware, enable caching, optimize database, check if CDN is configured, check Apache/Nginx error logs",
        "points": 3.0,
        "order": 22,
        "hint": "Think about: server resources, database, PHP, plugins, caching, logs",
    },
    {
        "type": "short_answer",
        "text": "How would you migrate a WordPress site from one server to another? List the step-by-step process.",
        "correct_answer": "1. Backup files (wp-content, themes, plugins) via tar/zip. 2. Export database using mysqldump. 3. Transfer files to new server via scp/rsync. 4. Create new database and user on new server. 5. Import database dump. 6. Update wp-config.php with new DB credentials. 7. Update site URL in database if domain changes. 8. Fix file permissions. 9. Test the site. 10. Update DNS if needed.",
        "points": 3.0,
        "order": 23,
        "hint": "Think about: files backup, database export, transfer, database import, config update, DNS",
    },
    {
        "type": "short_answer",
        "text": "Explain the correct file permissions for a WordPress installation and why they matter for security.",
        "correct_answer": "Directories: 755 (owner can read/write/execute, group and others can read/execute). Files: 644 (owner can read/write, group and others can read only). wp-config.php: 440 or 400 (restricted, only owner can read). Owner should be www-data (the Apache/Nginx user). Incorrect permissions can allow unauthorized users to modify files, upload malware, or read sensitive configuration like database credentials.",
        "points": 2.0,
        "order": 24,
        "hint": "Think about the difference between file and directory permissions, and which user Apache runs as",
    },
]

for q_data in questions:
    q = models.Question(module_id=module.id, **q_data)
    db.add(q)

db.commit()
print(f"Created module '{module.title}' (ID: {module.id}) with {len(questions)} questions")
print(f"  - 6 Setup tasks (LAMP + WordPress)")
print(f"  - 10 Troubleshooting tasks")
print(f"  - 5 MCQ questions")
print(f"  - 3 Theory questions")
print(f"Module is DRAFT — publish from admin panel when ready")
db.close()
