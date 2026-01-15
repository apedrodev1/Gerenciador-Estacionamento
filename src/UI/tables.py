"""
Componente padronizado para exibição de tabelas usando a biblioteca Rich.
Localização: src/ui/tables.py
"""
from rich.console import Console
from rich.table import Table
from rich import box
from src.utils.input_handler import clear_screen
from src.ui.colors import Colors

def criar_tabela(titulo, colunas, linhas):
    """
    Gera e imprime uma tabela estilizada.
    
    Args:
        titulo (str): Título da tabela.
        colunas (list): Lista de strings com os nomes das colunas.
        linhas (list): Lista de listas/tuplas com os dados.
    """
    clear_screen()
    console = Console()
    
    # 1. Configuração Visual da Tabela
    table = Table(
        title=titulo, 
        box=box.ROUNDED,
        header_style="bold cyan",
        title_style="bold magenta",
        expand=True # Ocupa a largura total do terminal
    )

    # 2. Adicionar Colunas
    for col_nome in colunas:
        # justify="left" padrão, pode ser parametrizado no futuro se precisar
        table.add_column(col_nome, justify="left")

    # 3. Verificar se há dados
    if not linhas:
        print(f"\n{Colors.YELLOW}📭 Nenhum registro encontrado para exibir.{Colors.RESET}")
        return

    # 4. Adicionar Linhas
    for linha in linhas:
        # Converte todos os itens para string para evitar erros no Rich
        dados_str = [str(item) for item in linha]
        table.add_row(*dados_str)

    # 5. Exibição
    console.print(table)
    print("") # Linha em branco para respiro visual