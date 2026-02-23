"""
Funcionalidade: Cadastro de Funcionários (RH).
Permite registrar colaboradores, associar veículos e reativar ex-funcionários.
"""
from rich.console import Console
from src.classes.Funcionario import Funcionario
from src.classes.Veiculo import Veiculo
from src.utils.input_handler import get_valid_input
from src.utils.validations import (
    validate_names, validate_cpf, validate_cnh_unica, validate_cargo, 
    validate_placa, validate_yes_no
)
from src.ui.colors import Colors
from src.ui.components import header, show_success, show_error, show_warning

console = Console()

def cadastrar_novo_funcionario(repo):
    header("NOVO COLABORADOR", "Cadastro de RH")
    
    # =========================================================================
    # PASSO 1: DADOS PESSOAIS & VERIFICAÇÃO INTELIGENTE
    # =========================================================================
    
    # 1. CPF (Pedimos antes do nome para checar existência)
    cpf_raw, _ = get_valid_input("CPF (apenas números): ", validate_cpf)
    
    # Busca se já existe alguém com esse CPF (Ativo ou Inativo)
    funcionario_existente = repo.funcionarios.buscar_por_cpf(cpf_raw)

    if funcionario_existente:
        if funcionario_existente.ativo:
            # Caso 1: Já trabalha aqui
            show_error(f"O CPF já pertence ao funcionário ativo: {funcionario_existente.nome}")
            input("Enter para voltar...")
            return
        else:
            # Caso 2: Ex-funcionário (Recontratação)
            clear_screen = print("\n") # Apenas pulando linha
            show_warning(f"Este CPF pertence a um ex-funcionário: {funcionario_existente.nome}")
            print(f"Cargo anterior: {funcionario_existente.cargo}")
            
            reativar, _ = get_valid_input("Deseja REATIVAR este cadastro? (s/n): ", validate_yes_no)
            
            if reativar == 's':
                repo.funcionarios.reativar(funcionario_existente.id)
                show_success(f"Bem-vindo de volta! {funcionario_existente.nome} foi reativado.")
                print(f"{Colors.DIM}Dica: Use a opção 'Editar' para atualizar Cargo ou Veículo se necessário.{Colors.RESET}")
                input("Enter para continuar...")
                return
            else:
                print("Operação cancelada. O CPF continua inativo.")
                input("Enter para voltar...")
                return

    # Cenário funcionário novo.
    # 2. Nome
    nome, _ = get_valid_input("Nome Completo: ", validate_names)
    if not nome: return 

    # 3. Cargo
    cargo, _ = get_valid_input("Cargo: ", validate_cargo)

    # 4. CNH (Opcional + Verificação de Duplicidade)
    print(f"{Colors.DIM}(Pressione ENTER se não dirigir){Colors.RESET}")
    
    # Busca a lista no banco uma vez só
    cnhs_existentes = [f.cnh for f in repo.funcionarios.listar() if f.cnh]
    
    def validador_cnh_opcional(val):
        if not val.strip(): 
            return None, None # Regra 1: Se vazio, passa direto
        
        # Regra 2: Se tem texto, joga pra a função validate_cnh_unica()
        return validate_cnh_unica(val, cnhs_existentes)

    cnh, _ = get_valid_input("CNH (Opcional): ", validador_cnh_opcional)

    # =========================================================================
    # PASSO 2: VEÍCULO (OPCIONAL)
    # =========================================================================
    print(f"\n{Colors.BOLD}2. Veículo Pessoal{Colors.RESET}")
    tem_carro, _ = get_valid_input("O funcionário utilizará vaga? (s/n): ", validate_yes_no)
    
    placa, modelo, cor = None, None, None
    
    if tem_carro == 's':
        placas_existentes = repo.veiculos.listar_todas_placas()
        def validador_placa_unica(valor):
            val, erro = validate_placa(valor)
            if erro: return None, erro
            if val in placas_existentes: return None, "Placa já cadastrada."
            return val, None

        placa, _ = get_valid_input("Placa: ", validador_placa_unica)
        modelo = input("Marca/Modelo: ").strip().upper()
        cor = input("Cor: ").strip().upper()

    # =========================================================================
    # PASSO 3: PERSISTÊNCIA
    # =========================================================================
    print(f"\n{Colors.DIM}Salvando registros...{Colors.RESET}")
    
    try:
        novo_func = Funcionario(nome=nome, cpf=cpf_raw, cargo=cargo, cnh=cnh)
        id_gerado = repo.funcionarios.adicionar(novo_func)
        
        if not id_gerado: raise ValueError("Erro ao gerar ID.")

        msg_veiculo = "🚶 Sem veículo."
        if placa and modelo:
            # ATENÇÃO: Lembre-se que precisamos criar a coluna id_funcionario na tabela veiculos
            # para isso funcionar 100% no futuro.
            novo_veiculo = Veiculo(
                placa=placa,
                modelo=modelo,
                cor=cor,
                funcionario_id=id_gerado) 
            
            repo.veiculos.adicionar(novo_veiculo)

            msg_veiculo = f"🚗 {modelo} - {placa} (Cadastrado)"

        show_success(f"Colaborador Cadastrado!")
        print(f"👤 {nome} | {cargo}")
        print(msg_veiculo)
        
    except Exception as e:
        show_error(f"Erro ao salvar: {e}")
        
    input("\nPressione ENTER para continuar...")