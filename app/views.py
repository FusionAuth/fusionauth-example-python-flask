import os
from app import app
from flask import Flask, request, render_template, send_from_directory, session
from fusionauth.fusionauth_client import FusionAuthClient
import pkce

api_key = ""
client_id = ""
client_secret = ""
host_ip = "localhost"

client = FusionAuthClient(api_key, "http://{}:9011".format(host_ip))



@app.route("/")
def index():
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    login_uri = "http://{}:9011/oauth2/authorize?client_id={}&response_type=code&redirect_uri=http%3A%2F%2F{}%3A5000%2Foauth-callback&code_challenge={}&code_challenge_method=S256".format(
        host_ip, client_id, host_ip, code_challenge
    )
    register_uri = "http://{}:9011/oauth2/register?client_id={}&response_type=code&redirect_uri=http%3A%2F%2F{}%3A5000%2Foauth-callback&code_challenge={}&code_challenge_method=S256".format(
        host_ip, client_id, host_ip, code_challenge
    )
    # save the verifier in session to send it later to the token endpoint
    session['code_verifier'] = code_verifier
    return render_template("public/index.html", login_uri=login_uri, register_uri=register_uri)

@app.route("/oauth-callback")
def oauth_callback():
    tok_resp = client.exchange_o_auth_code_for_access_token_using_pkce(
        request.args.get("code"),
        "http://{}:5000/oauth-callback".format(host_ip),
        session['code_verifier'],
        client_id,
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

# app = Flask(__name__)
# app.secret_key = os.urandom(24)
# if __name__ == "__main__":
#     app.secret_key = os.urandom(24)
#     app.run(debug=True)