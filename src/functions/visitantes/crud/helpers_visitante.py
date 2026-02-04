"""
Helpers para CRUD de Visitantes.
Funções auxiliares para selecionar itens em listas e formatar saídas.
Localização: src/functions/visitantes/crud/helpers_visitante.py
"""
from src.ui.colors import Colors
from src.ui.tables import criar_tabela
from src.utils.input_handler import get_valid_input

def selecionar_visitante(repositorio, apenas_listar=False):
    """
    Lista todos os visitantes cadastrados.
    Ordenação: Alfabética (Nome).
    """
    visitantes = repositorio.listar_visitantes_cadastrados()
    
    if not visitantes:
        print(f"\n{Colors.YELLOW}⚠ Nenhum visitante cadastrado.{Colors.RESET}")
        return None

    # Prepara dados
    linhas = []
    for v in visitantes:
        # Colunas: ID, Nome, CNH
        linhas.append([str(v.id), v.nome, v.cnh])

    # ORDENAÇÃO: Alfabética pelo Nome (índice 1)
    linhas.sort(key=lambda x: x[1])

    titulo = "CADASTRO VISITANTES" if apenas_listar else "SELECIONAR VISITANTE"

    criar_tabela(
        titulo=titulo,
        colunas=["ID", "Nome", "CNH"],
        linhas=linhas
    )
    
    if apenas_listar:
        return None

    # Lógica de Input (ID)
    def validador_id(valor):
        if not valor.isdigit(): return None, "Digite um número inteiro."
        id_int = int(valor)
        if id_int == 0: return 0, None # Saída
        
        # Busca no banco para garantir que existe
        visitante = repositorio.buscar_visitante_por_id(id_int)
        if visitante: return visitante, None
        
        return None, "ID não encontrado."

    print(f"\n{Colors.DIM}(Digite 0 para cancelar){Colors.RESET}")
    selecionado, _ = get_valid_input("Digite o ID: ", validador_id)
    
    if selecionado == 0:
        return None
        
    return selecionado