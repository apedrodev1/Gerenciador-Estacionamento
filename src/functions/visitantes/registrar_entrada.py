from src.classes.Visitante import Visitante
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_names, validate_cnh

def registrar_entrada_visitante(estacionamento, repositorio):
    print(f"\n--- 🚗 Registrar Entrada (Vagas Livres: {estacionamento.vagas_disponiveis}) ---")

    # 1. Busca quais vagas já estão ocupadas no banco (Repo -> Banco)
    vagas_ocupadas = repositorio.buscar_vagas_ocupadas_visitantes()

    # 2. Usa a lógica do Estacionamento para descobrir a próxima vaga livre (Lógica)
    vaga_livre = estacionamento.alocar_vaga_visitante(vagas_ocupadas)

    if vaga_livre is None:
        print("❌ O estacionamento está LOTADO (Não há números de vaga disponíveis)!")
        return

    print(f"ℹ️  Próxima vaga disponível: {vaga_livre}")

    # 3. Coleta de Dados
    print("\nPreencha os dados do visitante:")
    nome, _ = get_valid_input("Nome do Motorista: ", validate_names)
    placa, _ = get_valid_input("Placa do Veículo: ", validate_placa)
    cnh, _ = get_valid_input("CNH: ", validate_cnh)
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")

    # 4. Criação do Objeto com a Vaga Alocada
    novo_visitante = Visitante(
        nome=nome,
        placa=placa,
        cnh=cnh,
        modelo=modelo,
        cor=cor,
        numero_vaga=vaga_livre  # <--- Salvamos a vaga aqui
    )

    # 5. Persistência
    try:
        repositorio.registrar_entrada(novo_visitante)
        print("\n" + "="*40)
        print(f"✅ ENTRADA CONFIRMADA!")
        print(f"👤 Motorista: {nome}")
        print(f"🚘 Placa: {placa}")
        print(f"🅿️  DIRIJA-SE À VAGA: {vaga_livre}") 
        print("="*40)
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")