"""
Script de Seed (População) para o Banco de Dados.
Localização: src/tests/seed_moradores.py
"""
import os
import sys
import random
import string
from dotenv import load_dotenv

# --- TRUQUE DE PATH ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)
# ----------------------

from src.db.repository import EstacionamentoRepository
from src.classes.Morador import Morador

dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

def gerar_placa():
    letras = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
    numeros = "".join(random.choices("0123456789", k=4))
    return f"{letras}-{numeros}"

def gerar_nome_valido():
    """Gera um nome apenas com letras (ex: Morador Teste ABC)"""
    sufixo = "".join(random.choices(string.ascii_uppercase, k=3))
    return f"Morador Teste {sufixo}"

def main():
    print("🌱 Iniciando o Seed de Moradores...")
    
    # Configuração do Banco
    db_filename = os.getenv("DB_FILENAME", "estacionamento.db")
    db_path = os.path.join(project_root, "src", "db", db_filename)
    repo = EstacionamentoRepository(db_path)

    # Configuração do Prédio
    andares = [1, 2, 3, 4, 5] 
    aptos_por_andar = 5       

    total_criados = 0

    try:
        with repo:
            for andar in andares:
                for final in range(aptos_por_andar): 
                    apto_numero = f"{andar}{final}"
                    
                    if int(apto_numero) > 50: 
                       break

                    # CORREÇÃO 1: Nome apenas com letras
                    nome_ficticio = gerar_nome_valido()
                    placa_ficticia = gerar_placa()
                    
                    # Lógica de Vaga com Texto (Apto-1)
                    vaga_automatica = f"{apto_numero}-1"

                    try:
                        novo_morador = Morador(
                            nome=nome_ficticio,
                            placa=placa_ficticia,
                            cnh="12345678900",
                            modelo="Carro Teste",
                            cor="Prata",
                            apartamento=apto_numero,
                            vaga_id=vaga_automatica
                        )

                        repo.adicionar_morador(novo_morador)
                        print(f"✅ Criado: {nome_ficticio} | Apto: {apto_numero} | Vaga: {vaga_automatica}")
                        total_criados += 1
                    
                    except Exception as e:
                        if "UNIQUE constraint failed" in str(e):
                            print(f"⚠️  Duplicidade ignorada para {apto_numero}.")
                        else:
                            print(f"❌ Erro no {apto_numero}: {e}")

    except Exception as e:
        print(f"❌ Erro geral: {e}")

    print(f"\n🏁 Concluído! {total_criados} moradores inseridos.")

if __name__ == "__main__":
    main()