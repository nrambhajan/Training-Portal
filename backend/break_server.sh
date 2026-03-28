#!/bin/bash
# ============================================================
# BREAK SCRIPT — Run on trainee server AFTER they complete
# the LAMP + WordPress setup (Tasks 1-6)
#
# This creates 10 issues for them to troubleshoot.
# Usage: bash break_server.sh
# ============================================================

echo "========================================="
echo " Breaking things for troubleshooting..."
echo "========================================="

# TROUBLE 1: Stop Apache
echo "[1/10] Stopping Apache..."
systemctl stop apache2

# TROUBLE 2: Stop MySQL
echo "[2/10] Stopping MySQL..."
systemctl stop mysql

# TROUBLE 3: Wrong DB password in wp-config
echo "[3/10] Corrupting wp-config.php DB password..."
if [ -f /var/www/html/wp-config.php ]; then
    sed -i "s/define( *'DB_PASSWORD'.*/define( 'DB_PASSWORD', 'wrongpassword' );/" /var/www/html/wp-config.php
fi

# TROUBLE 4: Kill permissions on /var/www/html
echo "[4/10] Breaking file permissions..."
chmod 000 /var/www/html

# TROUBLE 5: Disable PHP module
echo "[5/10] Disabling PHP module..."
a2dismod php* 2>/dev/null

# TROUBLE 6: Fill /tmp with junk files
echo "[6/10] Creating junk files in /tmp..."
dd if=/dev/zero of=/tmp/junk_file1 bs=1M count=100 2>/dev/null
dd if=/dev/zero of=/tmp/junk_file2 bs=1M count=100 2>/dev/null
dd if=/dev/zero of=/tmp/junk_file3 bs=1M count=100 2>/dev/null

# TROUBLE 7: Plant malware file
echo "[7/10] Planting malicious PHP file..."
chmod 755 /var/www/html 2>/dev/null  # temporarily fix to create file
mkdir -p /var/www/html/wp-content/uploads/
echo '<?php eval(base64_decode("cGhwaW5mbygp")); ?>' > /var/www/html/wp-content/uploads/.cache-update.php
chown www-data:www-data /var/www/html/wp-content/uploads/.cache-update.php
chmod 000 /var/www/html  # break permissions again

# TROUBLE 8: Corrupt .htaccess
echo "[8/10] Corrupting .htaccess..."
chmod 755 /var/www/html 2>/dev/null
cat > /var/www/html/.htaccess << 'HTACCESS'
# Corrupted .htaccess
InvalidDirective On
FakeModule Enable
RewriteEngine Broken
HTACCESS
chmod 000 /var/www/html  # break permissions again

# TROUBLE 9: Break DNS resolution
echo "[9/10] Breaking DNS resolution..."
echo "nameserver 192.168.0.1" > /etc/resolv.conf

# TROUBLE 10: Add bad Apache config
echo "[10/10] Adding bad Apache config file..."
cat > /etc/apache2/conf-enabled/bad-config.conf << 'BADCONF'
# This is a broken config file
InvalidDirective On
FakeModule Enable
BADCONF

echo ""
echo "========================================="
echo " Done! 10 issues created."
echo " Trainee must fix them in order."
echo "========================================="
echo ""
echo " Issues created:"
echo "  1. Apache stopped"
echo "  2. MySQL stopped"
echo "  3. wp-config.php has wrong DB password"
echo "  4. /var/www/html permissions set to 000"
echo "  5. PHP Apache module disabled"
echo "  6. /tmp filled with 300MB junk files"
echo "  7. Malware file in wp-content/uploads/"
echo "  8. .htaccess corrupted"
echo "  9. DNS resolution broken (resolv.conf)"
echo " 10. Bad Apache config in conf-enabled/"
echo "========================================="
