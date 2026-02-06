"""
Módulo de Desligamento de Funcionários.
Realiza a Exclusão Lógica (Soft Delete).
O funcionário fica inativo e perde acesso ao sistema, mas o histórico é mantido.
Localização: src/functions/funcionarios/crud/deletar_funcionario.py
"""
from rich.console import Console
from src.functions.funcionarios.crud.helpers_funcionario import selecionar_funcionario
from src.ui.components import clear_screen, header, Colors

console = Console()

def demitir_funcionario(repo):
    clear_screen()
    header("DESLIGAMENTO", "RH / Demissão")

    # 1. Selecionar o Funcionário
    func = selecionar_funcionario(repo)
    if not func:
        return # Cancelou

    # 2. Confirmação de Segurança
    print("\n" + "=" * 40)
    console.print(f"[bold red]⚠ ATENÇÃO: Você está prestes a desativar:[/]")
    console.print(f"Nome: [bold white]{func.nome}[/]")
    console.print(f"CPF:  [bold white]{func.cpf}[/]")
    print("=" * 40)
    
    print(f"\nO funcionário perderá acesso imediato ao sistema.")
    print("O histórico de ações passadas será mantido para auditoria.")
    
    confirmacao = input(f"\n{Colors.RED}Digite 'DEMITIR' para confirmar: {Colors.RESET}").strip()

    if confirmacao == "DEMITIR":
        try:
            # Chama o método 'remover' do repositório (que faz o soft delete)
            repo.funcionarios.remover(func.id)
            
            console.print(f"\n[bold green]✅ Funcionário '{func.nome}' foi desligado com sucesso.[/]")
            console.print("[dim]O status agora é: Inativo[/]")
            
        except Exception as e:
            console.print(f"\n[bold red]❌ Erro ao processar desligamento: {e}[/]")
    else:
        print("\nOperação cancelada.")

    input("\nPressione ENTER para voltar...")