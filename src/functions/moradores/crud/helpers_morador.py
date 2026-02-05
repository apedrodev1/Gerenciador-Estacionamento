"""
Helpers para CRUD de Moradores.
Funções auxiliares para selecionar itens em listas e formatar saídas.
Localização: src/functions/moradores/crud/helpers_morador.py
"""
import re
from rich.console import Console
from rich.table import Table
from src.utils.input_handler import get_valid_input, clear_screen

console = Console()

def selecionar_morador(repositorio, apenas_listar=False):
    """
    Lista todos os moradores usando Rich Tables.
    Ordenação Inteligente: Bloco (A-Z) -> Número (Crescente).
    """
    clear_screen()

    moradores = repositorio.listar_moradores()
    
    if not moradores:
        console.print("\n[bold yellow]⚠ Nenhum morador cadastrado.[/]")
        return None

    # --- 1. Preparação dos Dados (Mapa de Apartamentos) ---
    lista_aptos = repositorio.listar_apartamentos()
    mapa_aptos = {a.id: a for a in lista_aptos}

    # Criamos uma lista de tuplas (Morador, Apartamento) para facilitar a ordenação
    dados_completos = []
    for m in moradores:
        apto = mapa_aptos.get(m.id_apartamento)
        dados_completos.append((m, apto))

    # --- 2. Lógica de Ordenação Natural (Bloco -> Número) ---
    def chave_ordenacao(item):
        _, apto = item # Desempacota a tupla
        
        if not apto:
            # Joga quem não tem apto pro final da lista (ZZZ)
            return ("ZZZ", 999999) 
        
        # Extrai número (ex: "101" -> 101, "101B" -> 101, "Térreo" -> 0)
        try:
            num = int(apto.numero)
        except ValueError:
            # Regex para pegar apenas dígitos de strings como "101B"
            nums = re.findall(r'\d+', str(apto.numero))
            num = int(nums[0]) if nums else 0

        # Bloco vazio vira espaço " " para aparecer antes de "A"
        bloco = apto.bloco if apto.bloco else " "
        
        return (bloco, num)

    # Aplica a ordenação
    dados_completos.sort(key=chave_ordenacao)

    # --- 3. Montagem da Tabela Rich ---
    titulo = "LISTA DE MORADORES" if apenas_listar else "SELECIONAR MORADOR"
    table = Table(title=f"📋 {titulo}", show_header=True, header_style="bold magenta")
    
    table.add_column("ID", style="cyan", justify="center", width=4)
    table.add_column("Nome", style="green")
    table.add_column("Apartamento", style="bold white")

    for morador, apto in dados_completos:
        rotulo_apto = apto.rotulo if apto else "[dim]---[/]"
        table.add_row(str(morador.id), morador.nome, rotulo_apto)

    console.print(table)
    
    if apenas_listar:
        return None

    # --- 4. Validador para o Input Handler ---
    def validador_id(valor_str):
        if not valor_str.isdigit():
            return None, "Digite apenas números."
        
        id_int = int(valor_str)
        if id_int == 0:
            return 0, None # Código de saída/cancelamento
        
        morador = repositorio.buscar_morador_por_id(id_int)
        if morador:
            return morador, None
        
        return None, "ID não encontrado no sistema."

    # --- 5. Captura com Loop ---
    console.print("\n[dim](Digite 0 para cancelar)[/]")
    selecionado, _ = get_valid_input("Digite o ID do Morador", validador_id)
    
    if selecionado == 0:
        return None
        
    return selecionado