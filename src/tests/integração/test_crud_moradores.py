"""
Script de Teste Completo (CRUD + Fluxo de Catraca via PLACA).
Ciclo: Criar -> Ler -> Atualizar -> ENTRAR (Placa) -> SAIR (Placa) -> Deletar.
Localização: src/tests/test_crud_completo.py
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
from src.classes.Morador import Morador

load_dotenv(os.path.join(project_root, '.env'))

def banner(texto):
    print(f"\n{'='*40}")
    print(f"🧪 {texto}")
    print(f"{'='*40}")

def main():
    db_path = os.path.join(project_root, "src", "db", os.getenv("DB_FILENAME", "estacionamento.db"))
    repo = EstacionamentoRepository(db_path)
    
    # Dados de Teste
    placa_teste = "TST9999" # Placa LIMPA (sem hífen) pois é assim que o banco salva
    nome_original = "Senhor Teste Crud"
    vaga_original = "99-1"
    
    with repo:
        try:
            # Limpeza inicial
            existente = repo.buscar_morador_por_placa(placa_teste)
            if existente:
                repo.remover_morador(existente.id)

            # --- 1. CREATE ---
            banner("PASSO 1: CREATE (Cadastrando)")
            novo_morador = Morador(
                nome=nome_original,
                placa=placa_teste,
                cnh="99999999900",
                modelo="Delorean",
                cor="Prata",
                apartamento="99",
                vaga_id=vaga_original
            )
            repo.adicionar_morador(novo_morador)
            print("✅ Morador cadastrado.")

            # --- 2. READ ---
            morador = repo.buscar_morador_por_placa(placa_teste)
            if not morador:
                print("❌ Erro: Morador não encontrado.")
                return

            # --- 3. UPDATE ---
            banner("PASSO 3: UPDATE (Editando)")
            morador.modelo = "Tesla Cybertruck"
            repo.atualizar_morador(morador)
            print("✅ Modelo atualizado para Cybertruck.")

            # --- 4. ENTRADA (AGORA USANDO PLACA) ---
            banner(f"PASSO 4: CATRACA (Entrada da Placa {placa_teste})")
            
            # Simulação: Câmera leu "TST9999" -> Sistema manda liberar
            repo.registrar_entrada_morador(placa_teste) 
            print("🚙 Cancelas abertas! Comando enviado via Placa.")
            
            # Verificação
            check_entrada = repo.buscar_morador_por_placa(placa_teste)
            if check_entrada.estacionado:
                print("✅ Status confirmado no banco: ESTACIONADO (True).")
            else:
                print("❌ Erro: O banco não registrou a entrada.")
                return

            # --- 5. SAÍDA (AGORA USANDO PLACA) ---
            banner(f"PASSO 5: CATRACA (Saída da Placa {placa_teste})")
            
            repo.registrar_saida_morador(placa_teste)
            print("👋 Comando de saída enviado via Placa.")
            
            check_saida = repo.buscar_morador_por_placa(placa_teste)
            if not check_saida.estacionado:
                print("✅ Status confirmado no banco: AUSENTE (False).")
            else:
                print("❌ Erro: O banco ainda mostra o morador como estacionado.")
                return

            # --- 6. DELETE ---
            banner("PASSO 6: DELETE (Limpando)")
            repo.remover_morador(morador.id) # Para deletar, o ID ainda é mais seguro (interno), mas poderia ser placa
            
            if not repo.buscar_morador_por_placa(placa_teste):
                print("✅ Registro deletado com sucesso.")
            else:
                print("❌ Falha ao deletar.")

            banner("🏁 RESULTADO FINAL")
            print("🎉 Ciclo Completo (Cadastro -> Entrada/Saída via Placa -> Remoção) OK!")

        except Exception as e:
            print(f"❌ EXCEÇÃO: {e}")

if __name__ == "__main__":
    main()