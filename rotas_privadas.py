from flask import Flask, render_template, request, redirect
import animais, utilizadores
"""
Rotas para funcionalidades em que é necessário autenticação
"""
import consultas
#Define as rotas em que é necessário estar autenticado
def configurar(app):
    @app.route("/aadmin")
    def area_admin():
        if utilizadores.Utilizador_Admin()==False:
            return redirect("/")
        dados = consultas.ListarConsultasDia()

        return render_template("aadmin.html",dados = dados)
    
    @app.route("/acliente")
    def area_cliente():
        if utilizadores.SessaoIniciada()==False:
            return redirect("/")
        return render_template("acliente.html")
    
    @app.route("/animal/adicionar",methods=["GET","POST"])
    def animal_adicionar():
        if utilizadores.SessaoIniciada()==False:
            return redirect("/")
        return animais.Adicionar(app)
    
    @app.route("/animal/listar")
    def animal_listar():
        if utilizadores.SessaoIniciada()==False:
            return redirect("/")
        return animais.Listar(app)
    
    @app.route("/animal/detalhes")
    def animal_detalhes():
        if utilizadores.SessaoIniciada()==False:
            return redirect("/")
        id = request.args.get("id")
        return animais.Detalhes(id)
    
    @app.route("/utilizador/adicionar",methods=["GET","POST"])
    def utilizador_adicionar():
        if utilizadores.Utilizador_Admin()==False:
            return redirect("/")
        return utilizadores.Adicionar()
    
    @app.route("/utilizador/listar")
    def utilizador_listar():
        if utilizadores.Utilizador_Admin()==False:
            return redirect("/")
        return utilizadores.Listar()
    
    @app.route("/utilizador/bloquear",methods=["POST"])
    def utilizador_bloquear():
        if utilizadores.Utilizador_Admin()==False:
            return redirect("/")
        return utilizadores.Bloquear()
    
    @app.route("/consulta/adicionar",methods=["GET","POST"])
    def consulta_adicionar():
        if utilizadores.SessaoIniciada()==False:
            return redirect("/")
        return consultas.Marcar()
    
    @app.route("/consulta/listar",methods=["GET"])
    def consulta_listar():
        if utilizadores.SessaoIniciada()==False:
            return redirect("/")
        return consultas.Listar()
    
    @app.route("/consulta/estado",methods=["POST"])
    def consulta_estado():
        if utilizadores.Utilizador_Admin()==False:
            return redirect("/")
        return consultas.Estado()
    
    @app.route("/consulta/resumo",methods=["POST"])
    def consulta_resumo():
        if utilizadores.Utilizador_Admin()==False:
            return redirect("/")
        return consultas.Resumo()
    
    @app.route("/consulta/resumo_preenchido",methods=["POST"])
    def consulta_resumo_preenchido():
        if utilizadores.Utilizador_Admin()==False:
            return redirect("/")
        return consultas.Resumo_Preenchido()
    