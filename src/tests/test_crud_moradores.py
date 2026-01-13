"""
Script de Teste de Integração (CRUD Completo).
Testa o ciclo de vida: Criar -> Ler -> Atualizar -> Deletar.
Localização: src/tests/test_crud_completo.py
"""
import os
import sys
import time
from dotenv import load_dotenv

# --- SETUP DE CAMINHO ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.append(project_root)
# ------------------------

from src.db.repository import EstacionamentoRepository
from src.classes.Morador import Morador

# Carrega .env
load_dotenv(os.path.join(project_root, '.env'))

def banner(texto):
    print(f"\n{'='*40}")
    print(f"🧪 {texto}")
    print(f"{'='*40}")

def main():
    # 1. Conexão
    db_path = os.path.join(project_root, "src", "db", os.getenv("DB_FILENAME", "estacionamento.db"))
    repo = EstacionamentoRepository(db_path)
    
    # --- DADOS DE TESTE CORRIGIDOS ---
    # Placa: "TST9999" (SEM HÍFEN, pois o Banco salva sem hífen!)
    placa_teste = "TST9999"
    
    # Nome: Sem pontuação
    nome_original = "Senhor Teste Crud"
    nome_alterado = "Senhor Teste Atualizado"
    
    # Vaga/Apto
    vaga_original = "99-1"
    vaga_alterada = "99-2"
    apto_teste = "99"

    with repo:
        try:
            # --- PASSO 1: CREATE (Criação) ---
            banner("PASSO 1: CREATE (Criando Morador)")
            
            # Limpeza preventiva
            morador_velho = repo.buscar_morador_por_placa(placa_teste)
            if morador_velho:
                repo.remover_morador(morador_velho.id)
                print("🧹 Limpeza de teste anterior realizada.")

            novo_morador = Morador(
                nome=nome_original,
                placa=placa_teste, # Aqui a classe aceitaria com hífen, mas vamos mandar limpo
                cnh="99999999900",     
                modelo="Delorean",
                cor="Cinza",
                apartamento=apto_teste,
                vaga_id=vaga_original
            )
            
            repo.adicionar_morador(novo_morador)
            print("✅ Comando de Adicionar enviado com sucesso.")


            # --- PASSO 2: READ (Leitura e Verificação) ---
            banner("PASSO 2: READ (Verificando no Banco)")
            
            # AGORA VAI FUNCIONAR: Buscamos pela placa SEM HÍFEN
            morador_recuperado = repo.buscar_morador_por_placa(placa_teste)
            
            if morador_recuperado:
                print(f"🔎 Encontrado: ID {morador_recuperado.id} | Nome: {morador_recuperado.nome}")
                
                # Validação dos dados
                if morador_recuperado.nome.lower() == nome_original.lower() and morador_recuperado.vaga_id == vaga_original:
                    print("✅ Dados conferem com o original!")
                else:
                    print(f"❌ DADOS INCORRETOS! Esperado: {nome_original}/{vaga_original} - Veio: {morador_recuperado.nome}/{morador_recuperado.vaga_id}")
                    return 
            else:
                print(f"❌ ERRO CRÍTICO: Morador com placa {placa_teste} não foi encontrado!")
                # Dica de Debug
                print("DICA: Verifique se o banco salvou a placa com ou sem hífen.")
                return


            # --- PASSO 3: UPDATE (Atualização) ---
            banner("PASSO 3: UPDATE (Alterando Dados)")
            
            # Modificamos o objeto recuperado
            morador_recuperado.nome = nome_alterado
            morador_recuperado.vaga_id = vaga_alterada
            
            # Mandamos salvar
            repo.atualizar_morador(morador_recuperado)
            print(f"🔄 Solicitada troca para: {nome_alterado} na vaga {vaga_alterada}")
            
            # Buscamos NOVAMENTE
            morador_atualizado = repo.buscar_morador_por_placa(placa_teste)
            
            if morador_atualizado.nome.lower() == nome_alterado.lower() and morador_atualizado.vaga_id == vaga_alterada:
                 print("✅ Sucesso! O banco de dados retornou os dados novos.")
            else:
                 print(f"❌ FALHA NO UPDATE. O banco retornou: {morador_atualizado.nome} | Vaga: {morador_atualizado.vaga_id}")
                 return


            # --- PASSO 4: DELETE (Remoção) ---
            banner("PASSO 4: DELETE (Removendo)")
            
            repo.remover_morador(morador_recuperado.id)
            print(f"🗑️ Solicitada remoção do ID {morador_recuperado.id}")
            
            # Tenta buscar de novo. Deve vir None.
            morador_fantasma = repo.buscar_morador_por_placa(placa_teste)
            
            if not morador_fantasma:
                print("✅ Sucesso! O registro desapareceu do banco.")
            else:
                print("❌ FALHA NO DELETE. O morador ainda está lá!")
                return

            banner("🏁 RESULTADO FINAL")
            print("🎉 PARABÉNS! O Sistema passou em todos os testes de CRUD.")

        except Exception as e:
            print(f"❌ EXCEÇÃO NÃO TRATADA: {e}")

if __name__ == "__main__":
    main()