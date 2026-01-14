from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_yes_no
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_saida_visitante(estacionamento, repositorio):
    header("REGISTRAR SAÍDA (VISITANTE)")

    # 1. Busca
    placa_busca, _ = get_valid_input("Digite a placa do veículo: ", validate_placa)

    # Busca Otimizada: Trazemos todos e filtramos (pode ser melhorado com query específica no futuro)
    visitantes_ativos = repositorio.listar_visitantes_ativos()
    
    # Filtra (Case insensitive)
    visitante_encontrado = next((v for v in visitantes_ativos if v.placa == placa_busca), None)
    
    if not visitante_encontrado:
        show_warning(f"Veículo com placa {placa_busca} não encontrado no pátio.")
        return

    # 2. Cálculos
    minutos_totais = estacionamento.calcular_tempo_permanencia(visitante_encontrado)
    horas = int(minutos_totais // 60)
    minutos = int(minutos_totais % 60)
    
    venceu = estacionamento.verificar_ticket_vencido(visitante_encontrado)
    
    if venceu:
        status_txt = f"{Colors.RED}VENCIDO (Cobrar Multa){Colors.RESET}"
    else:
        status_txt = f"{Colors.GREEN}Dentro do limite{Colors.RESET}"

    # 3. Resumo Visual
    print("\n" + Colors.CYAN + "="*40 + Colors.RESET)
    print(f"{Colors.BOLD}RESUMO DA ESTADIA{Colors.RESET}")
    print(f"👤 Nome:    {visitante_encontrado.nome}")
    print(f"🚘 Placa:   {visitante_encontrado.placa}")
    print(f"🕒 Entrada: {visitante_encontrado.entrada.strftime('%H:%M')}")
    print(f"⏱️  Tempo:   {horas}h {minutos}min")
    print(f"🏷️  Status:  {status_txt}")
    print(Colors.CYAN + "="*40 + Colors.RESET + "\n")

    # 4. Confirmação
    confirmar, _ = get_valid_input("Confirmar saída e liberar vaga? (s/n): ", validate_yes_no)

    if confirmar == 's':
        try:
            repositorio.registrar_saida(visitante_encontrado.id)
            show_success(f"Saída registrada. Vaga {visitante_encontrado.numero_vaga} liberada.")
        except Exception as e:
            show_error(f"Erro ao dar baixa no banco: {e}")
    else:
        print(f"\n{Colors.YELLOW}↩️  Operação cancelada.{Colors.RESET}")
        input("Pressione Enter para voltar...")