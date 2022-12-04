cd /var/www/deinplugin
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
chmod 664 /var/www/deinplugin/db.sqlite3
chmod 775 /var/www/deinplugin
chown :www-data /var/www/deinplugin/db.sqlite3
chown :www-data /var/www/deinplugin
apache2ctl -D FOREGROUND
