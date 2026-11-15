
from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path

#not used2
app = Flask(__name__)

# Arquivo onde os dados serão armazenados
ARQUIVO_DADOS = Path("tarefas.json")


def carregar_dados():
    if ARQUIVO_DADOS.exists():
        return json.loads(ARQUIVO_DADOS.read_text(encoding="utf-8"))

    return {
        "tarefas": [],
        "anotacoes": ""
    }


def salvar_dados(dados):
    ARQUIVO_DADOS.write_text(
        json.dumps(dados, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )


# Página principal
@app.route("/")
def home():
    return render_template("index.html")


# Consultar tarefas e anotações
@app.route("/dados")
def obter_dados():
    return jsonify(carregar_dados())


# Adicionar tarefa
@app.route("/tarefas", methods=["POST"])
def adicionar_tarefa():
    dados = carregar_dados()
    tarefa = request.json.get("tarefa", "").strip()

    if not tarefa:
        return jsonify({"erro": "Digite uma tarefa"}), 400

    nova_tarefa = {
        "id": max(
            [t["id"] for t in dados["tarefas"]],
            default=0
        ) + 1,
        "descricao": tarefa,
        "concluida": False
    }

    dados["tarefas"].append(nova_tarefa)
    salvar_dados(dados)

    return jsonify(nova_tarefa)


# Alterar status da tarefa
@app.route("/tarefas/<int:id>", methods=["PATCH"])
def atualizar_tarefa(id):
    dados = carregar_dados()

    for tarefa in dados["tarefas"]:
        if tarefa["id"] == id:
            tarefa["concluida"] = not tarefa["concluida"]
            salvar_dados(dados)
            return jsonify(tarefa)

    return jsonify({"erro": "Tarefa não encontrada"}), 404


# Excluir tarefa
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def excluir_tarefa(id):
    dados = carregar_dados()

    dados["tarefas"] = [
        t for t in dados["tarefas"]
        if t["id"] != id
    ]

    salvar_dados(dados)

    return jsonify({"sucesso": True})


# Salvar anotações
@app.route("/anotacoes", methods=["POST"])
def salvar_anotacoes():
    dados = carregar_dados()
    dados["anotacoes"] = request.json.get("texto", "")

    salvar_dados(dados)

    return jsonify({"sucesso": True})


if __name__ == "__main__":
    app.run(debug=True)
