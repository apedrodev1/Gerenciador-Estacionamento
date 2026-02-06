from src.ui.components import menu_option, clear_screen, header, Colors, show_warning
# Imports dos CRUDs que acabamos de criar
from src.functions.funcionarios.crud.cadastro_funcionario import cadastrar_novo_funcionario
from src.functions.funcionarios.crud.helpers_funcionario import selecionar_funcionario

def executar_menu_funcionarios(repo):
    while True:
        clear_screen()
        header("GESTÃO DE RH", "Controle de Funcionários e Colaboradores")
        
        menu_option("1", "Cadastrar Novo Funcionário")
        menu_option("2", "Listar Quadro de Funcionários")
        menu_option("3", "Editar Dados (Cargo/CNH)")
        menu_option("4", "Demitir / Inativar")
        print("-" * 40)
        menu_option("0", "Voltar")
        
        opcao = input(f"\n{Colors.CYAN}➤ Opção: {Colors.RESET}").strip()
        
        if opcao == '1':
            cadastrar_novo_funcionario(repo)
            
        elif opcao == '2':
            clear_screen()
            selecionar_funcionario(repo, apenas_listar=True)
            input("\nEnter para voltar...")
            
        elif opcao == '3':
            print("🚧 Em construção: Edição")
            input()
            
        elif opcao == '4':
            print("🚧 Em construção: Demissão")
            input()
            
        elif opcao == '0':
            break
        else:
            show_warning("Opção inválida.")