"""
Ponto de entrada principal para o Sistema de Gestão de Estacionamento.

Este script inicializa a aplicação, conecta ao banco de dados via Repositório,
hidrata a classe de lógica (Estacionamento) e gerencia o loop principal de interação.
"""

import os
from src.db.repository import EstacionamentoRepository
from src.classes.Estacionamento import Estacionamento

# Importando as funções de interface (Menus)
from src.functions.visitantes.registrar_entrada import registrar_entrada_visitante
from src.functions.visitantes.registrar_saida import registrar_saida_visitante
from src.functions.visitantes.listar_visitantes import listar_visitantes_ativos
from src.functions.moradores.gerenciar_moradores import menu_gerenciar_moradores
from src.functions.UI.exibir_mapa import exibir_mapa_estacionamento

# Utilitários
from src.utils.input_handler import get_valid_input, clear_screen
from src.utils.validations import validate_yes_no

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # 1. Configuração do Banco de Dados
    # Definimos um caminho padrão para o arquivo .db
    db_path = os.path.join("src", "db", "estacionamento.db")
    
    try:
        # Inicializa o repositório (cria tabelas se não existirem)
        repo = EstacionamentoRepository(db_path)
    except Exception as e:
        print(f"❌ Erro crítico ao conectar ao banco de dados: {e}")
        return

    # 2. Inicializa a Lógica (O 'Cérebro')
    # Definimos regras aqui: Lotação 50, Tempo Limite 2h (120 min)
    estacionamento = Estacionamento(
        nome="Condomínio Solar", 
        capacidade_total=50, 
        tempo_limite_minutos=0
    )

    # 3. Loop Principal (Context Manager garante fechamento da conexão)
    with repo:
        while True:
            # --- HIDRATAÇÃO ---
            # A cada loop, perguntamos ao banco quantos visitantes estão ativos
            # para manter a 'catraca' do objeto Estacionamento atualizada.

            clear_screen()

            total_visitantes = repo.contar_visitantes_ativos()
            estacionamento.ocupacao_atual = total_visitantes # será corrigido após nova implementação de alocação de vagas ocupação_atual = total_visitantes + total_visitantes

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
            print("\n1. 📥 Registrar Entrada (Visitante)")
            print("2. 📤 Registrar Saída (Visitante)")
            print("3. 📋 Listar Visitantes (Verificar Vencidos)")
            print("4. 🗺️  Mapa Geral (Todos os Veículos)")
            print("5. 🏘️  Gerenciar Moradores")
            print("0. ❌ Sair")

            opcao = input("\nEscolha uma opção: ").strip()

            # --- ROTEAMENTO ---
            if opcao == '1':
                # Passamos o objeto 'estacionamento' para validar a lotação
                # e o 'repo' para salvar se estiver tudo ok.
                registrar_entrada_visitante(estacionamento, repo)
            
            elif opcao == '2':
                # Passamos 'estacionamento' para calcular o tempo/preço
                # e 'repo' para dar baixa.
                registrar_saida_visitante(estacionamento, repo)
            
            elif opcao == '3':
                # Lista e mostra o trigger visual de vencimento
                listar_visitantes_ativos(estacionamento, repo)

            elif opcao == '4':
                exibir_mapa_estacionamento(repo)
            
            elif opcao == '5':
                # Sub-menu de CRUD
                menu_gerenciar_moradores(repo)
            
            elif opcao == '0':
                # Confirma saída
                    print("\n👋 Sistema encerrado. Até logo!")
                    break
            
            else:
                print("❌ Opção inválida.")
    
            input("\nPressione Enter para voltar...")

if __name__ == "__main__":
    main()