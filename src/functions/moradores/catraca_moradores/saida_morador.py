from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa
from src.ui.components import header, show_success, show_error, show_warning

def registrar_saida_morador(repositorio):
    header("CATRACA: SAÍDA MORADOR 🛫")
    
    placa_busca, _ = get_valid_input("Digite a placa do morador: ", validate_placa)
    
    todos = repositorio.listar_moradores()
    morador = next((m for m in todos if m.placa == placa_busca), None)
    
    if not morador:
        show_warning(" ❌ Morador não encontrado no cadastro.")
        return

    if not morador.estacionado:
        show_warning(f"O morador {morador.nome} já consta como FORA.")
        return

    try:
        repositorio.registrar_saida_morador(morador.placa) 
        show_success(f" 👋 Até logo, {morador.nome}!")
        
    except Exception as e:
        show_error(f" ❌ Erro ao registrar saída: {e}")