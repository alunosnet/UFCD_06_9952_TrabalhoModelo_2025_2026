"""
Módulo para animais
"""
import basedados
from flask import Flask, render_template, request, redirect, session

#Função para adicionar um animal novo
#Pode ser utilizada pelo admin ou pelo cliente
def Adicionar(app):
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    utilizadores = basedados.consultar_sql(ligacao_bd,"SELECT email,nome FROM Utilizadores ORDER BY Nome")
    if request.method=="GET":
        return render_template("Animais/adicionar.html",utilizadores=utilizadores)
    if request.method=="POST":
        #validar dados
        nome = request.form.get("nome")
        especie = request.form.get("especie")
        raca = request.form.get("raca")
        ano = request.form.get("ano")
        ano = int(ano)
        genero = request.form.get("genero")
        peso = request.form.get("peso")
        peso = float(peso)
        altura = request.form.get("altura")
        altura = float(altura)
        chip = request.form.get("chip")
        data_vacina = request.form.get("data_vacina")
        #verificar o perfil do utilizador
        if session["perfil"] == "admin":
            email = request.form.get("dono")
        else:
            email = session["email"]
        #inserir na base de dados o registo
        sql="INSERT INTO Animais(nome,especie,raca,ano_nascimento,genero,peso,altura,chip,data_vacina,email) VALUES (?,?,?,?,?,?,?,?,?,?)"
        parametros=(nome,especie,raca,ano,genero,peso,altura,chip,data_vacina,email)
        id_animal = basedados.executar_sql(ligacao_bd,sql,parametros)
        #guardar a fotografia
        fotografia = request.files["fotografia"]
        nome_fotografia = f"{id_animal}.jpg"
        fotografia.save(app.config["UPLOAD_FOLDER"]+"/"+nome_fotografia)
        #redirecionar para /animal/listar
        return redirect("/animal/listar")

#Função listar animais
#Pode ser utilizada por admin e clientes
def Listar(app):
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    if session['perfil'] == 'admin':
        sql = "SELECT * FROM Animais"
        dados = basedados.consultar_sql(ligacao_bd,sql)
    else:
        email = session['email']
        sql = "SELECT * FROM Animais WHERE email = ?"
        parametros = (email,)
        dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("animais/listar.html",dados=dados)

#recebe o id do animal e mostra todos os campos numa página
def Detalhes(id):
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    #Se não é admin só pode ver o animal se for o dono
    if session["perfil"] != "admin":
        email = session["email"]
        sql = "SELECT * FROM Animais WHERE id=? and email=?"
        parametros=(id,email,)
    else:
        #se é admin pode ver todos os animais
        sql = "SELECT * FROM Animais WHERE id=?"
        parametros=(id,)

    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    if dados != None and len(dados)>0:
        return render_template("animais/detalhes.html",dados=dados[0])
    return redirect("/animal/listar")