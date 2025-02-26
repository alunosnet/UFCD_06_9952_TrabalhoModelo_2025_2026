from flask import Flask, render_template, request, redirect, session, make_response, jsonify
from flask_mail import Mail
import tabelas
import config, rotas_privadas, rotas_publicas

app = Flask(__name__)

#configuração de uploads, sessões e emails
config.config_uploads(app)
config.config_sessoes(app)
config.config_email(app)
mail=Mail(app)

#rotas
rotas_publicas.configurar(app,mail)
rotas_privadas.configurar(app)
#TODO: rotas dos erros

if __name__=='__main__':
    app.run(debug=True)