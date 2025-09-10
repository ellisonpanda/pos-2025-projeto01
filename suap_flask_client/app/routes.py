from flask import Blueprint, render_template, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from flask import current_app as app

main = Blueprint('main', __name__)

# Configura o OAuth
oauth = OAuth(app)
suap = oauth.register(
    name='suap',
    client_id="fC05RsKBLSFT3vjklMCseenxkEM9gi6VqjdzZJfB",  # teu client_id
    client_secret="9ezz0GGZk0P6umYJlP8Dk85smx0LhNGqxAVbXMKtmsaNssMZPAxS8rWpqrb4jOs80LRhEBEZjRvV2f0qAD2RfO7C5fMRoLKtCYD9EqIB7P3Rvl8HcDXJfQVv2VblwJ7k",  # teu client_secret
    access_token_url="https://suap.ifrn.edu.br/o/token/",
    authorize_url="https://suap.ifrn.edu.br/o/authorize/",
    api_base_url="https://suap.ifrn.edu.br/api/v2/",
    client_kwargs={"scope": "identificacao email documentos"}
)

@main.route('/')
def index():
    user = session.get("user")
    return render_template('index.html', user=user)

@main.route('/login')
def login():
    redirect_uri = url_for("main.authorize", _external=True)
    return suap.authorize_redirect(redirect_uri)

@main.route('/authorize')
def authorize():
    token = suap.authorize_access_token()
    user = suap.get("minhas-informacoes/meus-dados/").json()

    # guarda dados do usuário na sessão
    session["user"] = {
        "nome": user.get("nome_usual"),
        "matricula": user.get("matricula"),
        "email": user.get("email"),
        "foto": user.get("url_foto_75x100")
    }
    return redirect(url_for("main.perfil"))

@main.route('/perfil')
def perfil():
    user = session.get("user")
    if not user:
        return redirect(url_for("main.login"))
    return render_template('perfil.html', user=user)

@main.route('/boletim')
def boletim():
    user = session.get("user")
    if not user:
        return redirect(url_for("main.login"))
    return render_template('boletim.html', user=user)

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("main.index"))
