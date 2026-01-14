"""
Componentes visuais reutilizáveis.
Centraliza a lógica de exibição (Headers, Alerts, Menus).
Localização: src/ui/components.py
"""
from src.UI.colors import Colors
from src.utils.input_handler import clear_screen
def header(titulo, subtitulo=None):
    """
    Exibe um cabeçalho padrão.
    Limpa a tela automaticamente antes de exibir.
    """
    clear_screen()
    print(Colors.CYAN + "=" * 50 + Colors.RESET)
    print(f"{Colors.BOLD}{titulo.center(50)}{Colors.RESET}")
    if subtitulo:
        print(f"{subtitulo.center(50)}")
    print(Colors.CYAN + "=" * 50 + Colors.RESET)
    print("")

def menu_option(numero, texto):
    """Formata uma linha de opção de menu."""
    print(f"{Colors.YELLOW}[{numero}]{Colors.RESET} {texto}")

def show_success(mensagem):
    """Exibe mensagem de sucesso (Verde) e pausa."""
    print(f"\n{Colors.GREEN}✅ SUCESSO: {mensagem}{Colors.RESET}")
    input(f"{Colors.DIM}Pressione Enter para continuar...{Colors.RESET}")

def show_error(mensagem):
    """Exibe mensagem de erro (Vermelho) e pausa."""
    print(f"\n{Colors.RED}❌ ERRO: {mensagem}{Colors.RESET}")
    input(f"{Colors.DIM}Pressione Enter para tentar novamente...{Colors.RESET}")

def show_warning(mensagem):
    """Exibe alerta (Amarelo) e pausa."""
    print(f"\n{Colors.YELLOW}⚠️  ATENÇÃO: {mensagem}{Colors.RESET}")
    input(f"{Colors.DIM}Pressione Enter para continuar...{Colors.RESET}")