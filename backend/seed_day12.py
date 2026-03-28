"""
Seed script: Day 12 — Web Hosting, WHM, cPanel & WHMCS
Run once: python3 seed_day12.py
"""
import sys
sys.path.insert(0, ".")
from database import SessionLocal, engine
import models

db = SessionLocal()

# Create the module
module = models.Module(
    title="Day 12 — Web Hosting, WHM, cPanel & WHMCS",
    description="Covers web hosting fundamentals, WHM server management, cPanel account administration, and WHMCS billing/automation.",
    sort_order=12,
    is_published=False,
    time_limit=90,
    resources=[
        {"title": "cPanel Documentation", "url": "https://docs.cpanel.net/"},
        {"title": "WHM Documentation", "url": "https://docs.cpanel.net/whm/"},
        {"title": "WHMCS Documentation", "url": "https://docs.whmcs.com/"},
    ],
)
db.add(module)
db.flush()

questions = [
    # ─── MCQ Questions (1-15) ─────────────────────────────────────────────────

    # WHM
    {
        "type": "mcq",
        "text": "What is the default port used to access WHM?",
        "options": ["80", "443", "2086/2087", "8080"],
        "correct_answer": "2",
        "points": 1.0,
        "order": 1,
        "hint": "WHM uses a non-standard port pair for HTTP/HTTPS access.",
    },
    {
        "type": "mcq",
        "text": "In WHM, which feature is used to create a new cPanel account for a customer?",
        "options": ["Account Functions > Create Account", "DNS Functions > Add Zone", "Server Configuration > New User", "Packages > Create Package"],
        "correct_answer": "0",
        "points": 1.0,
        "order": 2,
        "hint": "Look under the Account Functions section.",
    },
    {
        "type": "mcq",
        "text": "What does EasyApache do in WHM?",
        "options": ["Manages DNS zones", "Configures Apache, PHP, and related modules", "Creates cPanel accounts", "Manages SSL certificates"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 3,
        "hint": "It's the tool for customizing the web server stack.",
    },
    {
        "type": "mcq",
        "text": "Which service does WHM use for email delivery?",
        "options": ["Postfix", "Exim", "Sendmail", "Dovecot"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 4,
        "hint": "cPanel/WHM has traditionally used this MTA since its early days.",
    },
    {
        "type": "mcq",
        "text": "What is the purpose of the 'Tweak Settings' page in WHM?",
        "options": ["Manage DNS records", "Configure server-wide settings for Apache, PHP, mail, etc.", "Create hosting packages", "Monitor server resource usage"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 5,
        "hint": "It's the central place for server-wide configuration options.",
    },

    # cPanel
    {
        "type": "mcq",
        "text": "What is the default port used to access cPanel?",
        "options": ["80", "2082/2083", "8443", "3000"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 6,
        "hint": "cPanel uses its own dedicated port pair.",
    },
    {
        "type": "mcq",
        "text": "In cPanel, which tool is used to manage MySQL databases?",
        "options": ["File Manager", "phpMyAdmin", "Terminal", "Softaculous"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 7,
        "hint": "It's a web-based database administration tool.",
    },
    {
        "type": "mcq",
        "text": "Which cPanel feature allows you to set up automatic website backups?",
        "options": ["Cron Jobs + Backup Wizard", "File Manager", "Zone Editor", "MultiPHP Manager"],
        "correct_answer": "0",
        "points": 1.0,
        "order": 8,
        "hint": "You can schedule tasks and use the built-in backup feature.",
    },
    {
        "type": "mcq",
        "text": "What is an Addon Domain in cPanel?",
        "options": ["A domain alias that points to the main domain", "A fully functional additional domain hosted on the same account", "A subdomain of the primary domain", "A parked domain for SEO"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 9,
        "hint": "It has its own document root and can host a separate website.",
    },
    {
        "type": "mcq",
        "text": "Which cPanel section allows you to manage SSL/TLS certificates?",
        "options": ["Security > SSL/TLS", "Domains > Zone Editor", "Files > File Manager", "Software > Softaculous"],
        "correct_answer": "0",
        "points": 1.0,
        "order": 10,
        "hint": "Look under the Security section.",
    },

    # WHMCS
    {
        "type": "mcq",
        "text": "What is WHMCS primarily used for?",
        "options": ["Server monitoring", "Web hosting billing, automation, and client management", "Email marketing", "Content delivery"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 11,
        "hint": "It stands for Web Host Manager Complete Solution.",
    },
    {
        "type": "mcq",
        "text": "In WHMCS, what is a 'Product/Service' used for?",
        "options": ["Tracking server uptime", "Defining a hosting plan or service that clients can order", "Managing DNS zones", "Creating email accounts"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 12,
        "hint": "Products represent what you sell to clients.",
    },
    {
        "type": "mcq",
        "text": "Which WHMCS module type handles automatic provisioning of hosting accounts?",
        "options": ["Payment Gateway", "Server Module (Provisioning Module)", "Addon Module", "Mail Module"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 13,
        "hint": "This module communicates with WHM/cPanel to create accounts automatically.",
    },
    {
        "type": "mcq",
        "text": "What does the WHMCS cron job do?",
        "options": ["Only sends emails", "Processes invoices, suspensions, renewals, and automation tasks", "Creates backups", "Monitors server resources"],
        "correct_answer": "1",
        "points": 1.0,
        "order": 14,
        "hint": "It's the heartbeat of WHMCS automation.",
    },
    {
        "type": "mcq",
        "text": "In WHMCS, what is the difference between 'Active' and 'Suspended' service status?",
        "options": [
            "Active means paid and running; Suspended means overdue and access restricted",
            "Active means the server is up; Suspended means the server is down",
            "There is no difference",
            "Active is for VPS; Suspended is for shared hosting"
        ],
        "correct_answer": "0",
        "points": 1.0,
        "order": 15,
        "hint": "It relates to the client's payment status.",
    },

    # ─── Practical Questions (16-25) ──────────────────────────────────────────

    # WHM practical
    {
        "type": "practical",
        "text": "Create a new cPanel account in WHM with the following details:\n- Domain: testsite.com\n- Username: testuser\n- Password: Test@1234\n- Package: default\n\nUse WHM to create this account.",
        "verify_command": "/usr/local/cpanel/bin/whmapi1 accountsummary user=testuser --output=json | grep -o '\"status\":1'",
        "verify_expected": '"status":1',
        "verify_type": "contains",
        "points": 2.0,
        "order": 16,
        "hint": "Go to WHM > Account Functions > Create a New Account.",
    },
    {
        "type": "practical",
        "text": "Using WHM, change the PHP version for the account 'testuser' to PHP 8.2. You can use MultiPHP Manager in WHM.",
        "verify_command": "/usr/local/cpanel/bin/whmapi1 php_get_vhost_versions --output=json | grep -o 'ea-php82'",
        "verify_expected": "ea-php82",
        "verify_type": "contains",
        "points": 2.0,
        "order": 17,
        "hint": "Go to WHM > Software > MultiPHP Manager, select the domain, and change the PHP version.",
    },
    {
        "type": "practical",
        "text": "Install a free Let's Encrypt SSL certificate for testsite.com using WHM AutoSSL. Navigate to WHM > SSL/TLS > Manage AutoSSL and run AutoSSL for the testuser account.",
        "verify_command": "/usr/local/cpanel/bin/whmapi1 get_autossl_check_schedule --output=json | grep -o 'enabled'",
        "verify_expected": "enabled",
        "verify_type": "contains",
        "points": 2.0,
        "order": 18,
        "hint": "WHM > SSL/TLS > Manage AutoSSL. Select the provider and run for the account.",
    },
    {
        "type": "practical",
        "text": "Create a hosting package in WHM with the following limits:\n- Package Name: starter_plan\n- Disk Quota: 2048 MB\n- Bandwidth: 50000 MB\n- Max Addon Domains: 3\n- Max Email Accounts: 10",
        "verify_command": "/usr/local/cpanel/bin/whmapi1 getpkg pkg=starter_plan --output=json | grep -o 'starter_plan'",
        "verify_expected": "starter_plan",
        "verify_type": "contains",
        "points": 2.0,
        "order": 19,
        "hint": "Go to WHM > Packages > Add a Package.",
    },
    {
        "type": "practical",
        "text": "Suspend the cPanel account 'testuser' from WHM with the reason 'Payment overdue'. Then verify the account is suspended.",
        "verify_command": "/usr/local/cpanel/bin/whmapi1 accountsummary user=testuser --output=json | grep -o 'suspended'",
        "verify_expected": "suspended",
        "verify_type": "contains",
        "points": 2.0,
        "order": 20,
        "hint": "Go to WHM > Account Functions > Suspend/Unsuspend Account.",
    },

    # cPanel practical
    {
        "type": "practical",
        "text": "Log into cPanel as testuser and create a MySQL database named 'testuser_wpdb' and a database user 'testuser_wpuser' with password 'Db@Pass123'. Grant ALL PRIVILEGES to the user on the database.",
        "verify_command": "/usr/local/cpanel/bin/cpapi2 --user=testuser MysqlFE listdbs | grep -o 'testuser_wpdb'",
        "verify_expected": "testuser_wpdb",
        "verify_type": "contains",
        "points": 2.0,
        "order": 21,
        "hint": "In cPanel, go to Databases > MySQL Databases. Create the DB, then the user, then assign privileges.",
    },
    {
        "type": "practical",
        "text": "Using cPanel File Manager for testuser, create an index.html file in the public_html directory with the content: '<h1>Welcome to TestSite</h1>'",
        "verify_command": "cat /home/testuser/public_html/index.html | grep -o 'Welcome to TestSite'",
        "verify_expected": "Welcome to TestSite",
        "verify_type": "contains",
        "points": 2.0,
        "order": 22,
        "hint": "Open cPanel > File Manager > public_html, create a new file named index.html.",
    },
    {
        "type": "practical",
        "text": "Set up an email account support@testsite.com in cPanel with a mailbox quota of 500 MB.",
        "verify_command": "/usr/local/cpanel/bin/cpapi2 --user=testuser Email listpops | grep -o 'support@testsite.com'",
        "verify_expected": "support@testsite.com",
        "verify_type": "contains",
        "points": 2.0,
        "order": 23,
        "hint": "Go to cPanel > Email > Email Accounts > Create.",
    },
    {
        "type": "practical",
        "text": "Create a cron job in cPanel for testuser that runs every day at midnight (0 0 * * *) and executes the command: /usr/bin/php /home/testuser/public_html/cron.php",
        "verify_command": "crontab -l -u testuser 2>/dev/null | grep -o 'cron.php'",
        "verify_expected": "cron.php",
        "verify_type": "contains",
        "points": 2.0,
        "order": 24,
        "hint": "Go to cPanel > Advanced > Cron Jobs.",
    },
    {
        "type": "practical",
        "text": "Using WHM, unsuspend the account 'testuser' so it is active again.",
        "verify_command": "/usr/local/cpanel/bin/whmapi1 accountsummary user=testuser --output=json | grep -c 'suspendreason'",
        "verify_expected": "0",
        "verify_type": "contains",
        "points": 1.0,
        "order": 25,
        "hint": "Go to WHM > Account Functions > Unsuspend Account.",
    },

    # ─── Short Answer / Theory Questions (26-40) ──────────────────────────────

    {
        "type": "short_answer",
        "text": "Explain the difference between Shared Hosting, VPS Hosting, and Dedicated Server hosting. When would you recommend each type?",
        "correct_answer": "Shared hosting: multiple sites share one server's resources, cheapest, suitable for small/low-traffic sites. VPS: virtualized private server with dedicated resources, good for growing sites needing more control. Dedicated server: entire physical server for one client, maximum performance and control, for high-traffic or resource-intensive applications.",
        "points": 2.0,
        "order": 26,
        "hint": "Think about resource allocation, cost, and use cases.",
    },
    {
        "type": "short_answer",
        "text": "What is the role of WHM (Web Host Manager) in a web hosting environment? How does it relate to cPanel?",
        "correct_answer": "WHM is the server-level administration panel used by hosting providers/resellers to manage the server, create cPanel accounts, configure server settings, manage packages, DNS, and security. cPanel is the account-level control panel given to individual customers to manage their hosting (files, databases, email, domains). WHM creates and manages cPanel accounts.",
        "points": 2.0,
        "order": 27,
        "hint": "Think about the hierarchy: server admin vs. individual account management.",
    },
    {
        "type": "short_answer",
        "text": "What is a hosting package in WHM? What parameters can you configure in a hosting package?",
        "correct_answer": "A hosting package is a predefined set of resource limits and features assigned to cPanel accounts. Parameters include: disk space quota, bandwidth/data transfer limit, max addon domains, max subdomains, max parked domains, max email accounts, max databases, max FTP accounts, shell access, CGI access, and dedicated IP.",
        "points": 1.5,
        "order": 28,
        "hint": "Think about the resource limits you'd set for different hosting plans.",
    },
    {
        "type": "short_answer",
        "text": "What is DNS propagation and why does it take time when you change nameservers or DNS records?",
        "correct_answer": "DNS propagation is the process by which updated DNS information spreads across all DNS servers worldwide. It takes time (up to 24-48 hours) because DNS records are cached by ISPs and DNS resolvers based on the TTL (Time To Live) value. Each resolver keeps the old cached record until the TTL expires, then fetches the updated record.",
        "points": 1.5,
        "order": 29,
        "hint": "Think about caching and TTL values.",
    },
    {
        "type": "short_answer",
        "text": "Explain the difference between an A record, CNAME record, MX record, and TXT record in DNS.",
        "correct_answer": "A record: maps a domain to an IPv4 address. CNAME: creates an alias pointing one domain to another domain name. MX record: specifies the mail server responsible for receiving emails for the domain. TXT record: holds text information, commonly used for SPF, DKIM, DMARC email authentication and domain verification.",
        "points": 2.0,
        "order": 30,
        "hint": "Each record type serves a different purpose in DNS.",
    },
    {
        "type": "short_answer",
        "text": "What is WHMCS and what are its core functions in a web hosting business?",
        "correct_answer": "WHMCS (Web Host Manager Complete Solution) is a billing and automation platform for web hosting companies. Core functions: automated billing and invoicing, client management, hosting account provisioning/suspension, domain registration, support ticket system, payment gateway integration, product/service management, and automated renewal/expiry handling.",
        "points": 2.0,
        "order": 31,
        "hint": "Think about the business side of running a hosting company.",
    },
    {
        "type": "short_answer",
        "text": "A client reports their website is showing a '500 Internal Server Error'. What are the common causes and how would you troubleshoot this in a cPanel environment?",
        "correct_answer": "Common causes: incorrect .htaccess rules, PHP errors, incorrect file/folder permissions (should be 644 for files, 755 for directories), PHP memory limit exceeded, broken PHP scripts, missing PHP modules. Troubleshooting: check Apache error logs (cPanel > Errors or /home/user/logs/error.log), review .htaccess file, check file permissions, check PHP error log, increase PHP memory_limit, try renaming .htaccess to isolate the issue.",
        "points": 2.0,
        "order": 32,
        "hint": "Start with the error logs and common permission issues.",
    },
    {
        "type": "short_answer",
        "text": "What is the difference between a Parked Domain (Alias) and an Addon Domain in cPanel?",
        "correct_answer": "Parked Domain (Alias): points to the same document root as the primary domain, shows the same website content. Used when you own multiple domains and want them all to show the same site. Addon Domain: a fully independent domain with its own document root, can host a completely separate website, essentially another hosting account within the same cPanel account.",
        "points": 1.5,
        "order": 33,
        "hint": "Think about whether each type has its own separate content.",
    },
    {
        "type": "short_answer",
        "text": "Explain what SPF, DKIM, and DMARC are and why they are important for email delivery.",
        "correct_answer": "SPF (Sender Policy Framework): DNS TXT record that specifies which mail servers are authorized to send email for a domain, prevents spoofing. DKIM (DomainKeys Identified Mail): adds a digital signature to outgoing emails, allowing receivers to verify the email wasn't tampered with. DMARC (Domain-based Message Authentication): policy that tells receivers how to handle emails that fail SPF/DKIM checks. Together they prevent email spoofing, improve deliverability, and protect against phishing.",
        "points": 2.0,
        "order": 34,
        "hint": "These are email authentication mechanisms that work together.",
    },
    {
        "type": "short_answer",
        "text": "A client's website is slow. How would you diagnose and resolve performance issues from a hosting/cPanel perspective?",
        "correct_answer": "Diagnosis: check server load/resource usage in WHM (CPU, RAM, disk I/O), check the account's resource usage in cPanel, review Apache access/error logs for excessive requests, check for malware or compromised scripts, verify PHP version and settings. Solutions: enable caching (OPcache), optimize database queries, increase PHP memory_limit, enable Gzip compression, check for heavy cron jobs, consider CloudFlare CDN, upgrade hosting plan if resource limits are hit, check for poorly coded plugins/themes.",
        "points": 2.0,
        "order": 35,
        "hint": "Think about server resources, application optimization, and caching.",
    },
    {
        "type": "short_answer",
        "text": "How does the WHMCS-WHM integration work for automatic provisioning? Describe the flow from a client ordering a hosting plan to the account being created.",
        "correct_answer": "Flow: 1) Client selects a hosting product on the WHMCS order page. 2) Client completes payment via configured payment gateway. 3) WHMCS marks the order as paid and triggers the server module (cPanel/WHM module). 4) The server module sends an API call to WHM with account details (domain, username, package). 5) WHM creates the cPanel account with the specified package limits. 6) WHMCS sends a welcome email to the client with login details. 7) The service status changes to 'Active' in WHMCS.",
        "points": 2.0,
        "order": 36,
        "hint": "Follow the journey from order placement to account creation.",
    },
    {
        "type": "short_answer",
        "text": "What are nameservers and why are they important in web hosting? How would you set up custom/private nameservers for a hosting company?",
        "correct_answer": "Nameservers are DNS servers that translate domain names to IP addresses and store DNS records for domains. They are essential because they tell the internet where to find a website. To set up private nameservers (e.g., ns1.yourdomain.com, ns2.yourdomain.com): 1) Register child nameservers (glue records) at your domain registrar pointing to your server IP. 2) Configure the DNS zone in WHM. 3) Set up the nameserver software (BIND/named) in WHM. This gives a professional, branded appearance for hosting clients.",
        "points": 2.0,
        "order": 37,
        "hint": "Think about what happens when you type a domain in a browser.",
    },
    {
        "type": "short_answer",
        "text": "What backup strategies would you implement for a web hosting server? Explain the difference between full and incremental backups.",
        "correct_answer": "Full backup: complete copy of all data (accounts, configs, databases) — takes more space and time but provides complete restoration capability. Incremental backup: only backs up data that changed since the last backup — faster and uses less space but requires the full backup plus all incrementals to restore. Strategy: daily incremental backups, weekly full backups, retain multiple backup copies, store backups on a remote/external server, test restoration regularly. In WHM: configure backup settings under Backup Configuration, choose backup destination (local, remote FTP/SFTP, S3).",
        "points": 2.0,
        "order": 38,
        "hint": "Think about backup frequency, storage, and restoration.",
    },
    {
        "type": "short_answer",
        "text": "A client reports they cannot send or receive emails. What steps would you take to troubleshoot email issues in a cPanel hosting environment?",
        "correct_answer": "Troubleshooting steps: 1) Check if the email account exists and has correct password. 2) Verify MX records point to the correct mail server. 3) Check disk quota — full mailbox blocks incoming mail. 4) Check Exim mail logs (/var/log/exim_mainlog) for delivery errors. 5) Verify SPF/DKIM records are correct. 6) Check if server IP is blacklisted (use MXToolbox). 7) Verify email client settings (IMAP/SMTP ports, SSL/TLS). 8) Check if the server firewall is blocking mail ports (25, 465, 587, 993). 9) Test sending from webmail to isolate client-side issues.",
        "points": 2.0,
        "order": 39,
        "hint": "Follow a systematic approach from DNS to server to client configuration.",
    },
    {
        "type": "short_answer",
        "text": "What is CloudLinux and how does it benefit a shared hosting environment? What are LVE limits?",
        "correct_answer": "CloudLinux is a Linux distribution designed for shared hosting that isolates each cPanel account into a lightweight virtualized environment (CageFS). Benefits: prevents one account from consuming all server resources, improves stability and security, provides per-user resource limits. LVE (Lightweight Virtual Environment) limits include: CPU speed, CPU cores, RAM (physical memory), I/O throughput, IOPS, entry processes (concurrent connections), and number of processes. Admins can set these limits per account or per package in WHM using the CloudLinux LVE Manager.",
        "points": 2.0,
        "order": 40,
        "hint": "Think about resource isolation in a multi-tenant hosting environment.",
    },
]

for q_data in questions:
    q = models.Question(
        module_id=module.id,
        type=q_data["type"],
        text=q_data["text"],
        options=q_data.get("options"),
        correct_answer=q_data.get("correct_answer"),
        verify_command=q_data.get("verify_command"),
        verify_expected=q_data.get("verify_expected"),
        verify_type=q_data.get("verify_type"),
        points=q_data["points"],
        order=q_data["order"],
        hint=q_data.get("hint"),
    )
    db.add(q)

db.commit()
print(f"Created module: {module.title} (ID: {module.id})")
print(f"Created {len(questions)} questions (15 MCQ + 10 Practical + 15 Theory)")
print("Module is set to DRAFT — publish it from admin panel when ready.")
db.close()
