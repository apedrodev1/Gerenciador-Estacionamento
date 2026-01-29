"""
Menu: Gestão de Visitantes.
Controlador Principal para o módulo de Visitantes Frequentes.
Responsabilidade: Roteador para Cadastro, Edição, Exclusão e Listagem.
Localização: src/functions/visitantes/menu_visitante.py
"""
from src.ui.components import header, clear_screen
from src.ui.colors import Colors

# Importa os módulos especialistas da pasta CRUD
from .crud import cadastro_visitante, edicao_visitante, exclusao_visitante, helpers_visitante

def executar_menu_visitantes(repositorio):
    """
    Loop principal do menu de visitantes.
    """
    while True:
        clear_screen()
        header("GESTÃO DE VISITANTES FREQUENTES ⭐")
        
        print(f"{Colors.BOLD}Escolha uma operação:{Colors.RESET}")
        print("1. Cadastrar Novo Frequentador")
        print("2. Editar Cadastro / Gerenciar Frota")
        print("3. Remover Cadastro")
        print("4. Listar Todos")
        print("-" * 30)
        print("0. Voltar ao Menu Principal")
        
        opcao = input(f"\n{Colors.CYAN}Opção: {Colors.RESET}").strip()
        
        if opcao == '1': 
            # Chama o Wizard de Cadastro (Pessoa + Carro Opcional)
            cadastro_visitante.cadastrar_visitante_form(repositorio)
            
        elif opcao == '2': 
            # Chama o Gerenciador de Edição (Nome, CNH, Add/Rem Carros)
            edicao_visitante.editar_visitante_form(repositorio)
            
        elif opcao == '3': 
            # Chama o Fluxo de Exclusão (com aviso de cascade)
            exclusao_visitante.remover_visitante_form(repositorio)
            
        elif opcao == '4': 
            # Usa o helper apenas para listar (flag apenas_listar=True)
            helpers_visitante.selecionar_visitante(repositorio, apenas_listar=True)
            input(f"\n{Colors.DIM}Pressione Enter para continuar...{Colors.RESET}")
            
        elif opcao == '0': 
            break
            
        else:
            print(f"{Colors.RED}Opção inválida!{Colors.RESET}")
            input("Pressione Enter...")