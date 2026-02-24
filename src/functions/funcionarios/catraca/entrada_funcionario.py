"""
Módulo de Entrada de Funcionários (Catraca).
Fluxo: 
1. Verifica Vagas na Zona C.
2. Identifica Veículo e Vínculo RH.
3. Registra Entrada e Ocupação da Vaga.
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
    # 1. GESTÃO DE VAGAS (ZONA C)
    # =========================================================================
    vagas_ocupadas = repositorio.listar_vagas_ocupadas_funcionarios()
    
    # A classe abstrata acha a vaga baseada no limite configurado no .env
    vaga_livre = estacionamento.alocar_vaga_livre(estacionamento.capacidade_funcionarios, vagas_ocupadas)

    if vaga_livre is None:
        show_error("BLOQUEADO: A Zona C (Funcionários) está LOTADA!")
        return

    # Feedback visual de vagas
    livres = estacionamento.capacidade_funcionarios - len(vagas_ocupadas)
    print(f"ℹ Vagas na Zona C: {livres} | Dirija-se a {Colors.BOLD}{Colors.GREEN}Vaga {vaga_livre}{Colors.RESET}")
    print("-" * 50)

    # =========================================================================
    # 2. IDENTIFICAÇÃO (Wrapper vs Manual)
    # =========================================================================
    if placa_pre_validada:
        placa = placa_pre_validada
        print(f"Placa identificada: {Colors.BOLD}{placa}{Colors.RESET}")
    else:
        placa, _ = get_valid_input("Digite a PLACA do veículo: ", validate_placa)

    # Busca o VEÍCULO
    veiculo = repositorio.buscar_veiculo_por_placa(placa)

    # --- VALIDAÇÕES DE SEGURANÇA ---
    if not veiculo:
        show_error(f"BLOQUEADO: Veículo {placa} não cadastrado!")
        print(f"{Colors.DIM}Funcionários devem ter o carro previamente cadastrado no RH.{Colors.RESET}")
        return

    if not veiculo.funcionario_id:
        show_warning(f"ALERTA: O veículo {placa} não pertence a um Funcionário.")
        print(f"{Colors.DIM}Veículo pertence a Morador ou Visitante.{Colors.RESET}")
        return

    if veiculo.estacionado:
        show_warning(f"O sistema indica que o veículo {placa} JÁ ESTÁ no pátio.")
        return

    # =========================================================================
    # 3. RECUPERA DADOS PARA DISPLAY
    # =========================================================================
    funcionario = repositorio.buscar_funcionario_por_id(veiculo.funcionario_id)
    
    if not funcionario:
        show_error("Erro de integridade: Funcionário não encontrado no banco de dados.")
        return

    if not funcionario.ativo:
        show_error("BLOQUEADO: Este funcionário consta como INATIVO/DEMITIDO.")
        return

    # EXIBIÇÃO RÁPIDA
    print("-" * 40)
    print(f"🚘 Veículo: {veiculo.modelo} ({veiculo.cor})")
    print(f"💼 Func.:   {funcionario.nome} - {funcionario.cargo}")
    print(f"📍 Destino: Zona C (Vaga {vaga_livre})")
    print("-" * 40)

    # =========================================================================
    # 4. REGISTRO AUTOMÁTICO
    # =========================================================================
    try:
        # 1. Altera status para estacionado e grava no Histórico (Log)
        repositorio.registrar_entrada_veiculo(veiculo.placa, tipo_dono='FUNCIONARIO')
        
        # 2. Grava a vaga ocupada na tabela de controle do RH
        repositorio.registrar_vaga_funcionario(veiculo.placa, vaga_livre, funcionario.id)
        
        print(f"\n{Colors.GREEN}✔ ACESSO LIBERADO PARA A ZONA C{Colors.RESET}")
        input(f"\n{Colors.DIM}Pressione Enter para continuar...{Colors.RESET}")
        
    except Exception as e:
        show_error(f"Erro crítico ao registrar entrada do funcionário: {e}")