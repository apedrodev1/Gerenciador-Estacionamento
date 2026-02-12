"""
Módulo de Edição de Funcionários.
Permite alterar Nome, Cargo e Gerenciar Veículo.
CPF e CNH são imutáveis (identidade).
"""
from src.ui.components import clear_screen, header, menu_option, show_success, show_error, Colors
from src.functions.funcionarios.crud.helpers_funcionario import selecionar_funcionario
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_names, validate_cargo, validate_placa
from src.classes.Veiculo import Veiculo

def editar_dados_funcionario(repo):
    clear_screen()
    header("EDITAR FUNCIONÁRIO", "RH / Gestão")

    # 1. Seleciona
    func = selecionar_funcionario(repo)
    if not func: return

    # 2. Loop de Edição
    while True:
        clear_screen()
        
        # CNH e CPF agora são apenas visuais (Imutáveis)
        cnh_display = func.cnh if func.cnh else "Não cadastrada"
        subtitulo = f"CPF: {func.cpf} |"
        
        header(f"EDITANDO: {func.nome}", subtitulo)
        
        # Verifica se tem veículo vinculado (Precisamos implementar buscar_por_funcionario no repo de veiculos,
        # ou buscar pela placa se soubermos. Por enquanto, vamos listar e filtrar na "mão" ou adicionar o método)
        # SUPONDO que repo.veiculos.buscar_por_funcionario(id) exista. Se não, implementaremos.
        # Por enquanto, mostramos opção genérica.
        
        print(f"{Colors.BOLD}1.{Colors.RESET} Alterar Nome:   {Colors.CYAN}{func.nome}{Colors.RESET}")
        print(f"{Colors.BOLD}2.{Colors.RESET} Alterar Cargo:  {Colors.CYAN}{func.cargo}{Colors.RESET}")
        print(f"{Colors.BOLD}3.{Colors.RESET} Gerenciar Veículo")
        print("-" * 40)
        menu_option("0", "Salvar e Voltar")

        opcao = input(f"\n{Colors.CYAN}➤ Opção: {Colors.RESET}").strip()

        try:
            if opcao == '1':
                novo_nome, _ = get_valid_input("Novo Nome: ", validate_names)
                if novo_nome: 
                    func.nome = novo_nome
                    show_success("Nome alterado (pendente salvar).")

            elif opcao == '2':
                novo_cargo, _ = get_valid_input("Novo Cargo: ", validate_cargo)
                if novo_cargo: 
                    func.cargo = novo_cargo
                    show_success("Cargo alterado (pendente salvar).")

            elif opcao == '3':
                # SUB-MENU DE VEÍCULO
                gerenciar_veiculo_funcionario(repo, func)

            elif opcao == '0':
                repo.funcionarios.atualizar(func)
                show_success(f"Dados de {func.nome} atualizados!")
                break
            
            else:
                show_error("Opção inválida.")
                
        except Exception as e:
            show_error(f"Erro: {e}")

def gerenciar_veiculo_funcionario(repo, func):
    """Sub-função para adicionar/remover veículo do funcionário."""
    clear_screen()
    header(f"VEÍCULO DE {func.nome.upper()}")
    
    # Busca veículos deste funcionário
    # Precisamos adicionar este método no VeiculoRepository!
    # Vou usar um método hipotético 'listar_por_funcionario'.
    veiculos = repo.veiculos.listar_por_funcionario(func.id) 
    
    if veiculos:
        print(f"Veículo atual: {Colors.GREEN}{veiculos[0].modelo} - {veiculos[0].placa}{Colors.RESET}\n")
        print("1. Remover este veículo")
        print("0. Voltar")
        op = input("\nOpção: ")
        if op == '1':
            repo.veiculos.remover(veiculos[0].placa) # Remove do banco
            show_success("Veículo removido!")
    else:
        print(f"{Colors.YELLOW}Nenhum veículo vinculado.{Colors.RESET}\n")
        print("1. Adicionar Veículo")
        print("0. Voltar")
        op = input("\nOpção: ")
        if op == '1':
            placa, _ = get_valid_input("Placa: ", validate_placa)
            
            # Verifica se placa já existe
            if repo.veiculos.buscar_por_placa(placa):
                show_error("Placa já cadastrada no sistema!")
                return

            modelo = input("Modelo: ").strip().upper()
            cor = input("Cor: ").strip().upper()
            
            novo_carro = Veiculo(placa=placa, modelo=modelo, cor=cor, id_funcionario=func.id)
            repo.veiculos.adicionar(novo_carro)
            show_success("Veículo adicionado com sucesso!")