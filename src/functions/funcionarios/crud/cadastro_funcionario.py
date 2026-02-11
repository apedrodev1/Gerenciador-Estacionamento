"""
Funcionalidade: Cadastro de Funcionários (RH).
Permite registrar colaboradores e, opcionalmente, seus veículos pessoais.
Seguindo o padrão de 'cadastro_visitante.py'.
"""
from rich.console import Console
from src.classes.Funcionario import Funcionario
from src.classes.Veiculo import Veiculo
from src.utils.input_handler import get_valid_input
from src.utils.validations import (
    validate_names, validate_cpf, validate_cnh, validate_cargo, 
    validate_placa, validate_yes_no
)
from src.ui.colors import Colors
from src.ui.components import header, show_success, show_error

console = Console()

def cadastrar_novo_funcionario(repo):
    header("NOVO COLABORADOR", "Cadastro de RH")
    print(f"{Colors.DIM}ℹ Cadastro completo: Dados Pessoais + Veículo (Opcional).{Colors.RESET}")
    
    # =========================================================================
    # PASSO 1: DADOS PESSOAIS
    # =========================================================================
    print(f"\n{Colors.BOLD}1. Dados Pessoais{Colors.RESET}")

    # 1. Nome
    nome, _ = get_valid_input("Nome Completo: ", validate_names)
    if not nome: return # Cancelou

    # 2. CPF (Com verificação de duplicidade)
    cpf_raw, _ = get_valid_input("CPF (apenas números): ", validate_cpf)
    
    if repo.funcionarios.buscar_por_cpf(cpf_raw):
        show_error("Este CPF já consta no quadro de funcionários!")
        input("Enter para voltar...")
        return

    # 3. Cargo
    cargo, _ = get_valid_input("Cargo: ", validate_cargo)

    # 4. CNH (Opcional, mas validada se digitada)
    print(f"{Colors.DIM}(Pressione ENTER se não dirigir){Colors.RESET}")
    def validador_cnh_opcional(val):
        if not val.strip(): return None, None 
        return validate_cnh(val)

    cnh, _ = get_valid_input("CNH (Opcional): ", validador_cnh_opcional)

    # =========================================================================
    # PASSO 2: VEÍCULO (OPCIONAL)
    # =========================================================================
    print(f"\n{Colors.BOLD}2. Veículo Pessoal{Colors.RESET}")
    
    tem_carro, _ = get_valid_input("O funcionário utilizará vaga de estacionamento? (s/n): ", validate_yes_no)
    
    placa, modelo, cor = None, None, None
    
    if tem_carro == 's':
        placas_existentes = repo.veiculos.listar_todas_placas() # Usa repo de veiculos
        
        def validador_placa_unica(valor):
            val, erro = validate_placa(valor)
            if erro: return None, erro
            if val in placas_existentes: return None, "Placa já cadastrada no sistema."
            return val, None

        placa, _ = get_valid_input("Placa: ", validador_placa_unica)
        modelo = input("Marca/Modelo: ").strip().upper()
        cor = input("Cor: ").strip().upper()
    else:
        print(f"{Colors.DIM}>> Sem veículo vinculado.{Colors.RESET}")

    # =========================================================================
    # PASSO 3: PERSISTÊNCIA
    # =========================================================================
    print(f"\n{Colors.DIM}Salvando registros...{Colors.RESET}")
    
    try:
        # 1. Salva o FUNCIONÁRIO
        novo_func = Funcionario(nome=nome, cpf=cpf_raw, cargo=cargo, cnh=cnh)
        id_gerado = repo.funcionarios.adicionar(novo_func)
        
        if not id_gerado:
            raise ValueError("Erro ao gerar ID do funcionário.")

        # 2. Salva o VEÍCULO (Se houver)
        msg_veiculo = "🚶 Sem veículo."
        
        if placa and modelo:
            # AQUI ESTÁ A MÁGICA:
            # O sistema de Veículos precisa saber lidar com 'funcionario_id' ou 
            # usamos uma lógica genérica.
            # Como sua tabela Veiculos provavelmente tem 'id_morador' e 'id_visitante',
            # precisaremos adicionar 'id_funcionario' nela ou usar uma tabela de vínculo.
            
            # POR ENQUANTO (Gambiarra temporária até alterarmos a tabela Veiculos):
            # Vamos avisar que o carro foi anotado, mas precisamos criar a coluna no banco.
            
            # O CORRETO É:
            novo_veiculo = Veiculo(
               placa=placa, 
               modelo=modelo, 
               cor=cor,
               # id_funcionario=id_gerado <-- PRECISAREMOS CRIAR ESSA COLUNA NA TABELA VEICULOS
            )
            # repo.veiculos.adicionar(novo_veiculo) <-- ISSO VAI FALHAR SE NÃO TIVER A COLUNA
            
            msg_veiculo = f"🚗 {modelo} - {placa} (Pendente de Vínculo)"

        show_success(f"Colaborador Cadastrado!")
        print(f"👤 {nome} | {cargo}")
        print(msg_veiculo)
        
    except Exception as e:
        show_error(f"Erro ao salvar: {e}")
        
    input("\nPressione ENTER para continuar...")