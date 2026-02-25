"""
Módulo de Entrada de Funcionários (Catraca).
Fluxo: 
1. Identifica Veículo (Wrapper vs Manual).
2. Validações de Segurança.
3. Verifica Vagas na Zona C.
4. Registra Entrada e Ocupação da Vaga.
Localização: src/functions/funcionarios/catraca/entrada_funcionario.py
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_entrada_funcionario(repositorio, estacionamento, placa_pre_validada=None):
    """
    Registra a entrada de um funcionário na Zona C via placa.
    """
    header("ENTRADA DE FUNCIONÁRIO (CATRACA)")

    # =========================================================================
    # 1. IDENTIFICAÇÃO (Wrapper vs Manual)
    # =========================================================================
    if placa_pre_validada:
        placa = placa_pre_validada
        print(f"Placa identificada: {Colors.BOLD}{placa}{Colors.RESET}")
    else:
        placa, _ = get_valid_input("Digite a PLACA do veículo: ", validate_placa)

    # =========================================================================
    # 2. BUSCA E VALIDAÇÕES DE SEGURANÇA
    # =========================================================================
    veiculo = repositorio.buscar_veiculo_por_placa(placa)

    if not veiculo:
        show_error(f"BLOQUEADO: Veículo {placa} não cadastrado!")
        print(f"{Colors.DIM}Funcionários devem ter o carro previamente cadastrado no RH.{Colors.RESET}")
        return

    if not veiculo.funcionario_id:
        show_warning(f"ALERTA: O veículo {placa} não pertence a um Funcionário.")
        return

    if veiculo.estacionado:
        show_warning(f"O sistema indica que o veículo {placa} JÁ ESTÁ no pátio.")
        return

    # =========================================================================
    # 3. RECUPERAÇÃO DE DADOS PARA MENSAGEM
    # =========================================================================
    funcionario = repositorio.buscar_funcionario_por_id(veiculo.funcionario_id)
    
    if not funcionario:
        show_error("Erro de integridade: Funcionário não encontrado no banco de dados.")
        return

    # =========================================================================
    # 4. GESTÃO DE VAGAS (ZONA C)
    # =========================================================================
    vagas_ocupadas = repositorio.listar_vagas_ocupadas_funcionarios()
    vaga_livre = estacionamento.alocar_vaga_livre(estacionamento.capacidade_funcionarios, vagas_ocupadas)

    if vaga_livre is None:
        show_error("BLOQUEADO: A Zona C (Funcionários) está LOTADA!")
        return

    livres = estacionamento.capacidade_funcionarios - len(vagas_ocupadas)

    # =========================================================================
    # 5. EXIBIÇÃO RÁPIDA E REGISTRO
    # =========================================================================
    print("-" * 40)
    print(f"🚘 Veículo: {veiculo.modelo} ({veiculo.cor})")
    print(f"💼 Func.:   {funcionario.nome} - {funcionario.cargo}")
    print(f"📍 Destino: Zona C (Vaga {vaga_livre}) | Livres: {livres}")
    print("-" * 40)

    try:
        # 1. Altera status para estacionado e grava no Histórico (Log)
        repositorio.registrar_entrada_veiculo(veiculo.placa, tipo_dono='FUNCIONARIO')
        
        # 2. Grava a vaga ocupada na tabela de controle do RH
        repositorio.registrar_vaga_funcionario(veiculo.placa, vaga_livre, funcionario.id)
        
        print(f"\n{Colors.GREEN}✔ ACESSO LIBERADO PARA A ZONA C{Colors.RESET}")
        input(f"\n{Colors.DIM}Pressione Enter para continuar...{Colors.RESET}")
        
    except Exception as e:
        show_error(f"Erro crítico ao registrar entrada do funcionário: {e}")