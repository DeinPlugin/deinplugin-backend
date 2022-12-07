/wait
cd /var/www/deinplugin
# python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
apache2ctl -D FOREGROUND
