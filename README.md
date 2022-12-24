# backend-mvp
The backend project for deinplugin

# Docker setup for local development

- Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install)
- Copy `localdev/docker-compose.overrides.yml` to `docker-compose.overrides.yml`
- Extract `localdev/local-certs.zip` into the main project folder (Make sure that the certs end up in the certs directory)
- Run `docker-compose up --build`
- Run `docker-compose exec webserver bash` in a separate terminal to open a shell in the container
- Run `cd /var/www/deinplugin/`
- Run `python manage.py createsuperuser` to create a local admin user
- Exit the shell using `exit`
- The admin console should now be available at `https://localhost:5097/admin/`
- Stop the containers again using Ctrl+C in the first terminal

To start the conatiners in detached mode:
- `docker-compose up -d` (with `--build`, if modules have changed since last run)

To stop the containers:
- `docker-compose down`

To show the logs of the containers:
- `docker-compose logs`
