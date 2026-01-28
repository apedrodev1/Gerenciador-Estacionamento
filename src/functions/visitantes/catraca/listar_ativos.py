from src.ui.tables import criar_tabela
from src.ui.colors import Colors

def listar_visitantes_ativos(estacionamento, repositorio):
    """
    Lista todos os visitantes atualmente no estacionamento.
    Usa a nova tabela Rich padronizada.
    """
    
    visitantes = repositorio.listar_visitantes_ativos()
    
    # Prepara os dados para a tabela
    dados_linhas = []
    
    for v in visitantes:
        minutos = estacionamento.calcular_tempo_permanencia(v)
        venceu = estacionamento.verificar_ticket_vencido(v)

        # Formatação de Status com cores do Rich
        if venceu:
            status = "[bold red]VENCIDO 🚨[/bold red]"
        else:
            status = "[bold green]OK[/bold green]"

        horas = int(minutos // 60)
        mins = int(minutos % 60)
        tempo_str = f"{horas}h {mins}m"
        
        hora_entrada = v.entrada.strftime('%H:%M')

        # Adiciona a linha na lista
        dados_linhas.append([
            v.numero_vaga,
            v.placa,
            v.nome,
            hora_entrada,
            tempo_str,
            status
        ])

    # Chama o renderizador padrão
    criar_tabela(
        titulo="VISITANTES NO PÁTIO",
        colunas=["Vaga", "Placa", "Nome", "Entrada", "Tempo", "Status"],
        linhas=dados_linhas
    )
    
    # Pausa para não piscar a tela
    input(f"{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")