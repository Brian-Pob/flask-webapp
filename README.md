# COP4521


## Commands 

Activate virtual environment: `. ./venv/bin/activate`

Install requirements: `python3 -m pip install -r requirements.txt`

Gunicorn: `gunicorn --workers 3 --bind 0.0.0.0:8000 helloworld:app`

## Project Notes

The production application is running on Digital Ocean. For development, we
should be running local instances of the server on other machines. This could
be our bare metal machines or on other VMs. These dev machines should have
the same or similar setups to the production machine. That means setting up
Ubuntu 22.04, python3, pip, pipenv, gunicorn, nginx, etc.

