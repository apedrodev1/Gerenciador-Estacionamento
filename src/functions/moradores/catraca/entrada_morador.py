"""
Módulo de Entrada de Moradores (Catraca).
Fluxo: Identificação Automática -> Registro de Log -> Liberação.
Removida a confirmação manual para agilizar a operação.
Localização: src/functions/moradores/catraca/entrada_morador.py
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_entrada_morador(repositorio):
    """
    Registra a entrada de um morador via placa.
    Processo direto: Se a placa for válida e do condomínio, libera e loga.
    """
    header("ENTRADA DE MORADOR (CATRACA)")

    # 1. Solicita a Placa
    placa, _ = get_valid_input("Digite a PLACA do veículo: ", validate_placa)

    # 2. Busca o VEÍCULO
    # O Repositório já faz a busca otimizada (Indexada)
    veiculo = repositorio.buscar_veiculo_por_placa(placa)

    # --- VALIDAÇÕES DE SEGURANÇA ---
    
    if not veiculo:
        show_error(f"BLOQUEADO: Veículo {placa} não cadastrado!")
        print(f"{Colors.DIM}Verifique se a placa está correta.{Colors.RESET}")
        return

    if not veiculo.morador_id:
        show_warning(f"ALERTA: O veículo {placa} não pertence a um Morador.")
        print(f"{Colors.DIM}Use o menu de Visitantes para este veículo.{Colors.RESET}")
        return

    if veiculo.estacionado:
        # Se o sistema diz que já está dentro, pode ser erro de fluxo anterior,
        # mas por segurança avisamos o operador.
        show_warning(f"O sistema indica que o veículo {placa} JÁ ESTÁ no pátio.")
        return

    # 3. Recupera dados para Log e Display (Auditoria Visual)
    morador = repositorio.buscar_morador_por_id(veiculo.morador_id)
    
    # Recupera o Apto (Join manual via Repositório para garantir dados frescos)
    apto_obj = repositorio.buscar_apartamento_por_id(morador.id_apartamento)
    rotulo_apto = apto_obj.rotulo if apto_obj else "Indefinido"

    # 4. EXIBIÇÃO RÁPIDA (Feedback para o Porteiro)
    print("-" * 40)
    print(f"🚘 Veículo: {veiculo.modelo} ({veiculo.cor})")
    print(f"👤 Dono:    {morador.nome}")
    print(f"🏠 Unidade: {rotulo_apto}")
    print("-" * 40)

    # 5. REGISTRO AUTOMÁTICO (Ação)
    try:
        repositorio.registrar_entrada_veiculo(veiculo.placa, tipo_dono='MORADOR')
        
        # Feedback visual de sucesso
        print(f"\n{Colors.GREEN}✔ ACESSO LIBERADO{Colors.RESET}")
        print(f"Log de entrada registrado para {morador.nome}.")
        
    except Exception as e:
        show_error(f"Erro crítico ao registrar log: {e}")