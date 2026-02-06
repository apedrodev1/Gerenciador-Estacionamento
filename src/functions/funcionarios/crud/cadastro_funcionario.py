from rich.console import Console
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_names, validate_cpf, validate_cnh, validate_cargo
from src.classes.Funcionario import Funcionario
from src.ui.components import header 

console = Console()

def cadastrar_novo_funcionario(repo):
    header("NOVO COLABORADOR", "Cadastro de RH")
    
    # 1. Nome (Usa o validador padronizado)
    nome, _ = get_valid_input("Nome Completo: ", validate_names)
    if not nome: return # Cancelou

    # 2. CPF (Usa validação real de CPF)
    cpf_raw, _ = get_valid_input("CPF (apenas números): ", validate_cpf)
    
    # Verifica duplicidade no banco
    if repo.funcionarios.buscar_por_cpf(cpf_raw):
        console.print("[bold red]❌ Erro: CPF já cadastrado![/]")
        input("Pressione ENTER para voltar...")
        return

    # 3. Cargo (Usa o validate_cargo que criamos)
    cargo, _ = get_valid_input("Cargo (Ex: Porteiro, Zelador): ", validate_cargo)

    # 4. CNH (Opcional)
    console.print("[dim]Pressione ENTER se não tiver CNH[/]")
    
    # Validador local: Aceita VAZIO ou chama a validação rígida se tiver texto
    def validador_cnh_opcional(val):
        if not val.strip(): 
            return None, None # Retorna Sucesso com valor None
        return validate_cnh(val) # Se digitou algo, valida formato

    # Agora passamos a função, resolvendo o erro de missing argument
    cnh, _ = get_valid_input("CNH (Opcional): ", validador_cnh_opcional)
    
    try:
        # Criação do Objeto
        novo_func = Funcionario(nome=nome, cpf=cpf_raw, cargo=cargo, cnh=cnh)
        
        # Persistência
        repo.funcionarios.adicionar(novo_func)
        console.print(f"\n[bold green]✅ {nome} cadastrado com sucesso![/]")
        
    except ValueError as e:
        console.print(f"[bold red]❌ Erro de Validação: {e}[/]")
    except Exception as e:
        console.print(f"[bold red]❌ Erro no Banco: {e}[/]")
        
    input("\nPressione ENTER para continuar...")