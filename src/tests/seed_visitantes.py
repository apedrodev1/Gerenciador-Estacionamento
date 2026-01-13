"""
Script de Seed (População) para Visitantes.
Preenche metade do estacionamento rotativo para testes.
Localização: src/tests/seed_visitantes.py
"""
import os
import sys
import random
import string
from dotenv import load_dotenv

# --- TRUQUE DE PATH (Igual ao seed_moradores) ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)
# ----------------------

from src.db.repository import EstacionamentoRepository
from src.classes.Visitante import Visitante
from src.classes.Estacionamento import Estacionamento

# Carrega o .env
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

def gerar_placa():
    """Gera placa aleatória (AAA-0000)"""
    letras = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numeros = "".join(random.choices("0123456789", k=4))
    return f"{letras}-{numeros}"

def gerar_nome_visitante():
    """Gera nome válido (apenas letras)"""
    primeiro = "".join(random.choices(string.ascii_uppercase, k=1)) + \
               "".join(random.choices(string.ascii_lowercase, k=4))
    sobrenome = "".join(random.choices(string.ascii_uppercase, k=1)) + \
                "".join(random.choices(string.ascii_lowercase, k=5))
    return f"{primeiro} {sobrenome}"

def main():
    print("🚗 Iniciando o Seed de Visitantes...")

    # 1. Configuração
    db_filename = os.getenv("DB_FILENAME", "estacionamento.db")
    db_path = os.path.join(project_root, "src", "db", db_filename)
    repo = EstacionamentoRepository(db_path)

    # Precisamos da classe Estacionamento para calcular a vaga (V01, V02...)
    capacidade = int(os.getenv("TOTAL_CAPACITY", 20))
    estacionamento = Estacionamento(capacidade_visitantes=capacidade)

    # Meta: Preencher 10 vagas (deixando 10 livres se o total for 20)
    qtd_para_criar = 10
    criados = 0

    with repo:
        for i in range(qtd_para_criar):
            # 1. Busca vagas ocupadas atuais
            ocupadas = repo.buscar_vagas_ocupadas_visitantes()
            
            # 2. O Cérebro calcula a próxima vaga (V01, V02...)
            vaga_livre = estacionamento.alocar_vaga_visitante(ocupadas)

            if not vaga_livre:
                print("🚨 Estacionamento LOTOU durante o seed!")
                break

            # 3. Gera dados
            nome = gerar_nome_visitante()
            placa = gerar_placa()

            # 4. Cria e Salva
            try:
                visitante = Visitante(
                    nome=nome,
                    placa=placa,
                    cnh="11122233300",
                    modelo="Visitante Auto",
                    cor="Branco",
                    numero_vaga=vaga_livre # Aqui entra "V01", "V02"...
                )
                
                repo.registrar_entrada(visitante)
                print(f"✅ Entrada: {vaga_livre} | {nome} | {placa}")
                criados += 1
            except Exception as e:
                print(f"❌ Erro ao inserir {vaga_livre}: {e}")

    print("\n" + "="*30)
    print(f"🏁 Concluído! {criados} visitantes estacionados.")
    print(f"📊 Ocupação estimada: {criados}/{capacidade}")

if __name__ == "__main__":
    main()