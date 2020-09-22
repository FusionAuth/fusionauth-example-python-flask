import os
import json

from app import app
from flask import request, render_template, send_from_directory

from fusionauth.fusionauth_client import FusionAuthClient


api_key = ""
client_id = ""
client_secret = ""
host_ip = ""

client = FusionAuthClient(api_key, "http://{}:9011".format(host_ip))


@app.route("/")
def index():
    # resp = client.retrieve_user_by_email('test@showfloor.co')
    login_uri = "http://{}:9011/oauth2/authorize?client_id={}&response_type=code&redirect_uri=http%3A%2F%2F{}%3A5000%2Foauth-callback".format(
        host_ip, client_id, host_ip
    )
    register_uri = "http://{}:9011/oauth2/register?client_id={}&response_type=code&redirect_uri=http%3A%2F%2F{}%3A5000%2Foauth-callback".format(
        host_ip, client_id, host_ip
    )
    return render_template("public/index.html", login_uri=login_uri, register_uri=register_uri)

@app.route("/oauth-callback")
def oauth_callback():
    tok_resp = client.exchange_o_auth_code_for_access_token(
        request.args.get("code"),
        client_id,
        "http://{}:5000/oauth-callback".format(host_ip),
        client_secret,
    )
    if not tok_resp.was_successful():
        print("Failed to get token! Error: {}".format(tok_resp.error_response))
        uri = "http://{}:5000/".format(host_ip)
        return render_template(
            "public/error.html",
            uri=uri,
            msg="Failed to get auth token.",
            reason=tok_resp.error_response["error_reason"],
            description=tok_resp.error_response["error_description"],
        )

    user_resp = client.retrieve_user_using_jwt(tok_resp.success_response["access_token"])
    if not user_resp.was_successful():
        print("Failed to get user info! Error: {}".format(user_resp.error_response))
        uri = "http://{}:5000/".format(host_ip)
        return render_template(
            "public/error.html",
            uri=uri,
            msg="Failed to get user info.",
            reason=tok_resp.error_response["error_reason"],
            description=tok_resp.error_response["error_description"],
        )
    print(user_resp.success_response)
    uri = "http://{}:9011/oauth2/logout?client_id={}".format(host_ip, client_id)
    return render_template(
        "public/logged_in.html",
        uri=uri,
        user_id=user_resp.success_response["user"]["id"],
        email=user_resp.success_response["user"]["email"],
        created_at=user_resp.success_response["user"]["insertInstant"],
        updated_at=user_resp.success_response["user"]["lastUpdateInstant"],
        last_login=user_resp.success_response["user"]["lastLoginInstant"],
        pwd_updated_at=user_resp.success_response["user"]["passwordLastUpdateInstant"],
        pwd_change=user_resp.success_response["user"]["passwordChangeRequired"]
    )

@app.route("/logout")
def logout():
    uri = "http://{}:5000/".format(host_ip)
    return render_template("public/logged_out.html", uri=uri)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "app/static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )

