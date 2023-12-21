**This repo is out of date and is archived. Check out [an updated tutorial on using FusionAuth with Flask](https://fusionauth.io/docs/quickstarts/quickstart-python-flask-web) or [the updated GitHub repository](https://github.com/FusionAuth/fusionauth-quickstart-python-flask-web).**

# Example: Using Python3 with FusionAuth
This project contains an example project that illustrates using FusionAuth with Python3 Flask.

## Prerequisites
You will need the following things properly installed on your computer.

* [Git](http://git-scm.com/): Presumably you already have this on your machine if you are looking at this project locally; if not, use your platform's package manager to install git, and `git clone` this repo.
* [Python3](https://python.org): Python3 can be installed via a variety of methods
* `pip3`: The Python package manager should be installed as part of your Python install, but if not, use your Python install method's mechanism to install this package so that the Python dependencies can be pulled in.
* [Docker](https://www.docker.com): For standing up FusionAuth from within a Docker container. (You can [install it other ways](https://fusionauth.io/docs/v1/tech/installation-guide/), but for this example you'll need Docker.)

## Installation
* `git clone https://github.com/FusionAuth/fusionauth-example-python-flask`
* `cd fusionauth-example-python-flask`
* `docker-compose up` (this will block the current terminal)
* `python3 -m venv venv`
* `. venv/bin/activate`
* `pip3 install -r requirements.txt`


## FusionAuth Configuration
This example assumes that you will run FusionAuth from a Docker container. In the root of this project directory (next to this README) are two files [a Docker compose file](./docker-compose.yml) and an [environment variables configuration file](./.env). Assuming you have Docker installed on your machine, a `docker-compose up` will bring FusionAuth up on your machine.

The FusionAuth configuration files also make use of a unique feature of FusionAuth, called Kickstart: when FusionAuth comes up for the first time, it will look at the [Kickstart file](./kickstart/kickstart.json) and mimic API calls to configure FusionAuth for use. It will perform all the necessary setup to make this demo work correctly, but if you are curious as to what the setup would look like by hand, the "FusionAuth configuration (by hand)" section of this README describes it in detail.

For now, get FusionAuth in Docker up and running (via `docker-compose up`) if it is not already running; to see, [click here](http://localhost:9011/) to verify it is up and running.

> **NOTE**: If you ever want to reset the FusionAuth system, delete the volumes created by docker-compose by executing `docker-compose down -v`. FusionAuth will only apply the Kickstart settings when it is first run (e.g., it has no data configured for it yet).


## Running / Development

* `python3 run.py` (this will block the current terminal)
* [Open a browser](http://localhost:5000) and log in using our user's credentials ("richard@example.com"/"password").

You can also register a new user for this application and will be automatically logged in after.

Log into the [FusionAuth admin screen](http://localhost:9011) with a different browser or incognito window using the admin user credentials ("admin@example.com"/"password") to explore the admin user experience.

# Contributors

* [Nishant Trivedi/nishant009](https://github.com/nishant009) did the initial implementation. 
