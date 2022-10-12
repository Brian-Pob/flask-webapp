# COP4521


## Commands 

Activate virtual environment: `. ./venv/bin/activate`

Install requirements: `python3 -m pip install -r requirements.txt`

Gunicorn: `gunicorn --workers 3 --bind 0.0.0.0:8000 helloworld:app`

For database

$ flask db stamp head
$ flask db migrate
$ flask db upgrade

## Project Notes

The production application is running on Digital Ocean. For development, we
should be running local instances of the server on other machines. This could
be our bare metal machines or on other VMs. These dev machines should have
the same or similar setups to the production machine. That means setting up
Ubuntu 22.04, python3, pip, pipenv, gunicorn, nginx, etc.

## References

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date


