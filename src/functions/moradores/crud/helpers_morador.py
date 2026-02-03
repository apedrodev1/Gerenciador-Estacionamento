"""
Helpers para CRUD de Moradores.
Funções auxiliares para selecionar itens em listas e formatar saídas.
Localização: src/functions/moradores/crud/helpers_morador.py
"""
import re
from src.ui.colors import Colors
from src.ui.tables import criar_tabela
from src.utils.input_handler import get_valid_input

def selecionar_morador(repositorio, apenas_listar=False):
    """
    Lista todos os moradores.
    Ordenação Inteligente: Bloco (A-Z) -> Número (Crescente).
    """
    moradores = repositorio.listar_moradores()
    
    if not moradores:
        print(f"\n{Colors.YELLOW}⚠ Nenhum morador cadastrado.{Colors.RESET}")
        return None

    lista_aptos = repositorio.listar_apartamentos()
    # Mapa guarda o objeto completo do apartamento, não só o rótulo
    mapa_aptos = {a.id: a for a in lista_aptos}

    linhas = []
    for m in moradores:
        apto = mapa_aptos.get(m.id_apartamento)
        rotulo = apto.rotulo if apto else "---"
        
        # Guardamos dados brutos para ordenação escondida
        # [ID_str, Nome, Rotulo_Visivel, Objeto_Apto]
        linhas.append([str(m.id), m.nome, rotulo, apto])

    # --- FUNÇÃO DE ORDENAÇÃO NATURAL ---
    def chave_ordenacao(linha):
        apto = linha[3] # Objeto Apartamento (coluna extra que não exibiremos)
        if not apto:
            return ("ZZZ", 999999) # Joga quem não tem apto pro final
        
        # Tenta extrair número inteiro do apto para ordenar 1, 2, 10...
        # Se o numero for "101", vira 101. Se for "Térreo", vira 0 (ou outro critério)
        try:
            num = int(apto.numero)
        except ValueError:
            # Se tiver letras no número (ex: "101B"), usa regex para pegar só os dígitos
            nums = re.findall(r'\d+', str(apto.numero))
            num = int(nums[0]) if nums else 0

        # Ordem de prioridade: 1º Bloco, 2º Número
        # Bloco vazio ("") vira " " para vir antes de "A"
        bloco = apto.bloco if apto.bloco else " "
        
        return (bloco, num)

    # Aplica a ordenação
    linhas.sort(key=chave_ordenacao)

    # Remove a coluna extra (Objeto Apto) antes de exibir
    dados_finais = [l[:3] for l in linhas]

    titulo = "LISTA DE MORADORES" if apenas_listar else "SELECIONAR MORADOR"
    
    criar_tabela(
        titulo=titulo,
        colunas=["ID", "Nome", "Apartamento"],
        linhas=dados_finais
    )
    
    if apenas_listar:
        return None

    def validador_id(valor):
        if not valor.isdigit(): return None, "Digite um número."
        id_buscado = int(valor)
        morador = repositorio.buscar_morador_por_id(id_buscado)
        if morador: return morador, None
        return None, "ID não encontrado."

    print(f"\n{Colors.DIM}(Digite 0 para cancelar){Colors.RESET}")
    selecionado, _ = get_valid_input("Digite o ID do morador: ", validador_id)
    
    if selecionado and isinstance(selecionado, int) and selecionado == 0:
        return None 
        
    return selecionado