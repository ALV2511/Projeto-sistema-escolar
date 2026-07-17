from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

NOME_ARQUIVO = "sistema_alunos.xlsx"

# Modelo de dados para o cadastro de alunos
class Aluno(BaseModel):
    nome: str
    nota1: float
    nota2: float

# Garante que o arquivo Excel exista ao iniciar o servidor
def inicializar():
    if not os.path.exists(NOME_ARQUIVO):
        colunas = ["ID", "Nome", "Média", "Status"]
        df = pd.DataFrame(columns=colunas)
        df.to_excel(NOME_ARQUIVO, index=False)

inicializar()

# --- ROTAS DA API ---

@app.get("/api/alunos")
def listar_alunos():
    df = pd.read_excel(NOME_ARQUIVO)
    # Transforma as linhas do Excel em uma lista de dicionários para o JS ler
    return df.to_dict(orient="records")

@app.post("/api/alunos")
def cadastrar_aluno(aluno: Aluno):
    df = pd.read_excel(NOME_ARQUIVO)
    
    media = (aluno.nota1 + aluno.nota2) / 2
    status = "Aprovado" if media >= 7 else "Reprovado"
    
    novo_id = int(df["ID"].max()) + 1 if not df.empty else 1
    
    nova_linha = {
        "ID": novo_id,
        "Nome": aluno.nome,
        "Média": media,
        "Status": status
    }
    
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    df.to_excel(NOME_ARQUIVO, index=False)
    return {"status": "success", "mensagem": "Aluno cadastrado com sucesso!"}

@app.delete("/api/alunos/{id_aluno}")
def excluir_aluno(id_aluno: int):
    df = pd.read_excel(NOME_ARQUIVO)
    
    if id_aluno not in df["ID"].values:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
    df = df[df["ID"] != id_aluno]
    df.to_excel(NOME_ARQUIVO, index=False)
    return {"status": "success", "mensagem": "Aluno excluído com sucesso!"}

# --- SERVIR O FRONTEND ---

# Monta a pasta de arquivos estáticos (CSS e JS)
app.mount("/static", StaticFiles(directory="templates"), name="static")

# Rota principal que entrega o arquivo HTML para o navegador
@app.get("/")
def index():
    return FileResponse("templates/index.html")