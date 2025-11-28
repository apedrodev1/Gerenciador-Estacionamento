from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_yes_no

def registrar_entrada_morador(repositorio):
    print("\n--- 🏡 Entrada de Morador ---")
    
    # 1. Busca por Placa (Simulação de leitura de TAG/LPR)
    placa_busca, _ = get_valid_input("Digite a placa do morador: ", validate_placa)
    
    # Busca manual (idealmente seria uma query SELECT * FROM moradores WHERE placa = ?)
    # Por simplicidade, filtramos a lista completa
    todos = repositorio.listar_moradores()
    morador = next((m for m in todos if m.placa == placa_busca), None)
    
    if not morador:
        print("❌ Morador não encontrado.")
        return

    # 2. Validação de Status (A lógica de negócio simples)
    if morador.estacionado:
        print(f"⚠️  O morador {morador.nome} já consta como DENTRO do condomínio.")
        return

    # 3. Registrar Entrada
    try:
        repositorio.registrar_entrada_morador(morador.id)
        # Se a vaga for None, mostramos aviso, senão mostramos a vaga fixa
        vaga_msg = f"Vaga Fixa: {morador.vaga_id}" if morador.vaga_id else "Vaga: Não atribuída"
        print(f"✅ Bem-vindo, {morador.nome}! ({vaga_msg})")
    except Exception as e:
        print(f"❌ Erro ao registrar entrada: {e}")

