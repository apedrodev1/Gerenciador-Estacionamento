"""
Ponto de entrada principal para o Sistema de Gestão de Estacionamento.
"""

import os
from dotenv import load_dotenv # 1. Importar biblioteca

# 2. Carregar as variáveis do arquivo .env para a memória
load_dotenv()

from src.db.repository import EstacionamentoRepository
from src.classes.Estacionamento import Estacionamento

# Importando as funções de interface (Menus)
from src.functions.moradores.catraca_moradores.entrada_morador import registrar_entrada_morador
from src.functions.moradores.catraca_moradores.saida_morador import registrar_saida_morador
from src.functions.moradores.gerenciar_moradores import menu_gerenciar_moradores
from src.functions.visitantes.registrar_entrada import registrar_entrada_visitante
from src.functions.visitantes.registrar_saida import registrar_saida_visitante
from src.functions.visitantes.listar_visitantes import listar_visitantes_ativos
from src.functions.UI.exibir_mapa import exibir_mapa_estacionamento
from src.utils.input_handler import get_valid_input, clear_screen
from src.utils.validations import validate_yes_no

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # 1. Configuração do Banco de Dados via .env
    # Pegamos apenas o nome do arquivo do .env e montamos o caminho
    db_filename = os.getenv("DB_FILENAME", "estacionamento.db") 
    db_path = os.path.join("src", "db", db_filename)
    
    try:
        repo = EstacionamentoRepository(db_path)
    except Exception as e:
        print(f"❌ Erro crítico ao conectar ao banco de dados: {e}")
        return

    # 2. Inicializa a Lógica via .env
    # ATENÇÃO: É obrigatório converter para int() pois o .env retorna string
    try:
        capacidade = int(os.getenv("TOTAL_CAPACITY", 50))
        tempo_limite = int(os.getenv("TIME_LIMIT_MINUTES", 120))
        nome_estacionamento = os.getenv("PARKING_NAME", "Estacionamento Genérico")
    except ValueError:
        print("❌ Erro no arquivo .env: Capacidade e Tempo devem ser números inteiros.")
        return

    estacionamento = Estacionamento(
        nome=nome_estacionamento, 
        capacidade_total=capacidade, 
        tempo_limite_minutos=tempo_limite
    )

    # 3. Loop Principal
    with repo:
        while True:
            clear_screen()

            total_visitantes = repo.contar_visitantes_ativos()
            estacionamento.ocupacao_atual = total_visitantes 

            # --- DISPLAY DO STATUS ---
            print("\n" + "="*40)
            print(f"🏢 {estacionamento.nome} - PAINEL DE CONTROLE")
            print(f"📊 Lotação Visitantes: {estacionamento.ocupacao_atual}/{estacionamento.capacidade_total}")
            
            if estacionamento.esta_lotado:
                print("🚨 STATUS: LOTADO (Entrada Bloqueada)")
            else:
                print(f"✅ Vagas Livres: {estacionamento.vagas_disponiveis}")
            print("="*40)

            # --- MENU ---
            print("\n--- 🚗 VISITANTES ---")
            print("1. 📥 Registrar Entrada")
            print("2. 📤 Registrar Saída")
            print("3. 📋 Listar (Verificar Vencidos)")
            
            print("\n--- 🏡 MORADORES ---")
            print("4. 📥 Registrar Entrada")  
            print("5. 📤 Registrar Saída")    
            print("6. 🏘️  Gerenciar Cadastro") 
            
            print("\n--- ⚙️  SISTEMA ---")
            print("7. 🗺️  Mapa Geral (Ocupação)") 
            print("0. ❌ Sair")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == '1':
                registrar_entrada_visitante(estacionamento, repo)
            elif opcao == '2':
                registrar_saida_visitante(estacionamento, repo)
            elif opcao == '3':
                listar_visitantes_ativos(estacionamento, repo)
            elif opcao == '4':
                registrar_entrada_morador(repo)
            elif opcao == '5':
                registrar_saida_morador(repo)
            elif opcao == '6':
                menu_gerenciar_moradores(repo, estacionamento)
            elif opcao == '7':
                exibir_mapa_estacionamento(repo)
            
            elif opcao == '0':
                print("\n👋 Sistema encerrado. Até logo!")
                break
            
            else:
                print("❌ Opção inválida.")
    
            input("\nPressione Enter para voltar...")

if __name__ == "__main__":
    main()