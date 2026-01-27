"""
Helpers para CRUD de Moradores.
Funções auxiliares para selecionar itens em listas e formatar saídas.
Localização: src/functions/moradores/crud/helpers.py
"""
from src.ui.colors import Colors
from src.utils.input_handler import get_valid_input

def selecionar_morador(repositorio):
    """
    Lista todos os moradores e pede para o usuário escolher um pelo ID.
    Faz o cruzamento (JOIN em memória) para exibir o número do apto em vez do ID.
    Retorna: Objeto Morador ou None.
    """
    moradores = repositorio.listar_moradores()
    
    if not moradores:
        print(f"\n{Colors.YELLOW}⚠ Nenhum morador cadastrado.{Colors.RESET}")
        return None

    # --- NOVO: BUSCA APARTAMENTOS PARA EXIBIÇÃO ---
    # Precisamos traduzir "id_apartamento=5" para "101-A"
    lista_aptos = repositorio.listar_apartamentos()
    
    # Cria um dicionário rápido: { id: "Numero-Bloco" }
    mapa_aptos = {a.id: a.rotulo for a in lista_aptos}

    print(f"\n{Colors.BOLD}--- LISTA DE MORADORES ---{Colors.RESET}")
    print(f"{'ID':<5} | {'NOME':<30} | {'UNIDADE':<10}")
    print("-" * 50)
    
    for m in moradores:
        # Busca o rótulo no mapa usando o ID (Foreign Key)
        # Se não achar (banco inconsistente), mostra "---"
        nome_apto = mapa_aptos.get(m.id_apartamento, "---")
        
        print(f"{m.id:<5} | {m.nome:<30} | {nome_apto:<10}")
    
    print("-" * 50)
    
    # --- LÓGICA DE SELEÇÃO ---
    def validador_id(valor):
        if not valor.isdigit(): return None, "Digite um número."
        id_buscado = int(valor)
        
        # O repositório já devolve o objeto Morador completo
        morador = repositorio.buscar_morador_por_id(id_buscado)
        if morador: return morador, None
        return None, "ID não encontrado."

    print(f"\n{Colors.DIM}(Digite 0 para cancelar){Colors.RESET}")
    selecionado, _ = get_valid_input("Digite o ID do morador: ", validador_id)
    
    if selecionado and isinstance(selecionado, int) and selecionado == 0:
        return None # Cancelou
        
    return selecionado