"""
Módulo de Saída de Funcionários (Catraca).
Fluxo: 
1. Busca Veículo e Vínculo RH.
2. Libera a vaga na Zona C.
3. Registra Saída no Log.
Localização: src/functions/funcionarios/catraca/saida_funcionario.py
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_saida_funcionario(repositorio, placa_pre_validada=None):
    """
    Registra a saída de um veículo de funcionário e libera a vaga da Zona C.
    """
    header("SAÍDA DE FUNCIONÁRIO 🛫")
    
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
        show_warning("❌ Veículo não encontrado no cadastro.")
        return

    if not veiculo.funcionario_id:
        show_warning("Este veículo não está vinculado a um funcionário.")
        return

    if not veiculo.estacionado:
        show_warning(f"O veículo {placa} já consta como FORA do pátio.")
        return

    # =========================================================================
    # 3. RECUPERAÇÃO DE DADOS PARA MENSAGEM
    # =========================================================================
    funcionario = repositorio.buscar_funcionario_por_id(veiculo.funcionario_id)
    nome_dono = funcionario.nome if funcionario else "Desconhecido"

    # =========================================================================
    # 4. BAIXA NO SISTEMA
    # =========================================================================
    try:
        # Passo A: Remove o registro de ocupação da Zona C (Libera a Vaga)
        repositorio.liberar_vaga_funcionario(veiculo.placa)
        
        # Passo B: Altera o status para fora (0) e grava Log de Auditoria
        repositorio.registrar_saida_veiculo(veiculo.placa, tipo_dono='FUNCIONARIO') 
        
        show_success(f"Vaga da Zona C liberada com sucesso.")
        print(f"👋 Bom descanso, {nome_dono}!\n")
        
    except Exception as e:
        show_error(f"❌ Erro ao registrar saída do funcionário: {e}")