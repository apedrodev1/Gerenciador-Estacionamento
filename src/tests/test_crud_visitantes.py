"""
Script de Teste de Fluxo de Visitante.
Ciclo: Entrada (Alocar Vaga) -> Verificação -> Saída (Liberar Vaga).
Localização: src/tests/test_fluxo_visitante.py
"""
import os
import sys
from dotenv import load_dotenv

# --- SETUP DE CAMINHO ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)
# ------------------------

from src.db.repository import EstacionamentoRepository
from src.classes.Visitante import Visitante
from src.classes.Estacionamento import Estacionamento

load_dotenv(os.path.join(project_root, '.env'))

def banner(texto):
    print(f"\n{'='*40}")
    print(f"🧪 {texto}")
    print(f"{'='*40}")

def main():
    db_path = os.path.join(project_root, "src", "db", os.getenv("DB_FILENAME", "estacionamento.db"))
    repo = EstacionamentoRepository(db_path)
    
    cap = int(os.getenv("TOTAL_CAPACITY", 20))
    estacionamento = Estacionamento(capacidade_visitantes=cap)

    # Dados de Teste
    placa_vis = "VIS7777"
    nome_vis = "Visitante Rapido"

    with repo:
        try:
            # Limpeza
            antigo = repo.buscar_visitante_por_placa(placa_vis)
            if antigo:
                repo.registrar_saida(antigo.id)

            # --- 1. ENTRADA ---
            banner("PASSO 1: ENTRADA (Visitante Chegando)")
            
            # Achar Vaga
            ocupadas = repo.buscar_vagas_ocupadas_visitantes()
            vaga_livre = estacionamento.alocar_vaga_visitante(ocupadas)
            
            if not vaga_livre:
                print("❌ Estacionamento lotado. Teste abortado.")
                return
            
            print(f"🎫 Ticket gerado para a vaga: {vaga_livre}")

            novo_visitante = Visitante(
                nome=nome_vis,
                placa=placa_vis,
                cnh="22222222222",
                modelo="Uber",
                cor="Preto",
                numero_vaga=vaga_livre
            )
            
            repo.registrar_entrada(novo_visitante)
            print(f"✅ Visitante {placa_vis} entrou.")

            # --- 2. VERIFICAÇÃO ---
            banner("PASSO 2: VERIFICAÇÃO (Patrulha)")
            
            # Verifica se a vaga consta como ocupada
            ocupadas_agora = repo.buscar_vagas_ocupadas_visitantes()
            if vaga_livre in ocupadas_agora:
                print(f"✅ A vaga {vaga_livre} consta como OCUPADA no sistema.")
            else:
                print(f"❌ Erro: A vaga {vaga_livre} deveria estar ocupada!")
                return
            
            # Busca o visitante pelo banco
            vis_banco = repo.buscar_visitante_por_placa(placa_vis)
            if vis_banco:
                print(f"✅ Dados conferidos: {vis_banco.nome} está na vaga {vis_banco.numero_vaga}.")
            else:
                print("❌ Erro: Visitante não encontrado no banco.")

            # --- 3. SAÍDA ---
            banner("PASSO 3: SAÍDA (Liberando Vaga)")
            
            repo.registrar_saida(vis_banco.id)
            print(f"👋 Visitante {placa_vis} registrou saída.")

            # Verifica se liberou a vaga
            ocupadas_final = repo.buscar_vagas_ocupadas_visitantes()
            if vaga_livre not in ocupadas_final:
                print(f"✅ A vaga {vaga_livre} está LIVRE novamente.")
            else:
                print(f"❌ Erro: A vaga {vaga_livre} ainda consta como ocupada!")
                return

            banner("🏁 RESULTADO FINAL")
            print("🎉 Fluxo de Visitante (Entrada -> Ocupação -> Saída -> Liberação) OK!")

        except Exception as e:
            print(f"❌ EXCEÇÃO: {e}")

if __name__ == "__main__":
    main()