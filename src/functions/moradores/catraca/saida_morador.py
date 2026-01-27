"""
Módulo de Saída de Moradores.
Fluxo: Busca Veículo -> Registra Saída.
Localização: src/functions/moradores/catraca/saida_morador.py
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_saida_morador(repositorio):
    header("SAÍDA DE MORADOR 🛫")
    
    placa, _ = get_valid_input("Digite a PLACA do veículo: ", validate_placa)
    
    # 1. Busca Direta (Muito mais rápida que varrer lista)
    veiculo = repositorio.buscar_veiculo_por_placa(placa)
    
    if not veiculo:
        show_warning("❌ Veículo não encontrado no cadastro.")
        return

    # 2. Verifica Vínculo
    if not veiculo.morador_id:
        show_warning("Este veículo não está vinculado a um morador.")
        return

    # 3. Verifica Status
    if not veiculo.estacionado:
        show_warning(f"O veículo {placa} já consta como FORA do pátio.")
        return

    # 4. Recupera dono para mensagem amigável
    morador = repositorio.buscar_morador_por_id(veiculo.morador_id)
    nome_dono = morador.nome if morador else "Desconhecido"

    try:
        repositorio.registrar_saida_veiculo(veiculo.placa, tipo_dono='MORADOR') 
        show_success(f"👋 Até logo, {nome_dono}!")
        
    except Exception as e:
        show_error(f"❌ Erro ao registrar saída: {e}")