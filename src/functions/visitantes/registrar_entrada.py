from src.classes.Visitante import Visitante
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_names, validate_cnh
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_entrada_visitante(estacionamento, repositorio):
    header("REGISTRAR ENTRADA (VISITANTE)")
    print(f"ℹ️  Vagas de Visitantes Livres: {estacionamento.vagas_disponiveis}")

    # 1. Busca Vagas
    vagas_ocupadas = repositorio.buscar_vagas_ocupadas_visitantes()
    vaga_livre = estacionamento.alocar_vaga_visitante(vagas_ocupadas)

    if vaga_livre is None:
        show_error("O estacionamento está LOTADO para visitantes!")
        return

    print(f"\n🅿️  Próxima vaga sugerida: {Colors.BOLD}{Colors.GREEN}{vaga_livre}{Colors.RESET}")

    # 2. Coleta de Dados
    print("\n--- Dados do Visitante ---")
    nome, _ = get_valid_input("Nome do Motorista: ", validate_names)
    placa, _ = get_valid_input("Placa do Veículo: ", validate_placa)
    cnh, _ = get_valid_input("CNH (apenas números): ", validate_cnh)
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")

    # 3. Criação e Persistência
    novo_visitante = Visitante(
        nome=nome,
        placa=placa,
        cnh=cnh,
        modelo=modelo,
        cor=cor,
        numero_vaga=vaga_livre
    )

    try:
        repositorio.registrar_entrada(novo_visitante)
        
        # Mensagem Bonita com Pausa
        msg = (
            f"Visitante registrado com sucesso!\n"
            f"   👤 {nome}\n"
            f"   🚘 {placa}\n"
            f"   📍 VAGA: {vaga_livre}"
        )
        show_success(msg)
        
    except Exception as e:
        show_error(f"Erro ao salvar no banco: {e}")