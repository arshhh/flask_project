import json
from flask import Flask, redirect, url_for, session
from app.instance.config import *
from app import app
from flask_oauth import OAuth
from app.routes import routes
oauth = OAuth()

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'json'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/googleauth', methods=['GET','POST'])
def googleauth():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('googlelogin'))

    access_token = access_token[0]
    from urllib.request import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)

    except URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('googlelogin'))
        return res.read()


    dict_google = json.loads(res.read().decode('utf-8'))
    if dict_google['verified_email']:
        session['username']= dict_google['given_name']
        return redirect(url_for('home_page'))
    return dict_google

@app.route('/googlelogin')
def googlelogin():
    callback=url_for('authorized', _external=True)
    return google.authorize(callback=callback)



@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('googleauth'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


# def main():
#     app.run()
#
#
# if __name__ == '__main__':
#     main()
