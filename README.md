# COP4521

## Authors

Brian Poblete - bap21k

Jayen Lare - jsl19b

Group 9

## Project Notes

The production application is running on Digital Ocean. For development, we
should be running local instances of the server on other machines. This could
be our bare metal machines or on other VMs. These dev machines should have
the same or similar setups to the production machine. That means setting up
Ubuntu 22.04, python3, pip, pipenv, gunicorn, nginx, etc.

## Extra Credit

We will attempt to implement automatic CI/CD with Pulumi.

## Commands 

For local development without nginx: `pipenv run gunilocal`
With nginx (background): `pipenv run guni`
With nginx (foreground + debug mode): `pipenv run gunidebug`

For database

```
flask db stamp head
flask db migrate
flask db upgrade
```

## What does "curl news.brian.pob.me" do?

The Linux command line tool *curl* stands for "Client URL", and is used enable data transfers over various network protocols. It is able to communicate with a server by specifying a URL and the data that is to be sent or recieved. *curl* is commonly used for debugging, error logging, endpoint testing, and downloading files from the internet. It can be used directly on the command line or in a script, by using the following syntax:
```
curl [options/URLs]
```
For our project we were able to utilize the *curl* command, along with Wireshark to better understand the communication involved in accessing our server. We first executed the command: 
```
curl news.brianpob.me
```
This allowed us to build the flowchart shown below using Wireshark. The flowchart describes the protocols of communications being used, and what IP ports are being used.

*** INSERT FLOWCHART HERE ***


1. curl news.brianpob.me

2. 

## Project Security

## References

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date


