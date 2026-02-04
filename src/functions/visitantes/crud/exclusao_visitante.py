"""
Funcionalidade: Remoção de Visitantes.
Remove o registro da pessoa e, automaticamente (Cascade), seus veículos vinculados.
Localização: src/functions/visitantes/crud/exclusao.py
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_yes_no
from src.ui.components import show_success, show_error, show_warning, Colors

# Importa o helper local para selecionar quem será removido
from .helpers_visitante import selecionar_visitante

def remover_visitante_form(repositorio):
    """
    Fluxo de exclusão segura.
    Lista o que será perdido (veículos) antes de deletar.
    """
    
    # 1. Seleciona o alvo
    visitante = selecionar_visitante(repositorio)
    if not visitante:
        return

    # 2. Busca dados vinculados para mostrar o impacto
    # (Assumindo que o repositório já tem este método, conforme discutido na edição)
    veiculos = repositorio.listar_veiculos_por_visitante(visitante.id)

    # 3. Exibe o Alerta
    print(f"\n{Colors.RED}{Colors.BOLD}⚠ ATENÇÃO: EXCLUSÃO DE REGISTRO{Colors.RESET}")
    print(f"Você está prestes a excluir:")
    print(f"👤 {visitante.nome} (ID: {visitante.id})")
    
    if veiculos:
        print(f"\n{Colors.YELLOW}Isso também excluirá PERMANENTEMENTE os seguintes veículos:{Colors.RESET}")
        for v in veiculos:
            status = "[NO PÁTIO]" if v.estacionado else ""
            print(f"   🚗 {v.placa} - {v.modelo} {status}")
    else:
        print(f"\n{Colors.DIM}(Este visitante não possui veículos cadastrados){Colors.RESET}")

    print("-" * 50)
    
    # 4. Confirmação Final
    confirmar, _ = get_valid_input(
        f"Tem certeza absoluta que deseja excluir {visitante.nome}? (s/n): ", 
        validate_yes_no
    )
    
    if confirmar == 's':
        try:
            # O Delete Cascade do banco cuida dos veículos
            repositorio.remover_visitante_cadastro(visitante.id)
            show_success("Registro removido com sucesso.")
        except Exception as e:
            show_error(f"Erro ao excluir: {e}")
    else:
        print(f"\n{Colors.YELLOW}Operação cancelada.{Colors.RESET}")