from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa

def registrar_entrada_morador(repositorio):
    print("\n--- 🏡 Entrada de Morador ---")
    
    # 1. Busca por Placa
    placa_busca, _ = get_valid_input("Digite a placa do morador: ", validate_placa)
    
    # Busca o objeto para validar status (se já está dentro)
    todos = repositorio.listar_moradores()
    morador = next((m for m in todos if m.placa == placa_busca), None)
    
    if not morador:
        print("❌ Morador não encontrado.")
        return

    # 2. Validação de Lógica
    if morador.estacionado:
        print(f"⚠️  O morador {morador.nome} já consta como DENTRO do condomínio.")
        return

    # 3. Registrar Entrada 
    try:
        repositorio.registrar_entrada_morador(morador.placa) 
        
        vaga_msg = f"Vaga Fixa: {morador.vaga_id}" if morador.vaga_id else "Vaga: Não atribuída"
        print(f"✅ Bem-vindo, {morador.nome}! ({vaga_msg})")
    except Exception as e:
        print(f"❌ Erro ao registrar entrada: {e}")