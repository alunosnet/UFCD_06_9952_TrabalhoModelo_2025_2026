"""
Criar a base de dados, criar as tabelas, criar um admin
"""
import basedados
import bcrypt

#criar a base de dados
ligacao_bd=basedados.criar_conexao("vetonline.bd")

ativar_integridade_referencial = "PRAGMA foreign_keys=ON"
basedados.executar_sql(ligacao_bd,ativar_integridade_referencial)

#Criar a tabela dos utilizadores
#Utilizadores(email<PK>,passe,perfil [cliente,admin,bloqueado],nome,morada,cp,telefone,token_recuperacao,data_recuperacao)
sql = """
CREATE TABLE IF NOT EXISTS Utilizadores(
    email TEXT PRIMARY KEY check (email like '%@%.%'),
    passe TEXT NOT NULL,
    perfil TEXT NOT NULL,
    nome TEXT check (length(nome)>3),
    morada TEXT,
    cp TEXT,
    telefone TEXT,
    token_recuperacao TEXT,
    data_recuperacao NUMERIC
)
"""
basedados.executar_sql(ligacao_bd,sql)

#verificar se existe um admin
sql = "SELECT count(*) as contar FROM Utilizadores WHERE perfil='admin'"
dados = basedados.consultar_sql(ligacao_bd,sql)
# testar se existe um utilizador com perfil admin
if not dados or len(dados)<1 or dados[0]["contar"]==0:
    email="admin@gmail.com"
    nome = "admin"
    passe = "12345"
    #hash passe
    sal = bcrypt.gensalt()
    passe = passe.encode('utf-8')
    hash_passe = bcrypt.hashpw(passe,sal)
    sql ="""INSERT INTO Utilizadores(nome,email,passe,perfil) VALUES (?,?,?,'admin')"""
    parametros=(nome,email,hash_passe)
    basedados.executar_sql(ligacao_bd,sql,parametros)
#criar tabela dos animais
#Animais(id<pk>,nome, especie,raca,ano_nascimento,genero,peso,altura,chip,data_vacina,email<FK>)
sql = """
CREATE TABLE IF NOT EXISTS Animais(
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL,
    raca TEXT,
    ano_nascimento INTEGER check (ano_nascimento > 1970),
    genero TEXT,
    peso NUMERIC check (peso>0),
    altura NUMERIC check (altura>0),
    chip TEXT,
    data_vacina NUMERIC,
    email TEXT References Utilizadores(email)
)
"""
basedados.executar_sql(ligacao_bd,sql)
#criar a tabela das consultas
#Consultas(nr_consulta<pk>,email<FK>,id<FK>,data_marcacao,data_consulta,hora_consulta,estado [solicitada,confirmada,cancelada,realizada],medico,razao,resumo)
sql="""
CREATE TABLE IF NOT EXISTS Consultas(
    nr_consulta INTEGER PRIMARY KEY,
    email TEXT NOT NULL References Utilizadores(email),
    id INTEGER NOT NULL References Animais(id),
    data_marcacao NUMERIC NOT NULL,
    data_consulta NUMERIC NOT NULL,
    hora_consulta NUMERIC NOT NULL,
    estado TEXT NOT NULL CHECK (estado in ("Solicitada","Confirmada","Cancelada","Realizada")),
    medico TEXT,
    razao TEXT NOT NULL,
    resumo TEXT
)
"""
basedados.executar_sql(ligacao_bd,sql)
