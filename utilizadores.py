from flask import Flask, render_template, redirect, request
import basedados
import requests, bcrypt
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
            #TODO: Continuar aqui!!!!!!!!!!!!!!!!!!!!!!!
        else:
            return render_template("Utilizadores/login.html",mensagem="O login falhou. Tente novamente.")