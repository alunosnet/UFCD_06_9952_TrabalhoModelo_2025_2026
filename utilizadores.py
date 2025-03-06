from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import basedados
import random 
import requests, bcrypt
from flask_mail import Mail, Message
"""
Módulos utilizadores
"""
#chaves do recaptcha
RECAPTCHA_SITE_KEY='6LcSBtYqAAAAAMwMq-7EAhJ9SumdXnt7n5oj2ypd'
RECAPTCHA_SECRET_KEY ='6LcSBtYqAAAAAJNrHfsFTKZ3Xih2kmI61qPEvFqa'

#função para registar utilizadores
def registar():
    if request.method=="GET":
        return render_template("Utilizadores/registar.html",site_key=RECAPTCHA_SITE_KEY)
    if request.method=="POST":
        #testar recaptcha
        resposta = request.form["g-recaptcha-response"]
        payload={'response':resposta, 'secret':RECAPTCHA_SECRET_KEY}

        pedido = requests.post("https://www.google.com/recaptcha/api/siteverify",data=payload)
        pedido = pedido.json()
        if pedido["success"]==False:
            mensagem="Tem de provar que não é um robot."
            return render_template("Utilizadores/registar.html",site_key=RECAPTCHA_SITE_KEY,mensagem=mensagem)
        
        #ligação bd
        ligacao_bd=basedados.criar_conexao("vetonline.bd")
        #validação dos dados
        nome = request.form.get("nome")
        email = request.form.get("email")
        ppasse=request.form.get("ppasse")
        #inserir na bd
        ppasse = ppasse.encode('utf-8')
        sal = bcrypt.gensalt()
        ppasse_hash = bcrypt.hashpw(ppasse,sal)
        sql="INSERT INTO Utilizadores(nome,email,passe,perfil) VALUES (?,?,?,'cliente')"
        parametros=(nome,email,ppasse_hash)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        #redirecionar para /login
        return redirect("/login")
    
#iniciar sessão de utilizador
def login():
    if request.method=="GET":
        return render_template("Utilizadores/login.html")
    if request.method=="POST":
        email = request.form.get("email")
        ppasse = request.form.get("ppasse")
        #ligação a bd
        ligacao_bd=basedados.criar_conexao("vetonline.bd")
        #consulta a bd email
        sql="SELECT * FROM Utilizadores WHERE email=?"
        parametros=(email,)
        dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
        if not dados or len(dados)<1:
            return render_template("Utilizadores/login.html",mensagem="O login falhou. Tente novamente.")
        #verificar a password hash
        passe_bd = dados[0]['passe']
        if bcrypt.checkpw(ppasse.encode('utf-8'),passe_bd):
            #verificar o estado da conta
            if dados[0]['perfil']=="bloqueado":
                return render_template("Utilizadores/login.html",mensagem="A sua conta de utilizador está bloqueada.")
            #iniciar sessão (email, perfil, nome)
            session['email']=email
            session['perfil']=dados[0]['perfil']
            print(session['perfil'])
            session["nome"]=dados[0]['nome']
            if session['perfil'] == 'admin':
                return redirect("/aadmin")
            return redirect("/acliente")
        else:
            return render_template("Utilizadores/login.html",mensagem="O login falhou. Tente novamente.")

def recuperarpassword(mail):
    #1º passo (não existe o token)
    token = request.args.get("token",None)
    if token is None and request.method=="GET":
        #gerar o token
        email=request.args.get("email")
        token = GerarToken(email)
        #enviar email
        assunto="Recuperação de palavra passe"
        texto=f"""
            Clique no link para definir uma palavra passe nova <a href='http://127.0.0.1:5000/recuperar_password?token={token}'>Clique aqui</a><br>Se não foi solicitada nenhuma recuperação da palavra passe ignore este email.<br>Vetonline
        """
        mensagem = Message(assunto,sender="alunosnet@gmail.com",recipients=[email])
        mensagem.body = texto
        mensagem.html = texto
        mail.send(mensagem)
        #mostrar mensagem ao utilizador
        return render_template("Utilizadores/login.html",mensagem="Foi enviado um email para recuperação da sua palavra passe")
    #2º passo

def GerarToken(email):
    token = random.randint(100000,999999)   #UUID
    ligacao_bd = basedados.criar_conexao("vetonline.bd")
    sql="UPDATE Utilizadores SET token_recuperacao=? WHERE email=?"
    parametros=(token,email)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return str(token)