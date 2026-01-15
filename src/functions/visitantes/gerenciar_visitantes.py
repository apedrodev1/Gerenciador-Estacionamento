"""
Menu Principal de Gerenciamento de Visitantes Frequentes.
Localização: src/functions/visitantes/gerenciar_visitantes.py
"""
from src.ui.components import header, menu_option
from src.ui.colors import Colors

# Importações dos módulos locais
from .actions import adicionar_visitante_form, editar_visitante_form, remover_visitante_form
from .helpers import selecionar_visitante_cadastro

def menu_gerenciar_visitantes(repositorio):
    while True:
        header("GESTÃO DE VISITANTES FREQUENTES ⭐")
        menu_option("1", "Cadastrar Novo Frequentador")
        menu_option("2", "Editar Cadastro")
        menu_option("3", "Remover Cadastro")
        menu_option("4", "Listar Todos")
        print("-" * 30)
        menu_option("0", "Voltar")
        
        opcao = input(f"\n{Colors.CYAN}➤ Opção: {Colors.RESET}").strip()
        
        if opcao == '1': 
            adicionar_visitante_form(repositorio)
        elif opcao == '2': 
            editar_visitante_form(repositorio)
        elif opcao == '3': 
            remover_visitante_form(repositorio)
        elif opcao == '4': 
            selecionar_visitante_cadastro(repositorio, apenas_listar=True)
        elif opcao == '0': 
            break