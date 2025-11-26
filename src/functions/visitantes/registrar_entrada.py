from src.classes.Visitante import Visitante
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_names, validate_cnh

def registrar_entrada_visitante(estacionamento, repositorio):
    """
    Fluxo:
    1. Pergunta à Classe Estacionamento se tem vaga.
    2. Se tiver, pede dados ao usuário.
    3. Salva no Banco via Repositório.
    """
    print(f"\n--- 🚗 Registrar Entrada (Vagas Livres: {estacionamento.vagas_disponiveis}) ---")

    # 1. Validação Lógica (A Catraca)
    if not estacionamento.verificar_entrada():
        print("❌ O estacionamento está LOTADO! Não é possível registrar entrada.")
        return

    # 2. Coleta de Dados
    print("Preencha os dados do visitante:")
    
    nome, _ = get_valid_input("Nome do Motorista: ", validate_names)
    placa, _ = get_valid_input("Placa do Veículo: ", validate_placa)
    cnh, _ = get_valid_input("CNH: ", validate_cnh)
    
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")

    # 3. Criação do Objeto
    # Nota: Não passamos 'entrada', a classe Visitante define como 'agora' automaticamente.
    novo_visitante = Visitante(
        nome=nome,
        placa=placa,
        cnh=cnh,
        modelo=modelo,
        cor=cor
    )

    # 4. Persistência
    try:
        repositorio.registrar_entrada(novo_visitante)
        print(f"✅ Entrada registrada para {nome} ({placa}) às {novo_visitante.entrada.strftime('%H:%M')}")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")