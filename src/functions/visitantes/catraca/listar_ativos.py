"""
Funcionalidade: Monitoramento do Pátio (Visitantes).
Lista todos os veículos de visitantes (Tickets Abertos) atualmente no estacionamento.
Localização: src/functions/visitantes/catraca/listar_ativos.py
"""
from datetime import datetime
from src.ui.tables import criar_tabela
from src.ui.colors import Colors

def listar_visitantes_ativos(repositorio):
    """
    Lista todos os tickets ativos.
    Calcula o tempo de permanência em tempo real e identifica se é Avulso ou Cadastrado.
    """
    # 1. Busca todos os tickets abertos (que não têm data de saída)
    # Certifique-se de que o TicketRepository tenha este método implementado
    tickets = repositorio.listar_tickets_ativos()
    
    if not tickets:
        print(f"\n{Colors.YELLOW}ℹ O pátio de visitantes está vazio.{Colors.RESET}")
        input(f"\n{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")
        return

    # 2. Prepara os dados para a tabela
    dados_linhas = []
    agora = datetime.now()
    
    for t in tickets:
        # --- Cálculo de Tempo ---
        # t.entrada já é um objeto datetime (convertido na classe TicketVisitante)
        delta = agora - t.entrada
        total_minutos = int(delta.total_seconds() / 60)
        
        horas = total_minutos // 60
        mins = total_minutos % 60
        tempo_str = f"{horas}h {mins}m"
        
        # --- Identificação (Join Manual) ---
        if t.id_visitante:
            # É um visitante frequente: buscamos o nome
            visitante = repositorio.buscar_visitante_por_id(t.id_visitante)
            nome_exibicao = f"{visitante.nome} [cyan](Freq)[/]" if visitante else "Desconhecido"
        else:
            # É avulso
            nome_exibicao = "[dim]Avulso (Rotativo)[/]"

        # --- Status / Regra de Negócio Visual ---
        # Exemplo: Se passar de 24h, marca como ALERTA. 
        # (Isso substitui a antiga função 'verificar_ticket_vencido') SErá que é a melhor abordage??? 
        if horas >= 24:
            status = "[bold red]ALERTA (+24h) 🚨[/]"
        else:
            status = "[bold green]EM USO[/]"

        # Formata hora de entrada
        hora_entrada_str = t.entrada.strftime('%H:%M')
        
        # Opcional: Adiciona data se entrou em dia anterior
        if t.entrada.date() != agora.date():
            hora_entrada_str = f"{t.entrada.strftime('%d/%m')} {hora_entrada_str}"

        # Adiciona a linha
        dados_linhas.append([
            str(t.numero_vaga),
            t.placa,
            nome_exibicao,
            hora_entrada_str,
            tempo_str,
            status
        ])

    # 3. Renderiza a Tabela
    criar_tabela(
        titulo=f"VISITANTES NO PÁTIO ({len(tickets)})",
        colunas=["Vaga", "Placa", "Identificação", "Entrada", "Tempo", "Status"],
        linhas=dados_linhas
    )
    
    input(f"\n{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")