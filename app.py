import os
from flask import Flask, jsonify, request
from faker import Factory
from twilio.jwt.access_token import AccessToken, SyncGrant

app = Flask(__name__)
fake = Factory.create()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/token')
def token():
    # get credentials for environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    api_key = os.environ['TWILIO_API_KEY']
    api_secret = os.environ['TWILIO_API_SECRET']
    service_sid = os.environ['TWILIO_SYNC_SERVICE_SID']

    # create a randomly generated username for the client
    identity = fake.user_name()

    # Create a unique endpoint ID for the 
    device_id = request.args.get('device')
    endpoint = "TwilioSyncDemo:{0}:{1}".format(identity, device_id)

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret, identity)

    # Create a Sync grant and add to token
    sync_grant = SyncGrant(endpoint_id=endpoint, service_sid=service_sid)
    token.add_grant(sync_grant)

    # Return token info as JSON
    return jsonify(identity=identity, token=token.to_jwt())

if __name__ == '__main__':
    app.run(debug=True)
