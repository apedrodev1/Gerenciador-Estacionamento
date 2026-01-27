"""
Funcionalidade: Exclusão de Moradores.
Remove o registro do morador e, automaticamente (Cascade), seus veículos.
Localização: src/functions/moradores/crud/exclusao.py
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_yes_no
from src.ui.colors import Colors
from src.ui.components import show_success, show_warning, show_error

from .helpers import selecionar_morador

def excluir_morador_form(repositorio):
    """
    Fluxo de exclusão segura.
    Lista o que será perdido (veículos) antes de deletar.
    """
    
    # 1. Seleciona o alvo
    morador = selecionar_morador(repositorio)
    if not morador:
        return

    # 2. Busca dados vinculados para mostrar o impacto
    veiculos = repositorio.listar_veiculos_por_morador(morador.id)
    apto = repositorio.buscar_apartamento_por_id(morador.id_apartamento)
    rotulo_apto = apto.rotulo if apto else "---"

    # 3. Exibe o Alerta
    print(f"\n{Colors.RED}{Colors.BOLD}⚠ ATENÇÃO: EXCLUSÃO DE REGISTRO{Colors.RESET}")
    print(f"Você está prestes a excluir o morador:")
    print(f"👤 {morador.nome} (ID: {morador.id})")
    print(f"🏠 Unidade: {rotulo_apto}")
    
    if veiculos:
        print(f"\n{Colors.YELLOW}Isso também excluirá PERMANENTEMENTE os seguintes veículos:{Colors.RESET}")
        for v in veiculos:
            status = "[NO PÁTIO]" if v.estacionado else ""
            print(f"   🚗 {v.placa} - {v.modelo} {status}")
    else:
        print(f"\n{Colors.DIM}(Este morador não possui veículos cadastrados){Colors.RESET}")

    print("-" * 50)
    
    # 4. Confirmação Final
    confirmar, _ = get_valid_input(
        f"Tem certeza absoluta que deseja excluir {morador.nome}? (s/n): ", 
        validate_yes_no
    )
    
    if confirmar == 's':
        try:
            # O Delete Cascade do banco cuida dos veículos
            repositorio.remover_morador(morador.id)
            show_success("Registro removido com sucesso.")
        except Exception as e:
            show_error(f"Erro ao excluir: {e}")
    else:
        print(f"\n{Colors.YELLOW}Operação cancelada.{Colors.RESET}")