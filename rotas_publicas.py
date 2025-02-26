from flask import render_template
import utilizadores
"""
Rotas para funcionalidades sem autenticação
"""
#Define as rotas em que não é necessário autenticação
def configurar(app,mail):
    #raiz do site
    @app.route('/')
    def index():
        #TODO: adicionar dados estatisticos (nº de pets por raça)
        return render_template("index.html")
    #aceitar cookies
    #registar
    @app.route('/registar',methods=["GET","POST"])
    def registar():
        return utilizadores.registar()
    
    #login
    @app.route('/login',methods=["GET","POST"])
    def login():
        return utilizadores.login()
    #logout
    #recuperar password