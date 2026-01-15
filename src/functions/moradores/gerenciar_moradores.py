"""
Menu Principal de Gerenciamento de Moradores.
Roteia para as ações específicas (Actions) e usa helpers.
"""
from src.ui.components import header, menu_option, show_warning
from src.ui.colors import Colors

# Importações dos módulos irmãos
from .actions import adicionar_morador_form, editar_morador_form, remover_morador_form
from .helpers import selecionar_morador_da_lista

def menu_gerenciar_moradores(repositorio, estacionamento):
    """Sub-menu de gestão de moradores."""
    while True:
        header("GESTÃO DE MORADORES 🏘️")
        menu_option("1", "Adicionar Novo")
        menu_option("2", "Editar Cadastro")
        menu_option("3", "Remover")
        menu_option("4", "Listar Todos")
        print("-" * 30)
        menu_option("0", "Voltar")
        
        opcao = input(f"\n{Colors.CYAN}➤  Opção: {Colors.RESET}").strip()
        
        if opcao == '1': 
            adicionar_morador_form(repositorio, estacionamento)
        elif opcao == '2': 
            editar_morador_form(repositorio, estacionamento)
        elif opcao == '3': 
            remover_morador_form(repositorio)
        elif opcao == '4': 
            selecionar_morador_da_lista(repositorio, apenas_listar=True)
        elif opcao == '0': 
            break