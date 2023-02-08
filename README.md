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

### Note as of Feb. 8, 2023

I am writing this post-project submission. The class is over and we have shut down our DigitalOcean server. I have also deleted the Auth0 application that the secret keys in our `.env` file are linked to. 

We realized later on in the projet that we should not be storing our API keys and other important information in the same repo of the project. (Better to make the mistake in a college class than in a real job!)

However, if you scroll through our commit history, you will find the `.env` file with our keys. As I said earlier, the Auth0 app with those keys has been deleted so no need to worry about that (I hope).

Anyways, we were given permission to make our repos public. If you are seeing this on GitHub, it was originally on Gitlab. I just moved the repo so that I could have my biggest projects all in one place.

Most things from here on out have been untouched since project submission. Enjoy!

## Extra Credit

~~We will attempt to implement automatic CI/CD with Pulumi.~~

We never ended up doing this sadly :(

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

## Nginx Setup

We have Nginx setup to act as a proxy for our Flask app. When our domain is accessed, Nginx will access the .sock file created by Gunicorn
and serve to the user whatever is being served to the .sock file. We also use Nginx to serve static files. This can be tested
by going to [news.brianpob.me/static/images/stars.jpg](https://news.brianpob.me/static/images/stars.jpg) where we have an image that is being served by Nginx and not Flask.

## What does "curl news.brian.pob.me" do?

The Linux command line tool *curl* stands for "Client URL", and is used to enable data transfers over various network protocols. It is able to communicate with a server by specifying a URL and the data that is to be sent or recieved. *curl* is commonly used for debugging, error logging, endpoint testing, and downloading files from the internet. It can be used directly on the command line or in a script, by implementing the following syntax:
```
curl [options/URLs]
```
For our project we were able to utilize the *curl* command, along with Wireshark to better understand the communication involved in accessing our server. We first executed the command: 
```
curl news.brianpob.me
```
This allowed us to build the flowchart shown below using Wireshark. The flowchart showed us the protocols of communications being used are TCP and HTTP, and the IP ports being used are ports 80 and 50378.


![curl command flowchart](./images/wireshark_graph.png)

## How does Flask object execute Python code?

Below is an example of a basic Flask application
```Python
from flask import Flask    # from the flask package import the Flask class
app = Flask(__name__)      # create an instance of the Flask object called app with __name__
                           # __name__ is passed so the Flask object knows where to look for resources
@app.route('/')            # now we tell Flask what URL should trigger our function
def home():                # we create the function that should be triggered
    return "Hey there!"
if __name__ == '__main__': # if code is run standalone, name is main, execute the Flask app
    app.run(debug=True)    # execute the app
```
[Source 1](https://pythonhow.com/python-tutorial/flask/How-a-Flask-app-works/)

[Source 2](https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application)

## Project Security

We disabled password authentication in SSH so that only keys can be used to login. In the server,
we also setup firewall to block all ports by default except for SSH (port 22) and the ports used
by Nginx (80 and 443). In our Nginx configuration, we also set port 80 HTTP to automatically
redirect to port 443 HTTPS.

We obtained an SSL certificate for our site using LetsEncrypt's Certbot so our site can use HTTPS.

## How we deal with updates

For updates to our code base, we both work on our own virtual machines, and push any updates to our own dev branches. Once updates are working on our individual branch, we create a merge request with the main branch. After reviewing the merge request, the updates are merged into our main branch. Finally, we log into the server and pull the main branch with the updates.

For updates to the server, we implemented unattended-upgrades on Ubuntu following [this guide](https://www.cyberciti.biz/faq/how-to-set-up-automatic-updates-for-ubuntu-linux-18-04/).
In case of a breaking update or any other issue, we have a snapshot of our VM in DigitalOcean and are able to rollback to this snapshot.

We have also set up a GitLab pipeline that will periodically check our domain and see if our server is still up.
When it goes down, the pipeline should alert us. We can then use rollback our VM to the snapshot.

## Server config files

Our config files for setting up the server are located in the `config` folder and are organized in folders by the service or program they configure.

## References

https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-22-04

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

https://stackoverflow.com/questions/17768940/target-database-is-not-up-to-date

https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/#select
