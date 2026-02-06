"""
Módulo de Edição de Funcionários.
Permite alterar Nome, Cargo e CNH.
Não permite alterar CPF (chave única fiscal) ou ID.
Localização: src/functions/funcionarios/crud/editar_funcionario.py
"""
from rich.console import Console
from src.functions.funcionarios.crud.helpers_funcionario import selecionar_funcionario
from src.ui.components import clear_screen, header, Colors

console = Console()

def editar_dados_funcionario(repo):
    # 1. Preparação Visual
    # Limpamos a tela ANTES de chamar o helper para evitar o "flash" ou duplicidade.
    # O helper 'selecionar_funcionario' já desenha sua própria tabela com título.
    clear_screen() 

    # 2. Selecionar o Funcionário
    func = selecionar_funcionario(repo)
    if not func:
        return # Usuário digitou 0 ou cancelou

    # 3. Início da Edição (Transição de Tela: Lista -> Detalhe)
    header(f"EDITANDO: {func.nome}", "Pressione ENTER para manter o valor atual")
    
    print(f"{Colors.DIM}CPF: {func.cpf} (Não editável){Colors.RESET}\n")

    try:
        # --- CAMPO: NOME ---
        novo_nome = input(f"{Colors.BOLD}Nome atual: {func.nome}{Colors.RESET}\nNovo nome: ").strip()
        if novo_nome:
            func.nome = novo_nome # Atualiza o objeto na memória

        print("-" * 30)

        # --- CAMPO: CARGO ---
        novo_cargo = input(f"{Colors.BOLD}Cargo atual: {func.cargo}{Colors.RESET}\nNovo cargo: ").strip()
        if novo_cargo:
            func.cargo = novo_cargo

        print("-" * 30)

        # --- CAMPO: CNH ---
        cnh_atual = func.cnh if func.cnh else "Não possui"
        print(f"{Colors.BOLD}CNH atual: {cnh_atual}{Colors.RESET}")
        print(f"{Colors.DIM}(Digite '0' para remover a CNH){Colors.RESET}")
        nova_cnh = input("Nova CNH: ").strip()
        
        if nova_cnh == '0':
            func.cnh = None # Remove a CNH
        elif nova_cnh:
            # O Setter da classe Funcionario valida automaticamente
            func.cnh = nova_cnh 

        # --- PERSISTÊNCIA ---
        # Salva o objeto modificado no banco
        repo.funcionarios.atualizar(func)
        
        console.print(f"\n[bold green]✅ Dados de '{func.nome}' atualizados com sucesso![/]")

    except ValueError as e:
        # Pega erros de validação (ex: CNH inválida) vindos da Classe
        console.print(f"\n[bold red]⛔ Erro de Validação: {e}[/]")
        console.print("[yellow]⚠ Nenhuma alteração foi salva.[/]")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Erro de Banco de Dados: {e}[/]")

    input("\nPressione ENTER para voltar...")