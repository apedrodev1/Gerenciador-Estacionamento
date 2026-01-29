"""
Helpers para CRUD de Visitantes.
Funções auxiliares para listar e selecionar registros usando a UI padronizada.
Localização: src/functions/visitantes/crud/helpers.py
"""
from src.ui.tables import criar_tabela
from src.ui.colors import Colors
from src.ui.components import show_warning
from src.utils.input_handler import get_valid_input

def selecionar_visitante(repositorio, apenas_listar=False):
    """
    Exibe tabela de visitantes frequentes e permite seleção por ID.
    Retorna: Objeto Visitante ou None.
    """
    # 1. Busca os dados
    visitantes = repositorio.listar_visitantes_cadastrados()
    
    if not visitantes:
        print(f"\n{Colors.YELLOW}⚠ Nenhum visitante frequente cadastrado.{Colors.RESET}")
        return None

    # 2. Prepara dados para a Tabela Rich
    # Colunas: ID, Nome, CNH, Data Cadastro
    dados_tabela = []
    ids_validos = []
    
    for v in visitantes:
        ids_validos.append(v.id)
        
        # Formata data para ficar mais amigável (YYYY-MM-DD -> DD/MM/YYYY)
        # Se a string vier vazia ou None, trata para não quebrar
        data_fmt = v.data_cadastro.split("T")[0] if v.data_cadastro else "---"
        if "-" in data_fmt:
            ano, mes, dia = data_fmt.split("-")
            data_fmt = f"{dia}/{mes}/{ano}"

        dados_tabela.append([
            str(v.id),
            v.nome,
            v.cnh,
            data_fmt
        ])

    # 3. Renderiza a Tabela -- Verificar a melhor forma de exibição, se por id ou ordem alfabetica
    titulo = "VISITANTES CADASTRADOS" if apenas_listar else "SELECIONAR VISITANTE"
    
    criar_tabela(
        titulo=titulo,
        colunas=["ID", "Nome", "CNH", "Desde"],
        linhas=dados_tabela
    )

    # 4. Lógica de Seleção ou Saída
    if apenas_listar:
        return None

    print(f"\n{Colors.DIM}(Digite 0 para cancelar){Colors.RESET}")
    
    def validador_id(valor):
        if not valor.isdigit(): return None, "Digite um número inteiro."
        id_int = int(valor)
        if id_int == 0: return 0, None # Saída
        if id_int not in ids_validos: return None, "ID não encontrado na lista."
        return id_int, None

    id_selecionado, _ = get_valid_input("Digite o ID: ", validador_id)
    
    if id_selecionado == 0:
        return None
        
    # Retorna o objeto completo do repositório
    return repositorio.buscar_visitante_por_id(id_selecionado)