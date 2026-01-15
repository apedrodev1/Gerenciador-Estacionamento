"""
Helpers visuais para o módulo de Moradores.
Auxilia na seleção de itens e inputs específicos.
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_yes_no
from src.ui.tables import criar_tabela
from src.ui.colors import Colors
from src.ui.components import show_warning

def solicitar_input_vaga(estacionamento):
    """
    Pede uma vaga fixa usando o padrão visual do sistema.
    Retorna: Inteiro (Vaga) ou None (Se não quiser/pular).
    """
    def validar_opcao_vaga(texto):
        if not texto.strip(): return 'n', None
        return validate_yes_no(texto)

    opcao, _ = get_valid_input(
        "\nAtribuir vaga fixa numérica? (s/n/Enter para pular): ", 
        validar_opcao_vaga
    )
    
    if opcao == 'n':
        return None

    def validar_numero_vaga(texto):
        if not texto.isdigit(): 
            return None, "Digite apenas números inteiros."
        v_num = int(texto)
        sucesso, msg = estacionamento.validar_atribuicao_vaga_morador(v_num)
        if sucesso:
            return v_num, None
        return None, msg

    vaga_id, _ = get_valid_input(
        f"Número da Vaga (Acima de {estacionamento.capacidade_total}): ", 
        validar_numero_vaga
    )
    
    return vaga_id

def selecionar_morador_da_lista(repositorio, acao_titulo="SELECIONAR", apenas_listar=False):
    """Mostra tabela e retorna o morador escolhido (ou None)."""
    moradores = repositorio.listar_moradores()
    
    dados = [
        [str(m.id), m.nome, m.apartamento, m.placa, 
         f"[cyan]{m.vaga_id}[/cyan]" if m.vaga_id else "[dim]Rotativa[/dim]"]
        for m in moradores
    ]
    ids_validos = [m.id for m in moradores]

    titulo = "LISTA DE MORADORES" if apenas_listar else f"{acao_titulo} MORADOR"
    criar_tabela(titulo, ["ID", "Nome", "Apto", "Placa", "Vaga Fixa"], dados)

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