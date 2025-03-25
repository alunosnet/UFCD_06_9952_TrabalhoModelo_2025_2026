"""
Módulo para consultas
"""
import basedados, utilizadores
from flask import Flask, request, redirect, render_template, session
import datetime

#Função para listar todas as consultas se é admin ou só as consultas do cliente
def Listar():
    ligacao_bd = basedados.criar_conexao("vetonline.bd")
    if utilizadores.Utilizador_Admin():
        sql = "SELECT * From Consultas ORDER BY data_consulta, hora_consulta"
        dados = basedados.consultar_sql(ligacao_bd,sql)
    else:
        email = session["email"]
        sql = "SELECT * From Consultas WHERE email=? ORDER BY data_consulta, hora_consulta"
        parametros = (email,)
        dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("Consultas/listar.html",dados=dados)

#Função para marcar uma consulta para admin e para cliente (solicitada)
# [solicitada,confirmada,cancelada,realizada]
def Marcar():
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    if request.method=="GET":
        if utilizadores.Utilizador_Admin():
            sql = "SELECT * FROM Utilizadores WHERE perfil<>'bloqueado' ORDER BY Nome"
            dados = basedados.consultar_sql(ligacao_bd,sql)
            dados2 = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Animais")
        else:
            email=session["email"]
            sql = "SELECT * FROM Utilizadores WHERE perfil<>'bloqueado' and email=? ORDER BY Nome"
            parametros=(email,)
            dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
            sql = "SELECT * FROM Animais WHERE email=?"
            dados2=basedados.consultar_sql(ligacao_bd,sql,parametros)
        return render_template("Consultas/marcar.html",utilizadores=dados,animais=dados2)
    if request.method=="POST":
        estado = "Solicitada"
        email = session["email"]
        if utilizadores.Utilizador_Admin():
            estado = "Confirmada"
            email = request.form.get("email")
        #id do animal
        id = request.form.get("id")
        data_marcacao = datetime.datetime.now()
        #converter a data numa string
        data_marcacao = data_marcacao.strftime("%Y-%m-%d")
        data_consulta = request.form.get("data_consulta")
        hora_consulta = request.form.get("hora_consulta")
        medico = request.form.get("medico")
        razao = request.form.get("razao")
        resumo ="Preencher no dia da consulta"
        #inserir na base de dados
        sql = "INSERT INTO Consultas(email,id,data_marcacao,data_consulta,hora_consulta,estado, medico, razao, resumo) VALUES (?,?,?,?,?,?,?,?,?)"
        parametros = (email,id,data_marcacao,data_consulta,hora_consulta,estado,medico,razao, resumo)
        print(parametros)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        return redirect("/consulta/listar")

#Função para alterar o estado das consultas (admin)
def Estado():
    nr_consulta = request.form.get("nr_consulta")
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    sql = "SELECT estado FROM Consultas WHERE nr_consulta = ?"
    parametros=(nr_consulta,)
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    #Solicitada","Confirmada","Cancelada","Realizada"
    if dados[0][0]=="Solicitada":
        estado = "Confirmada"
    elif dados[0][0]=="Confirmada":
        estado = "Cancelada"
    elif dados[0][0]=="Cancelada":
        estado = "Realizada"
    else:
        estado = "Solicitada"
    sql = "UPDATE Consultas SET estado = ? WHERE nr_consulta = ?"
    parametros=(estado,nr_consulta)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/consulta/listar")

#Função devolve a lista das consultas do dia (admin)
def ListarConsultasDia():
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    data_hoje = datetime.datetime.now()
    data_hoje = data_hoje.strftime("%Y-%m-%d")     #converter no formato ano-mês-dia
    sql="SELECT * FROM Consultas WHERE data_consulta=?"
    parametros=(data_hoje,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return dados

#Recebe o nr da consulta e mostra o formulário resumo.html para ser preenchido
def Resumo():
    nr_consulta = request.form.get("nr_consulta")
    return render_template("consultas/resumo.html",nr_consulta=nr_consulta)

#Recebe o nr consulta e o resumo inserido para guardar na bd
def Resumo_Preenchido():
    nr_consulta = request.form.get("nr_consulta")
    resumo = request.form.get("resumo")
    ligacao_bd=basedados.criar_conexao("vetonline.bd")
    sql="UPDATE Consultas SET resumo = ? WHERE nr_consulta = ?"
    parametros = (resumo, nr_consulta)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/consulta/listar")