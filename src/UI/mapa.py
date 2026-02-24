from src.utils.input_handler import clear_screen
from src.ui.colors import Colors
from rich.console import Console
from rich.table import Table
from rich import box

def exibir_mapa_estacionamento(repositorio):
    clear_screen()
    console = Console()

    console.print("\n[bold cyan]--- 🗺️  MAPA GERAL DO ESTACIONAMENTO ---[/bold cyan]\n")
    
    ocupacao = repositorio.listar_ocupacao_completa()
    
    if not ocupacao:
        console.print("[bold yellow]📭 O estacionamento está completamente vazio.[/bold yellow]")
        input(f"\n{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")
        return

    table = Table(box=box.ROUNDED, title="Veículos no Pátio", title_justify="left")

    table.add_column("Local/Vaga", justify="center", style="cyan", no_wrap=True)
    table.add_column("Tipo", style="magenta")
    table.add_column("Motorista", style="white")
    table.add_column("Placa", justify="center", style="green")
    table.add_column("Modelo / Cor", style="dim")

    count_visitantes = 0
    count_moradores = 0
    count_funcionarios = 0 

    for row in ocupacao: 
        tipo_db = row['tipo']      # 'MORADOR', 'VISITANTE' ou 'FUNCIONARIO'
        apto_num = row['apto_num']
        apto_bloco = row['apto_bloco']
        vaga_atual = row['vaga_atual'] # <--- Atualizado para a variável abstrata
        nome = row['proprietario']
        placa = row['placa']
        modelo = row['modelo']
        cor = row['cor']
        
        # Formatação Visual
        detalhes = f"{modelo} - {cor}"

        if tipo_db == 'MORADOR':
            count_moradores += 1
            local_fmt = f"{apto_num}-{apto_bloco}" if apto_bloco else f"{apto_num}"
            tipo_fmt = "[bold blue]Morador 🏠[/bold blue]"
            nome_fmt = f"[bold]{nome}[/bold]"
        
        elif tipo_db == 'VISITANTE':
            count_visitantes += 1
            local_fmt = f"Vaga {vaga_atual}" # <--- Usa a variável abstrata
            tipo_fmt = "[bold yellow]Visitante 🚗[/bold yellow]"
            nome_fmt = nome

        elif tipo_db == 'FUNCIONARIO':
            count_funcionarios += 1
            local_fmt = f"Zona C - Vaga {vaga_atual}" # <--- Usa a mesma variável abstrata!
            tipo_fmt = "[bold green]Funcionário 💼[/bold green]"
            nome_fmt = f"[bold]{nome}[/bold]"
            
        else:
            local_fmt = "???"
            tipo_fmt = "[red]Desconhecido[/red]"
            nome_fmt = str(nome)

        table.add_row(
            str(local_fmt),
            tipo_fmt,
            str(nome_fmt),
            str(placa),
            str(detalhes)
        )

    console.print(table)

    total = count_moradores + count_visitantes + count_funcionarios 
    
    console.print(f"\n[dim]Total: {total} | Moradores: {count_moradores} | Visitantes: {count_visitantes} | Funcionários: {count_funcionarios}[/dim]")
    
    input(f"\n{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")