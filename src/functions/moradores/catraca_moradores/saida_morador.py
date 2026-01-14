from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa

def registrar_saida_morador(repositorio):
    print("\n--- 🛫 Saída de Morador ---")
    
    placa_busca, _ = get_valid_input("Digite a placa do morador: ", validate_placa)
    
    todos = repositorio.listar_moradores()
    morador = next((m for m in todos if m.placa == placa_busca), None)
    
    if not morador:
        print("❌ Morador não encontrado.")
        return

    if not morador.estacionado:
        print(f"⚠️  O morador {morador.nome} já consta como FORA do condomínio.")
        return

    try:
        repositorio.registrar_saida_morador(morador.placa) 
        print(f"👋 Até logo, {morador.nome}!")
    except Exception as e:
        print(f"❌ Erro ao registrar saída: {e}")