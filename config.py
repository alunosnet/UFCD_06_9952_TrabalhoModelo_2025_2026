import os
from flask_session import Session
"""
Configurações de emails, pasta dos uploads, recaptcha
"""
#configuração das pasta de uploads
def config_uploads(app):
    #configurar a pasta para fotos dos animais
    UPLOAD_FOLDER = os.path.join(app.root_path,"static/imagens")
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

#configuração dos cookies de sessão
def config_sessoes(app):
    app.config["SESSION_TYPE"]="filesystem"
    app.config["SESSION_PERMANENT"]=False
    Session(app)

#configuração email (Mailtrap.io)
def config_email(app):
    app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'e1c112fb3d14ca'
    app.config['MAIL_PASSWORD'] = '5056ec04bda81d'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False