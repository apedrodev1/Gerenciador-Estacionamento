from src.UI.colors import Colors

def listar_visitantes_ativos(estacionamento, repositorio):
    """
    Lista todos os visitantes atualmente no estacionamento.
    Aplica o 'Trigger Visual' se o tempo limite estourou.
    """
    # 1. Busca dados do Banco
    visitantes = repositorio.listar_visitantes_ativos()

    print(f"\n--- 📋 Visitantes no Pátio ({len(visitantes)}/{estacionamento.capacidade_total}) ---")
    
    if not visitantes:
        print("Nenhum visitante registrado no momento.")
        return

    # Cabeçalho da Tabela
    print(f"{'PLACA':<10} {'NOME':<15} {'ENTRADA':<10} {'TEMPO':<10} {'STATUS'}")
    print("-" * 60)

    for v in visitantes:
        # 2. Lógica de Cálculo (Delegada para a classe Estacionamento)
        minutos = estacionamento.calcular_tempo_permanencia(v)
        venceu = estacionamento.verificar_ticket_vencido(v)

        # 3. O Trigger Visual
        if venceu:
            cor = Colors.RED
            status = "VENCIDO!"
            icone = "🚨"
        else:
            cor = Colors.GREEN
            status = "OK"
            icone = ""

        # Formatação do tempo (ex: 1h 30m)
        horas_exib = int(minutos // 60)
        min_exib = int(minutos % 60)
        tempo_str = f"{horas_exib}h {min_exib}m"

        print(f"{v.placa:<10} {v.nome:<15} {v.entrada.strftime('%H:%M'):<10} {tempo_str:<10} {cor}{status} {icone}{Colors.RESET}")
    
    print("-" * 60)