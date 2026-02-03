"""
Módulo de Saída de Visitantes (Catraca).
Fluxo:
1. Busca Ticket pela Placa.
2. Verifica Tempo e Regras (Via Classe Estacionamento).
3. Baixa o Ticket.
Localização: src/functions/visitantes/catraca/saida_visitante.py
"""
from datetime import datetime
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_yes_no
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_saida_visitante(repositorio, estacionamento, placa_pre_validada=None):
    """
    Registra a saída de um veículo visitante.
    """
    header("REGISTRAR SAÍDA (VISITANTE)")

    # 1. IDENTIFICAÇÃO DO VEÍCULO
    if placa_pre_validada:
        placa = placa_pre_validada
    else:
        placa, _ = get_valid_input("Digite a PLACA do veículo: ", validate_placa)

    # 2. BUSCA DO TICKET ATIVO
    ticket = repositorio.buscar_ticket_ativo(placa)
    
    if not ticket:
        show_warning(f"Não há ticket aberto para a placa {placa}.")
        return

    # 3. CÁLCULOS (Usando Classe Estacionamento)
    agora = datetime.now()
    entrada = ticket.entrada
    
    # Cálculo apenas para exibição
    permanencia = agora - entrada
    total_minutos = int(permanencia.total_seconds() / 60)
    horas = total_minutos // 60
    minutos = total_minutos % 60
    
    # Regra de Negócio Centralizada
    # (Se o tempo limite mudar no .env, isso aqui atualiza sozinho)
    venceu = estacionamento.verificar_ticket_vencido(entrada)
    
    if venceu:
        status_txt = f"{Colors.RED}VENCIDO (Cobrar Excesso) 🚨{Colors.RESET}"
    else:
        status_txt = f"{Colors.GREEN}Dentro do limite{Colors.RESET}"

    # 4. RECUPERAÇÃO DE NOME
    nome_visitante = "Rotativo"
    if ticket.id_visitante:
        visitante_obj = repositorio.buscar_visitante_por_id(ticket.id_visitante)
        if visitante_obj:
            nome_visitante = visitante_obj.nome

    # 5. RESUMO VISUAL
    print("\n" + Colors.CYAN + "="*40 + Colors.RESET)
    print(f"{Colors.BOLD}RESUMO DA ESTADIA (Checkout){Colors.RESET}")
    print(f"👤 Visitante: {nome_visitante}")
    print(f"🚘 Placa:     {ticket.placa}")
    print(f"📍 Vaga Lib.: {ticket.numero_vaga}")
    print(f"🕒 Entrada:   {entrada.strftime('%d/%m %H:%M')}")
    print(f"⏱️  Tempo:     {horas}h {minutos}min")
    print(f"🏷️  Status:    {status_txt}")
    print(Colors.CYAN + "="*40 + Colors.RESET + "\n")

    # 6. BAIXA
    confirmar, _ = get_valid_input("Confirmar saída e liberar vaga? (s/n): ", validate_yes_no)

    if confirmar == 's':
        try:
            repositorio.remover_ticket(ticket.id)
            repositorio.registrar_log_visitante(ticket.placa, "SAIDA")
            show_success(f"Saída registrada! Vaga {ticket.numero_vaga} liberada.")
            print(f"👋 Volte sempre, {nome_visitante}!")
            
        except Exception as e:
            show_error(f"Erro ao dar baixa no banco: {e}")
    else:
        print(f"\n{Colors.YELLOW}↩️  Operação cancelada.{Colors.RESET}")