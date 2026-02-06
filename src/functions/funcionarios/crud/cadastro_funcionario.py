from rich.console import Console
from src.utils.input_handler import get_valid_input
from src.classes.Funcionario import Funcionario
from src.ui.components import header 

console = Console()

def cadastrar_novo_funcionario(repo):
    header("NOVO COLABORADOR", "Cadastro de RH")
    
    # 1. Nome
    nome, _ = get_valid_input("Nome Completo", lambda x: (x.upper(), None) if len(x)>3 else (None, "Nome muito curto"))
    if not nome: return # Cancelou

    # 2. CPF (A validação forte já está na Classe Funcionario, aqui pegamos só o texto)
    # Mas podemos validar formato básico para não perder tempo
    def validador_cpf_format(val):
        nums = ''.join(filter(str.isdigit, val))
        return (val, None) if len(nums) == 11 else (None, "CPF deve ter 11 dígitos")

    cpf_raw, _ = get_valid_input("CPF (apenas números)", validador_cpf_format)
    
    # Verifica duplicidade antes de continuar
    if repo.funcionarios.buscar_por_cpf(cpf_raw):
        console.print("[bold red]❌ Erro: CPF já cadastrado![/]")
        return

    # 3. Cargo
    cargo, _ = get_valid_input("Cargo (Ex: Porteiro, Zelador)")

    # 4. CNH (Opcional)
    console.print("[dim]Pressione ENTER se não tiver CNH[/]")
    cnh, _ = get_valid_input("CNH (Opcional)")
    
    try:
        # Criação do Objeto (Aqui o CPF e CNH são validados de verdade pela Classe)
        novo_func = Funcionario(nome=nome, cpf=cpf_raw, cargo=cargo, cnh=cnh)
        
        # Persistência
        repo.funcionarios.adicionar(novo_func)
        console.print(f"\n[bold green]✅ {nome} cadastrado com sucesso![/]")
        
    except ValueError as e:
        console.print(f"[bold red]❌ Erro de Validação: {e}[/]")
    except Exception as e:
        console.print(f"[bold red]❌ Erro no Banco: {e}[/]")
        
    input("\nPressione ENTER para continuar...")