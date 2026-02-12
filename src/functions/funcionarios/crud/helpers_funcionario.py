from rich.console import Console
from rich.table import Table
from src.utils.input_handler import get_valid_input

console = Console()

def selecionar_funcionario(repositorio, apenas_listar=False):
    """
    Lista funcionários e permite selecionar pelo ID.
    """
    # 1. Busca dados
    funcionarios = repositorio.listar_funcionarios() # Certifique-se que o método no repo é 'listar_funcionarios' ou 'listar'
    
    # 2. SE LISTA VAZIA: Pausa obrigatória
    if not funcionarios:
        console.print("\n[bold yellow]⚠ Nenhum funcionário ativo encontrado.[/]")
        console.print("[dim]Pressione ENTER para voltar ao menu...[/]")
        input() # <--- O segredo anti-flash
        return None

    # 3. Monta Tabela
    table = Table(title="📋 QUADRO DE FUNCIONÁRIOS", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="white", justify="center", width=4)
    table.add_column("Nome", style="green")
    table.add_column("Cargo", style="magenta")
    table.add_column("CPF", justify="center")

    for f in sorted(funcionarios, key=lambda x: x.nome):
        cpf_fmt = f"***.{f.cpf[3:6]}.***-{f.cpf[9:]}"
        table.add_row(str(f.id), f.nome, f.cargo, cpf_fmt)

    console.print(table)
    
    if apenas_listar:
        # Se for só pra listar, pausa aqui também para o usuário ler!
        input("\nPressione ENTER para continuar...") 
        return None

    # 4. Seleção
    def validador_id(valor):
        if not valor.isdigit(): return None, "Digite um número."
        id_int = int(valor)
        if id_int == 0: return 0, None
        
        # Ajuste aqui conforme o nome do seu repositório (repo.funcionarios ou repo)
        func = repositorio.funcionarios.buscar_por_id(id_int)
        if func and func.ativo: return func, None
        return None, "Funcionário não encontrado ou inativo."

    console.print("\n[dim](Digite 0 para cancelar)[/]")
    selecionado, _ = get_valid_input("Digite o ID do Funcionário: ", validador_id)
    
    if selecionado == 0: return None
    return selecionado