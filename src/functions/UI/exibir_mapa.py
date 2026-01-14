from src.utils.input_handler import clear_screen
from rich.console import Console
from rich.table import Table
from rich import box

def exibir_mapa_estacionamento(repositorio):
    clear_screen()
    console = Console()

    console.print("\n[bold cyan]--- 🗺️  MAPA GERAL DO ESTACIONAMENTO ---[/bold cyan]\n")
    
    ocupacao = repositorio.listar_ocupacao_total()
    
    if not ocupacao:
        console.print("[bold yellow]📭 O estacionamento está completamente vazio.[/bold yellow]")
        input("\nPressione Enter para voltar...")
        return

    table = Table(box=box.ROUNDED, title="Veículos no Pátio", title_justify="left")

    table.add_column("Vaga", justify="center", style="cyan", no_wrap=True)
    table.add_column("Tipo", style="magenta")
    table.add_column("Motorista", style="white")
    table.add_column("Placa", justify="center", style="green")
    table.add_column("Modelo / Cor", style="dim")

    for item in ocupacao:
        if item['tipo'] == 'Morador':
            tipo_fmt = "[bold blue]Morador 🏠[/bold blue]"
            nome_fmt = f"[bold]{item['nome']}[/bold]"
        else:
            tipo_fmt = "[bold yellow]Visitante 🚗[/bold yellow]"
            nome_fmt = item['nome']

        detalhes = f"{item['modelo']} - {item['cor']}"

        table.add_row(
            str(item['vaga']),
            tipo_fmt,
            nome_fmt,
            item['placa'],
            detalhes
        )

    console.print(table)

    total = len(ocupacao)
    visitantes = sum(1 for x in ocupacao if x['tipo'] == 'Visitante')
    moradores = total - visitantes
    
    console.print(f"\n[dim]Total: {total} | Visitantes: {visitantes} | Moradores: {moradores}[/dim]")
    
    # A PAUSA NECESSÁRIA:
    input("\nPressione Enter para voltar...")