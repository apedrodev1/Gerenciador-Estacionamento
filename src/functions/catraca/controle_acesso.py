"""
Módulo: Controle de Acesso Inteligente (Wrapper).
Responsabilidade: Receber uma placa e direcionar automaticamente para:
- Entrada/Saída de Morador
- Entrada/Saída de Visitante
- Entrada/Saída de Funcionário
Localização: src/functions/catraca/controle_acesso.py
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa
from src.ui.components import header, show_warning, Colors

from src.functions.moradores.catraca.entrada_morador import registrar_entrada_morador
from src.functions.moradores.catraca.saida_morador import registrar_saida_morador
from src.functions.visitantes.catraca.entrada_visitante import registrar_entrada_visitante
from src.functions.visitantes.catraca.saida_visitante import registrar_saida_visitante
from src.functions.funcionarios.catraca.entrada_funcionario import registrar_entrada_funcionario
from src.functions.funcionarios.catraca.saida_funcionario import registrar_saida_funcionario

def registrar_acesso_unificado(repositorio, estacionamento):
    """
    Hub Central da Catraca.
    O porteiro digita a placa E O SISTEMA DECIDE o que fazer.
    """
    header("CATRACA INTELIGENTE 🚧")
    
    # 1. Input Único da Placa
    placa, _ = get_valid_input("Digite a PLACA do veículo: ", validate_placa)
    
    print(f"\n{Colors.DIM}🔍 Analisando placa {placa}...{Colors.RESET}")
    
    # 2. Busca Inteligente: Quem é esse carro?
    # (O repositório já sabe buscar na tabela de veiculos)
    veiculo = repositorio.buscar_veiculo_por_placa(placa)
    
    # --- CENÁRIO A: Veículo NÃO Cadastrado (Provável Visitante Avulso) ---
    if not veiculo:
        # Se não achou na tabela fixa, verifica se tem um TICKET ABERTO (Visitante saindo)
        ticket = repositorio.buscar_ticket_ativo(placa)
        
        if ticket:
            print(f"🎫 Ticket de Visitante encontrado. Direcionando para SAÍDA...")
            registrar_saida_visitante(repositorio, estacionamento, placa_pre_validada=placa)
        else:
            print(f"🆕 Veículo desconhecido. Direcionando para ENTRADA DE VISITANTE...")
            registrar_entrada_visitante(repositorio, estacionamento, placa_pre_validada=placa)
        return

    # --- CENÁRIO B: Veículo de MORADOR ---
    if veiculo.morador_id:
        morador = repositorio.buscar_morador_por_id(veiculo.morador_id)
        if not morador:
            print(f"{Colors.RED}Erro de inconsistência: Veículo sem dono válido.{Colors.RESET}")
            return
            
        print(f"✅ Identificado: MORADOR - {morador.nome}")
        
        # Lógica de status: Se já está dentro, sai. Se está fora, entra.
        if veiculo.estacionado:
            print("Status Atual: [DENTRO] ➡ Registrando SAÍDA...")
            registrar_saida_morador(repositorio, placa_pre_validada=placa)
        else:
            print("Status Atual: [FORA] ➡ Registrando ENTRADA...")
            registrar_entrada_morador(repositorio, estacionamento, placa_pre_validada=placa)
        return

    # --- CENÁRIO C: Veículo de VISITANTE FREQUENTE (Prestador/Parente) ---
    if veiculo.visitante_id:
        visitante = repositorio.buscar_visitante_por_id(veiculo.visitante_id)
        print(f"✅ Identificado: VISITANTE FREQUENTE - {visitante.nome}")
        
        # Visitantes frequentes também geram tickets para controlar tempo
        # Então verificamos se tem ticket aberto
        ticket = repositorio.buscar_ticket_ativo(placa)
        
        if ticket:
            print("Status Atual: [DENTRO] ➡ Registrando SAÍDA...")
            registrar_saida_visitante(repositorio, estacionamento, placa_pre_validada=placa)
        else:
            print("Status Atual: [FORA] ➡ Registrando ENTRADA...")
            registrar_entrada_visitante(repositorio, estacionamento, placa_pre_validada=placa)
        return

    # --- CENÁRIO D: Veículo de FUNCIONÁRIO (Zona C) ---
    if veiculo.funcionario_id:
        funcionario = repositorio.buscar_funcionario_por_id(veiculo.funcionario_id)
        if not funcionario:
            print(f"{Colors.RED}Erro de inconsistência: Veículo de funcionário sem dono válido.{Colors.RESET}")
            return
            
        print(f"✅ Identificado: FUNCIONÁRIO - {funcionario.nome} ({funcionario.cargo})")
        
        if veiculo.estacionado:
            print("Status Atual: [DENTRO] ➡ Registrando SAÍDA...")
            registrar_saida_funcionario(repositorio, placa_pre_validada=placa)
        else:
            print("Status Atual: [FORA] ➡ Registrando ENTRADA...")
            registrar_entrada_funcionario(repositorio, estacionamento, placa_pre_validada=placa)
        return