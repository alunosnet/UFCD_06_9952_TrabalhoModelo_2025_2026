from flask import Flask, render_template
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