"""
Helpers visuais para o módulo de Moradores.
Auxilia na seleção de itens e inputs específicos.
Localização: src/functions/moradores/helpers.py
"""
from src.utils.input_handler import get_valid_input
from src.ui.tables import criar_tabela
from src.ui.colors import Colors
from src.ui.components import show_warning

# (Função solicitar_input_vaga foi removida pois não usamos mais)

def selecionar_morador_da_lista(repositorio, acao_titulo="SELECIONAR", apenas_listar=False):
    """Mostra tabela e retorna o morador escolhido (ou None)."""
    moradores = repositorio.listar_moradores()
    
    # CORREÇÃO: Mostra "Garantida (Apto X)" em vez de Vaga ID ou Rotativa
    dados = []
    for m in moradores:
        localizacao = f"[green]Apto {m.apartamento}[/green]"
        
        dados.append([
            str(m.id), 
            m.nome, 
            m.apartamento, 
            m.placa, 
            localizacao
        ])
        
    ids_validos = [m.id for m in moradores]

    titulo = "LISTA DE MORADORES" if apenas_listar else f"{acao_titulo} MORADOR"
    # Ajustamos o nome da coluna de 'Vaga Fixa' para 'Vaga/Local'
    criar_tabela(titulo, ["ID", "Nome", "Apto", "Placa", "Vaga/Local"], dados)

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
            return next(m for m in moradores if m.id == int(id_str))
        show_warning("ID inválido ou não encontrado.")