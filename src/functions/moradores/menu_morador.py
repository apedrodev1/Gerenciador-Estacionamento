"""
Controlador Principal: Gestão de Moradores.
Responsabilidade: Exibir o menu e rotear para os módulos de CRUD (Cadastro, Edição, Exclusão).
Localização: src/functions/moradores/menu_morador.py
"""
import os
from src.utils.input_handler import get_valid_input
from src.ui.components import header, clear_screen
from src.ui.colors import Colors

# Importa os módulos especialistas da pasta CRUD
from .crud import cadastro_morador, edicao_morador, exclusao_morador, helpers_morador

def executar_menu_moradores(repositorio):
    """
    Loop principal do menu de moradores.
    Recebe o Facade (repositorio) e passa para as funções filhas.
    """
    while True:
        clear_screen()
        header("GESTÃO DE MORADORES E APARTAMENTOS 🏘️")
        
        print(f"{Colors.BOLD}Escolha uma operação:{Colors.RESET}")
        print("1. Cadastrar Novo Morador")
        print("2. Editar Morador / Gerenciar Veículos")
        print("3. Excluir Morador")
        print("4. Listar Todos")
        print("-" * 30)
        print("0. Voltar ao Menu Principal")
        
        opcao = input("\nOpção: ").strip()
        
        if opcao == '1':
            # Chama o Wizard de Cadastro
            cadastro.cadastrar_morador_form(repositorio)
            
        elif opcao == '2':
            # Chama o Gerenciador de Edição
            edicao.editar_morador_form(repositorio)
            
        elif opcao == '3':
            # Chama o Fluxo de Exclusão
            exclusao.excluir_morador_form(repositorio)
            
        elif opcao == '4':
            # Usa o helper apenas para listar (sem selecionar)
            # Como o helper pede input, podemos criar uma função rápida aqui ou no helper
            # Para simplificar, chamamos o helper e ignoramos o retorno (efeito visual de listagem)
            helpers.selecionar_morador(repositorio)
            input(f"\n{Colors.DIM}Pressione Enter para continuar...{Colors.RESET}")
            
        elif opcao == '0':
            break
            
        else:
            print(f"{Colors.RED}Opção inválida!{Colors.RESET}")
            input("Pressione Enter...")