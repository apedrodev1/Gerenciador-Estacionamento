"""
Módulo de Entrada de Moradores (Catraca).
Registra a entrada verificando a cota de vagas do apartamento.
Localização: src/functions/moradores/catraca_moradores/entrada_morador.py
"""
from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_entrada_morador(repositorio, estacionamento):
    """
    Fluxo de entrada para moradores.
    Pede a placa, verifica se existe e se o apartamento tem cota livre.
    """
    header("ENTRADA DE MORADOR (CATRACA)")

    # 1. Solicita a Placa
    placa, _ = get_valid_input("Digite a PLACA do veículo: ", validate_placa)

    # 2. Busca o morador no banco
    morador_encontrado = repositorio.buscar_morador_por_placa(placa)

    if not morador_encontrado:
        show_error(f"Veículo com placa '{placa}' não encontrado no cadastro de moradores.")
        print(f"{Colors.DIM}Dica: Verifique se a placa está correta ou cadastre o morador.{Colors.RESET}")
        return

    # 3. Verifica se já está estacionado (Evita duplicidade)
    if morador_encontrado.estacionado:
        show_warning(f"O veículo {placa} já consta como ESTACIONADO no sistema!")
        return

    print("-" * 40)
    print(f"👤 Morador: {morador_encontrado.nome}")
    print(f"🏠 Apto:    {morador_encontrado.apartamento}")
    print(f"🚘 Veículo: {morador_encontrado.modelo} ({morador_encontrado.cor})")
    print("-" * 40)

    # 4. VALIDAÇÃO DE COTA 
    # Verifica se o apartamento pode colocar mais um carro
    pode_entrar, mensagem = estacionamento.validar_cota_morador(morador_encontrado, repositorio)

    if not pode_entrar:
        # Se barrou (Cota estourada), mostra erro e cancela
        show_error(mensagem)
        return

    # Se passou na validação, mostra o saldo e pede confirmação
    print(f"\n{mensagem}")
    
    confirmar = input(f"\n{Colors.CYAN}Confirmar entrada? (s/n): {Colors.RESET}").strip().lower()
    
    if confirmar == 's':
        try:
            # Registra a entrada no banco e no histórico
            repositorio.registrar_entrada_morador(morador_encontrado.placa)
            show_success(f"Entrada registrada! Bem-vindo(a), {morador_encontrado.nome}.")
        except Exception as e:
            show_error(f"Erro ao registrar entrada: {e}")
    else:
        print("\nOperação cancelada.")