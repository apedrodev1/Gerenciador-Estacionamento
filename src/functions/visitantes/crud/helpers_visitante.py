"""
Helpers para CRUD de Visitantes.
Funções auxiliares para selecionar itens em listas e formatar saídas.
Localização: src/functions/visitantes/crud/helpers_visitante.py
"""
from rich.console import Console
from rich.table import Table
from src.utils.input_handler import get_valid_input, clear_screen

console = Console()

def selecionar_visitante(repositorio, apenas_listar=False):
    """
    Lista todos os visitantes cadastrados usando Rich Tables.
    Retorna o Objeto Visitante selecionado ou None.
    """
    visitantes = repositorio.listar_visitantes_cadastrados()
    clear_screen()

    if not visitantes:
        console.print("\n[bold yellow]⚠ Nenhum visitante cadastrado no sistema.[/]")
        return None

    # --- 1. Montagem da Tabela Rich ---
    table = Table(title="📋 CADASTRO DE VISITANTES", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="center", width=4)
    table.add_column("Nome", style="green")
    table.add_column("CNH", justify="right")

    # Ordenação Alfabética
    visitantes_ordenados = sorted(visitantes, key=lambda v: v.nome)

    for v in visitantes_ordenados:
        table.add_row(str(v.id), v.nome, v.cnh)

    console.print(table)
    
    if apenas_listar:
        return None

    # --- 2. Validador para o Input Handler ---
    def validador_id(valor_str):
        if not valor_str.isdigit():
            return None, "O ID deve ser um número inteiro."
        
        id_int = int(valor_str)
        if id_int == 0:
            return 0, None # Código de saída
        
        # Busca no banco
        visitante = repositorio.buscar_visitante_por_id(id_int)
        if visitante:
            return visitante, None
        
        return None, f"ID {id_int} não encontrado."

    # --- 3. Captura com Loop (Input Handler) ---
    console.print("\n[dim](Digite 0 para cancelar)[/]")
    
    # O while True já está dentro do get_valid_input!
    selecionado, _ = get_valid_input("Selecione o ID do Visitante", validador_id)
    
    if selecionado == 0:
        return None
        
    return selecionado