/wait
cd /var/www/deinplugin
# python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py crontab add
touch /var/www/logs/pluginmeta.log
chmod 777 /var/www/logs/pluginmeta.log
env >> /etc/environment
cron
apache2ctl -D FOREGROUND
