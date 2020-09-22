# Python sample app

This is a sample application showing integration with FusionAuth and OAuth/OIDC.

This is based on the [5 minute setup guide](https://fusionauth.io/docs/v1/tech/5-minute-setup-guide) but using python3 instead of JavaScript.

## Prerequisites

* FusionAuth
* python3
* pip3

## Installation

* `python3 -m venv venv`
* `. venv/bin/activate`
* `pip3 install -r requirements.txt`
* Create an application in FusionAuth
  * Set the redirect url to `http://localhost:5000/oauth-callback`
  * Note the client id and client secret
  * Register a user for this application
* Create an API key in FusionAuth
* Update `app/views.py` with the values gathered above (look for the `#UPDATE ME` section)

## Running

`python3 run.py`

Visit `http://localhost:5000`

# Contributors

* Nishant Trivedi did the initial implementation. 

