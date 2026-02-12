"""
Módulo de Edição de Funcionários.
Interface padronizada com menu de opções para alterar campos específicos.
Localização: src/functions/funcionarios/crud/edicao_funcionario.py
"""
from src.ui.components import clear_screen, header, menu_option, show_success, show_error, Colors
from src.functions.funcionarios.crud.helpers_funcionario import selecionar_funcionario
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_names, validate_cargo, validate_cnh

def editar_dados_funcionario(repo):
    clear_screen()
    header("EDITAR FUNCIONÁRIO", "RH / Gestão")

    # 1. Seleciona o funcionário
    func = selecionar_funcionario(repo)
    if not func:
        return

    # 2. Loop de Edição
    while True:
        clear_screen()
        header(f"EDITANDO: {func.nome}", f"CPF: {func.cpf} (Imutável)")
        
        cnh_display = func.cnh if func.cnh else "Não cadastrada"
        
        print(f"{Colors.BOLD}1.{Colors.RESET} Nome atual:  {Colors.CYAN}{func.nome}{Colors.RESET}")
        print(f"{Colors.BOLD}2.{Colors.RESET} Cargo atual: {Colors.CYAN}{func.cargo}{Colors.RESET}")
        print(f"{Colors.BOLD}3.{Colors.RESET} CNH atual:   {Colors.CYAN}{cnh_display}{Colors.RESET}")
        print("-" * 40)
        menu_option("0", "Salvar e Voltar")

        opcao = input(f"\n{Colors.CYAN}➤ Escolha o campo para editar: {Colors.RESET}").strip()

        try:
            if opcao == '1':
                novo_nome, _ = get_valid_input("Novo Nome: ", validate_names)
                if novo_nome: 
                    func.nome = novo_nome
                    show_success("Nome atualizado na memória!")

            elif opcao == '2':
                novo_cargo, _ = get_valid_input("Novo Cargo: ", validate_cargo)
                if novo_cargo: 
                    func.cargo = novo_cargo
                    show_success("Cargo atualizado na memória!")

            elif opcao == '3':
                print(f"{Colors.DIM}(Digite 0 para remover a CNH atual){Colors.RESET}")
                
                def validador_cnh_opcional(val):
                    if val == '0': return 'REMOVER', None
                    if not val.strip(): return None, None
                    return validate_cnh(val)

                nova_cnh, _ = get_valid_input("Nova CNH: ", validador_cnh_opcional)
                
                if nova_cnh == 'REMOVER':
                    func.cnh = None
                    show_success("CNH removida!")
                elif nova_cnh:
                    func.cnh = nova_cnh
                    show_success("CNH atualizada na memória!")

            elif opcao == '0':
                # Salva no banco de dados
                repo.funcionarios.atualizar(func)
                show_success(f"Alterações salvas para {func.nome}!")
                break
            
            else:
                show_error("Opção inválida.")
                
        except ValueError as e:
            show_error(f"Erro de validação: {e}")
        except Exception as e:
            show_error(f"Erro no banco de dados: {e}")