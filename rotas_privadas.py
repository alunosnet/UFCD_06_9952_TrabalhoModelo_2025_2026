from flask import Flask, render_template, request
import animais, utilizadores
"""
Rotas para funcionalidades em que é necessário autenticação
"""
#Define as rotas em que é necessário estar autenticado
def configurar(app):
    @app.route("/aadmin")
    def area_admin():
        return render_template("aadmin.html")
    
    @app.route("/acliente")
    def area_cliente():
        return render_template("acliente.html")
    
    @app.route("/animal/adicionar",methods=["GET","POST"])
    def animal_adicionar():
        return animais.Adicionar(app)
    
    @app.route("/animal/listar")
    def animal_listar():
        return animais.Listar(app)
    
    @app.route("/animal/detalhes")
    def animal_detalhes():
        id = request.args.get("id")
        return animais.Detalhes(id)
    
    @app.route("/utilizador/adicionar",methods=["GET","POST"])
    def utilizador_adicionar():
        return utilizadores.Adicionar()
    
    @app.route("/utilizador/listar")
    def utilizador_listar():
        return utilizadores.Listar()