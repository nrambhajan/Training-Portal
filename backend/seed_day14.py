"""
Day 14 — L1 Support Simulation: Real Ticket Scenarios
Run once: python3 seed_day14.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

module = models.Module(
    title="Day 14 - L1 Support Simulation: Real Ticket Scenarios",
    description="Handle real-world L1 support tickets — DNS, SSL, Email, FTP, Database, Security, and Performance. Mix of setup tasks and break-fix troubleshooting.",
    sort_order=14,
    unlock_percent=0,
    is_published=False,
    time_limit=180,
)
db.add(module)
db.commit()
db.refresh(module)

questions = [
    # ── Phase 1: SETUP TASKS (Build services) ─────────────────────────────

    {
        "type": "practical",
        "text": "SETUP 1 - Install and Configure BIND DNS Server\n\nA client needs a DNS server set up. Install BIND9 DNS server and make sure it is running.\n\nSteps:\n1. sudo apt update && sudo apt install bind9 bind9-utils -y\n2. sudo systemctl enable --now named\n3. Verify: sudo systemctl status named",
        "verify_command": "systemctl is-active named 2>/dev/null || systemctl is-active bind9 2>/dev/null",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 2.0,
        "order": 1,
        "hint": "Install bind9 package and start the named/bind9 service",
    },
    {
        "type": "practical",
        "text": "SETUP 2 - Create a DNS Zone File\n\nCreate a forward zone for 'training.local' that resolves to your server IP.\n\nSteps:\n1. Create zone file: /etc/bind/db.training.local with:\n   $TTL 86400\n   @ IN SOA ns1.training.local. admin.training.local. (\n       2024010101 ; Serial\n       3600       ; Refresh\n       1800       ; Retry\n       604800     ; Expire\n       86400 )    ; Minimum TTL\n   @ IN NS ns1.training.local.\n   ns1 IN A 127.0.0.1\n   www IN A 127.0.0.1\n\n2. Add zone to /etc/bind/named.conf.local:\n   zone \"training.local\" {\n       type master;\n       file \"/etc/bind/db.training.local\";\n   };\n\n3. Check config: sudo named-checkconf\n4. Restart: sudo systemctl restart named",
        "verify_command": "dig @localhost www.training.local +short 2>/dev/null | grep -c '127.0.0.1'",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 2,
        "hint": "Create the zone file in /etc/bind/ and add the zone block to named.conf.local, then restart BIND",
    },
    {
        "type": "practical",
        "text": "SETUP 3 - Install and Configure Postfix Mail Server\n\nSet up a basic Postfix mail server in local-only mode.\n\nSteps:\n1. sudo apt install postfix mailutils -y\n   (Select 'Local only' during setup, or use debconf-set-selections)\n2. sudo systemctl enable --now postfix\n3. Verify: sudo systemctl status postfix",
        "verify_command": "systemctl is-active postfix",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 2.0,
        "order": 3,
        "hint": "sudo DEBIAN_FRONTEND=noninteractive apt install postfix mailutils -y && sudo systemctl enable --now postfix",
    },
    {
        "type": "practical",
        "text": "SETUP 4 - Install and Configure vsftpd FTP Server\n\nSet up an FTP server and create an FTP user.\n\nSteps:\n1. sudo apt install vsftpd -y\n2. sudo systemctl enable --now vsftpd\n3. Create FTP user: sudo useradd -m ftpuser && echo 'ftpuser:FTPpass@123' | sudo chpasswd\n4. Enable local user login in /etc/vsftpd.conf:\n   - Set: local_enable=YES\n   - Set: write_enable=YES\n5. Restart: sudo systemctl restart vsftpd",
        "verify_command": "systemctl is-active vsftpd && id ftpuser >/dev/null 2>&1 && echo 'ftp_ready'",
        "verify_expected": "ftp_ready",
        "verify_type": "contains",
        "points": 2.0,
        "order": 4,
        "hint": "Install vsftpd, create the ftpuser, and make sure write_enable=YES in the config",
    },
    {
        "type": "practical",
        "text": "SETUP 5 - Set Up a Self-Signed SSL Certificate\n\nCreate a self-signed SSL certificate and configure Apache to use HTTPS.\n\nSteps:\n1. Enable SSL module: sudo a2enmod ssl\n2. Generate self-signed cert:\n   sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \\\n     -keyout /etc/ssl/private/server.key \\\n     -out /etc/ssl/certs/server.crt \\\n     -subj '/CN=localhost'\n3. Enable the default SSL site: sudo a2ensite default-ssl\n4. Restart Apache: sudo systemctl restart apache2\n5. Verify: curl -k https://localhost should return HTML",
        "verify_command": "curl -sk https://localhost 2>/dev/null | grep -qi 'html' && echo 'ssl_ok'",
        "verify_expected": "ssl_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 5,
        "hint": "Enable mod_ssl, generate cert with openssl, enable default-ssl site, restart Apache",
    },
    {
        "type": "practical",
        "text": "SETUP 6 - Create a MySQL Backup Script\n\nCreate an automated MySQL backup script that dumps the 'wordpress' database.\n\nSteps:\n1. Create backup directory: sudo mkdir -p /backups/mysql\n2. Create script at /usr/local/bin/db_backup.sh:\n   #!/bin/bash\n   DATE=$(date +%Y%m%d_%H%M%S)\n   mysqldump wordpress > /backups/mysql/wordpress_$DATE.sql\n   echo \"backup_complete\"\n3. Make executable: sudo chmod +x /usr/local/bin/db_backup.sh\n4. Run it once to test: sudo /usr/local/bin/db_backup.sh\n5. Verify backup file exists in /backups/mysql/",
        "verify_command": "test -x /usr/local/bin/db_backup.sh && ls /backups/mysql/wordpress_*.sql 2>/dev/null | wc -l | grep -q '[1-9]' && echo 'backup_ok'",
        "verify_expected": "backup_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 6,
        "hint": "Create the script with mysqldump command, chmod +x, and run it to generate at least one backup",
    },
    {
        "type": "practical",
        "text": "SETUP 7 - Install and Configure CSF Firewall\n\nInstall ConfigServer Security & Firewall (CSF) — the most common firewall in web hosting.\n\nSteps:\n1. Install dependencies: sudo apt install libio-socket-inet6-perl libsocket6-perl libcrypt-ssleay-perl libnet-libidn-perl libio-socket-ssl-perl libgd-graph-perl perl -y\n2. Download CSF:\n   cd /usr/src\n   sudo wget https://download.configserver.com/csf.tgz\n   sudo tar -xzf csf.tgz\n   cd csf\n   sudo sh install.sh\n3. Set TESTING = 0 in /etc/csf/csf.conf to enable CSF\n4. Allow SSH port 22 in TCP_IN and TCP_OUT in /etc/csf/csf.conf\n5. Start CSF: sudo csf -r",
        "verify_command": "csf -v 2>/dev/null | grep -qi 'csf' && grep -q 'TESTING = \"0\"' /etc/csf/csf.conf 2>/dev/null && echo 'csf_ok'",
        "verify_expected": "csf_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 7,
        "hint": "Download CSF from configserver.com, install it, set TESTING=0, and restart with csf -r",
    },
    {
        "type": "practical",
        "text": "SETUP 8 - Set Up Log Rotation for Apache\n\nConfigure custom log rotation for Apache access logs to prevent disk space issues.\n\nSteps:\n1. Create /etc/logrotate.d/apache2-custom with:\n   /var/log/apache2/access.log {\n       daily\n       rotate 7\n       compress\n       delaycompress\n       missingok\n       notifempty\n       create 640 root adm\n       postrotate\n           systemctl reload apache2 > /dev/null 2>&1 || true\n       endscript\n   }\n2. Test it: sudo logrotate -d /etc/logrotate.d/apache2-custom",
        "verify_command": "test -f /etc/logrotate.d/apache2-custom && grep -c 'rotate 7' /etc/logrotate.d/apache2-custom",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 2.0,
        "order": 8,
        "hint": "Create the logrotate config file with daily rotation, 7 rotations kept, and compression",
    },

    # ── Phase 2: TROUBLESHOOTING (Break-fix tickets) ──────────────────────

    {
        "type": "practical",
        "text": "TICKET 1 - Client: 'I can't connect via FTP!'\n\nA client reports FTP connection is refused. The FTP service has been stopped and disabled.\n\nDiagnose and fix the issue so FTP is working again.",
        "verify_command": "systemctl is-active vsftpd",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 3.0,
        "order": 9,
        "hint": "Check if vsftpd service is running. Start and enable it.",
    },
    {
        "type": "practical",
        "text": "TICKET 2 - Client: 'My website shows someone else's page!'\n\nA client reports their website is showing the wrong content. Someone has tampered with the Apache default virtual host and changed the DocumentRoot.\n\nFix the Apache default site config so DocumentRoot points back to /var/www/html/",
        "verify_command": "grep 'DocumentRoot' /etc/apache2/sites-enabled/000-default.conf 2>/dev/null | grep -c '/var/www/html'",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 10,
        "hint": "Check /etc/apache2/sites-enabled/000-default.conf — the DocumentRoot has been changed. Fix it and restart Apache.",
    },
    {
        "type": "practical",
        "text": "TICKET 3 - Client: 'My emails are bouncing!'\n\nA client says all outgoing emails are stuck in the mail queue. The Postfix service has been stopped and the main.cf config has a typo in myhostname.\n\nFix the Postfix config and clear the mail queue.\n\nThe myhostname should be set to the server's actual hostname.",
        "verify_command": "systemctl is-active postfix && postconf myhostname 2>/dev/null | grep -v 'BROKEN' && echo 'mail_ok'",
        "verify_expected": "mail_ok",
        "verify_type": "contains",
        "points": 3.0,
        "order": 11,
        "hint": "Check /etc/postfix/main.cf for typos in myhostname, fix it, start postfix, and flush queue with 'postqueue -f'",
    },
    {
        "type": "practical",
        "text": "TICKET 4 - Client: 'Server is very slow!'\n\nA client reports their server is extremely slow. A rogue process is consuming 100% CPU.\n\nFind and kill the rogue process. (Look for a process called 'stress' or a suspicious script eating CPU.)",
        "verify_command": "pgrep -c 'stress|cpu_eater|crypto_miner' 2>/dev/null || echo '0'",
        "verify_expected": "0",
        "verify_type": "contains",
        "points": 3.0,
        "order": 12,
        "hint": "Use 'top' or 'ps aux --sort=-%cpu' to find the process eating CPU, then kill it with 'kill' or 'killall'",
    },
    {
        "type": "practical",
        "text": "TICKET 5 - Client: 'I see a defacement page on my site!'\n\nA client's WordPress site has been defaced — the index.php was replaced with a hacker's page. The original WordPress index.php has been backed up at /var/www/html/index.php.bak\n\nRestore the original WordPress index.php.",
        "verify_command": "grep -c 'wp-blog-header' /var/www/html/index.php 2>/dev/null",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 3.0,
        "order": 13,
        "hint": "The original index.php was backed up. Restore it: cp /var/www/html/index.php.bak /var/www/html/index.php",
    },
    {
        "type": "practical",
        "text": "TICKET 6 - Client: 'Suspicious cron jobs running!'\n\nA security scan found unauthorized cron jobs running under the www-data user. These cron jobs are downloading and executing malicious scripts.\n\nRemove all cron jobs for the www-data user.",
        "verify_command": "crontab -l -u www-data 2>&1 | grep -cv '^no crontab\\|^$'",
        "verify_expected": "0",
        "verify_type": "contains",
        "points": 3.0,
        "order": 14,
        "hint": "Check cron for www-data: 'crontab -l -u www-data'. Remove with: 'crontab -r -u www-data'",
    },
    {
        "type": "practical",
        "text": "TICKET 7 - Client: 'MySQL crashed and won't start!'\n\nMySQL refuses to start. The MySQL config file has been corrupted with invalid settings.\n\nFix the MySQL configuration and get it running.\n\nTip: Check /etc/mysql/mysql.conf.d/mysqld.cnf for errors.",
        "verify_command": "systemctl is-active mysql",
        "verify_expected": "active",
        "verify_type": "contains",
        "points": 3.0,
        "order": 15,
        "hint": "Check /etc/mysql/mysql.conf.d/mysqld.cnf — look for obviously wrong settings like invalid port or datadir. Fix and restart.",
    },
    {
        "type": "practical",
        "text": "TICKET 8 - Client: 'Apache keeps crashing every few minutes!'\n\nApache restarts but crashes again because a cron job keeps killing it every minute.\n\nFind and remove the malicious cron job that's killing Apache.",
        "verify_command": "! crontab -l 2>/dev/null | grep -q 'apache\\|httpd\\|pkill\\|killall' && systemctl is-active apache2 && echo 'fixed'",
        "verify_expected": "fixed",
        "verify_type": "contains",
        "points": 3.0,
        "order": 16,
        "hint": "Check root's crontab: 'crontab -l'. Remove the entry that's killing Apache. Then start Apache.",
    },
    {
        "type": "practical",
        "text": "TICKET 9 - Client: 'WordPress DB tables are crashed!'\n\nWordPress shows database errors. Some tables in the wordpress database are corrupted.\n\nRepair all WordPress database tables.\n\nSteps:\n1. mysqlcheck -u root --repair wordpress\n2. Verify tables are OK: mysqlcheck -u root wordpress",
        "verify_command": "mysqlcheck -u root wordpress 2>/dev/null | grep -c 'Corrupt'",
        "verify_expected": "0",
        "verify_type": "contains",
        "points": 3.0,
        "order": 17,
        "hint": "Use: mysqlcheck -u root --repair wordpress to repair all tables",
    },
    {
        "type": "practical",
        "text": "TICKET 10 - Client: 'SSH login is very slow!'\n\nSSH takes 30+ seconds to show the password prompt. This is usually caused by DNS reverse lookup.\n\nFix the SSH config to disable DNS lookup and make login instant.\n\nEdit /etc/ssh/sshd_config and set UseDNS to no, then restart SSH.",
        "verify_command": "grep -E '^UseDNS\\s+no' /etc/ssh/sshd_config | grep -c 'no'",
        "verify_expected": "1",
        "verify_type": "contains",
        "points": 2.0,
        "order": 18,
        "hint": "Edit /etc/ssh/sshd_config, add or uncomment 'UseDNS no', then restart sshd",
    },

    # ── Phase 3: MCQ — L1 Knowledge ──────────────────────────────────────

    {
        "type": "mcq",
        "text": "A client says their website shows 'ERR_CONNECTION_REFUSED'. What should you check first?",
        "options": ["DNS records", "Whether the web server is running", "SSL certificate", "Database connection"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 19,
    },
    {
        "type": "mcq",
        "text": "Which DNS record type is used for email routing?",
        "options": ["A record", "CNAME record", "MX record", "TXT record"],
        "correct_answer": "2",
        "points": 1.0,
        "order": 20,
    },
    {
        "type": "mcq",
        "text": "A client's website has a mixed content warning. What does this mean?",
        "options": ["The site has both HTML and PHP files", "The site loads some resources over HTTP instead of HTTPS", "The database has corrupted data", "Multiple users are editing the same file"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 21,
    },
    {
        "type": "mcq",
        "text": "What command shows the current mail queue in Postfix?",
        "options": ["mailq", "postfix queue", "sendmail -q", "mail --queue"],
        "correct_answer": "0",
        "points": 1.0,
        "order": 22,
    },
    {
        "type": "mcq",
        "text": "Which log file would you check first for WordPress 500 errors?",
        "options": ["/var/log/syslog", "/var/log/apache2/error.log", "/var/log/mysql/error.log", "/var/log/auth.log"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 23,
    },

    # ── Phase 4: Theory ──────────────────────────────────────────────────

    {
        "type": "short_answer",
        "text": "A client reports their website is down. Walk through your L1 troubleshooting checklist — what do you check, in what order?",
        "correct_answer": "1. Check if the server is reachable (ping). 2. Check if web server is running (systemctl status apache2/nginx). 3. Check if the port is open (curl, telnet, ss -tlnp). 4. Check DNS resolution (dig/nslookup). 5. Check Apache/Nginx error logs. 6. Check disk space (df -h). 7. Check server load (top, uptime). 8. Check if database is running. 9. Check application logs. 10. Escalate to L2 if unresolved.",
        "points": 3.0,
        "order": 24,
        "hint": "Think systematically: network → service → DNS → logs → resources → database → application",
    },
    {
        "type": "short_answer",
        "text": "Explain the difference between A, AAAA, CNAME, MX, TXT, and NS DNS records. Give an example use case for each.",
        "correct_answer": "A: Maps domain to IPv4 address (example.com → 1.2.3.4). AAAA: Maps domain to IPv6 address. CNAME: Alias pointing to another domain (www.example.com → example.com). MX: Mail exchange, routes email to mail servers (example.com → mail.example.com with priority). TXT: Text records for verification, SPF, DKIM (v=spf1 include:_spf.google.com ~all). NS: Nameserver records, delegates DNS authority (example.com → ns1.provider.com).",
        "points": 3.0,
        "order": 25,
        "hint": "Cover all 6 record types with what they do and a real-world example",
    },
    {
        "type": "short_answer",
        "text": "A client's server was hacked. Describe your incident response steps as an L1 support engineer.",
        "correct_answer": "1. Document the issue (screenshots, timestamps). 2. Check for unauthorized access (last, who, auth.log). 3. Check for suspicious processes (ps aux, top). 4. Check for malicious cron jobs (crontab -l for all users). 5. Check for modified files (find recently changed files). 6. Check for unauthorized SSH keys. 7. Block suspicious IPs (iptables/CSF). 8. Change all passwords. 9. Check for rootkits (rkhunter, chkrootkit). 10. Escalate to L2/security team with findings.",
        "points": 3.0,
        "order": 26,
        "hint": "Think about: documentation, access logs, processes, cron, file integrity, network, passwords, escalation",
    },
]

for q_data in questions:
    q = models.Question(module_id=module.id, **q_data)
    db.add(q)

db.commit()
print(f"Created module '{module.title}' (ID: {module.id}) with {len(questions)} questions")
print(f"  - 8 Setup tasks (DNS, Mail, FTP, SSL, Backup, Firewall, LogRotate)")
print(f"  - 10 Troubleshooting tickets")
print(f"  - 5 MCQ questions")
print(f"  - 3 Theory questions")
print(f"Module is DRAFT — publish from admin panel when ready")
db.close()
