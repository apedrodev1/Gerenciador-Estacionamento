"""
Helpers visuais para o módulo de Visitantes.
Auxilia na listagem e seleção de registros.
"""
from src.ui.tables import criar_tabela
from src.ui.colors import Colors
from src.ui.components import show_warning

def selecionar_visitante_cadastro(repositorio, acao_titulo="SELECIONAR", apenas_listar=False):
    """Exibe tabela de cadastros frequentes e permite seleção por ID."""
    cadastrados = repositorio.listar_visitantes_cadastrados()
    
    # Prepara dados para tabela Rich
    dados = [
        [str(v.id), v.nome, v.placa, v.modelo, v.cnh]
        for v in cadastrados
    ]
    ids_validos = [v.id for v in cadastrados]

    titulo = "VISITANTES FREQUENTES" if apenas_listar else f"{acao_titulo} VISITANTE"
    criar_tabela(titulo, ["ID", "Nome", "Placa", "Modelo", "CNH"], dados)

    if not ids_validos:
        input(f"\n{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")
        return None

    if apenas_listar:
        input(f"\n{Colors.DIM}Pressione Enter para voltar ao menu...{Colors.RESET}")
        return None

    while True:
        id_str = input(f"\n{Colors.CYAN}Digite o ID (ou 0 para cancelar): {Colors.RESET}").strip()
        if id_str == '0': return None
        
        if id_str.isdigit() and int(id_str) in ids_validos:
            return next(v for v in cadastrados if v.id == int(id_str))
        show_warning("ID inválido.")