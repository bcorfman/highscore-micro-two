from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from core.db import HighScore

app = FastAPI()
starlette_config = Config('env.txt')
app.add_middleware(SessionMiddleware,
                   secret_key=starlette_config.get('SECRET_KEY'))
oauth = OAuth(starlette_config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(name='google',
               server_metadata_url=CONF_URL,
               client_kwargs={'scope': 'openid email profile'})


@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        name = user.get('name')
        return HTMLResponse(f'<p>Hello {name}!</p><a href=/logout>Logout</a>')
    return HTMLResponse('<a href=/login>Login</a>')


@app.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@app.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@app.get("/highscores")
async def get_high_scores():
    highscore = HighScore()
    highscore.setup_db()


@app.put("/addscore")
async def add_score_to_list(initials: str, score: int):
    """ Add a new score with initials to a list of high scores,
    sort the list in descending order, and keep only the top 10
    scores in the database.
    Inputs:
    - initials: a string representing the initials of the player who achieved the score.
    - score: an integer representing the score achieved by the player. """
    d = deta.Deta(starlette_config.get('DETA_SPACE_DATA_KEY'))
    db = d.Base('FastAPI_data')
    if len(initials) > 0 and score >= 0:
        items = db.fetch().items
        high_scores = []
        if items:
            for item in items.pop()['score_list']:
                high_scores.append((item[1], item[0]))
        high_scores.append((score, initials[:3].upper()))
        high_scores.sort(reverse=True)
        db.put(
            {"score_list": [(item[1], item[0]) for item in high_scores[:10]]},
            "score_list")
    return db.fetch().items


@app.put("/clear")
async def clear_high_score_list():
    d = deta.Deta(starlette_config.get('DETA_SPACE_DATA_KEY'))
    db = d.Base('FastAPI_data')
    for item in db.fetch().items:
        db.delete(item['key'])
    return db.fetch().items