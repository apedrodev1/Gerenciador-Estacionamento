"""
Módulo de Registro de Entrada de Visitantes.
Agora com Integração Inteligente: Verifica cadastro frequente antes de pedir dados.
"""
# Importa a classe de operação (Catraca)
from src.classes.visitante.TicketVisitante import TicketVisitante
# Importa a classe de cadastro (Frequente)
from src.classes.visitante.Visitante import Visitante

from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_names, validate_cnh, validate_yes_no
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_entrada_visitante(estacionamento, repositorio):
    header("REGISTRAR ENTRADA (VISITANTE)")
    
    # 1. Busca Vaga Livre
    vagas_ocupadas = repositorio.buscar_vagas_ocupadas_visitantes()
    vaga_livre = estacionamento.alocar_vaga_visitante(vagas_ocupadas)

    if vaga_livre is None:
        show_error("O estacionamento está LOTADO para visitantes!")
        return

    print(f"ℹ️  Vagas Livres: {estacionamento.vagas_disponiveis} | Próxima: {Colors.BOLD}{Colors.GREEN}{vaga_livre}{Colors.RESET}")
    print("-" * 50)

    # 2. FLUXO INTELIGENTE: Pede a PLACA primeiro
    placa, _ = get_valid_input("\nDigite a PLACA do veículo: ", validate_placa)

    # Verifica se já existe um cadastro FREQUENTE para essa placa
    cadastro_frequente = repositorio.buscar_visitante_cadastro_por_placa(placa)
    
    # Variáveis de dados
    nome = ""
    cnh = ""
    modelo = ""
    cor = ""
    eh_novo_cadastro = False

    if cadastro_frequente:
        # --- CENÁRIO A: VISITANTE CONHECIDO ---
        print(f"\n{Colors.GREEN}✅ CADASTRO ENCONTRADO!{Colors.RESET}")
        print(f"   Nome:    {cadastro_frequente.nome}")
        print(f"   Veículo: {cadastro_frequente.modelo} - {cadastro_frequente.cor}")
        
        confirmar, _ = get_valid_input("\nConfirmar entrada com estes dados? (s/n): ", validate_yes_no)
        
        if confirmar == 's':
            nome = cadastro_frequente.nome
            cnh = cadastro_frequente.cnh
            modelo = cadastro_frequente.modelo
            cor = cadastro_frequente.cor
        else:
            print(f"\n{Colors.YELLOW}⚠️  Ok, vamos inserir os dados manualmente.{Colors.RESET}")
            cadastro_frequente = None # Força o fluxo manual
    
    if not cadastro_frequente:
        # --- CENÁRIO B: VISITANTE NOVO (Ou dados manuais) ---
        print("\nPreencha os dados do visitante:")
        nome, _ = get_valid_input("Nome do Motorista: ", validate_names)
        cnh, _ = get_valid_input("CNH: ", validate_cnh)
        modelo = input("Modelo (opcional): ")
        cor = input("Cor (opcional): ")
        eh_novo_cadastro = True

    # 3. Criação do Objeto de Visita (Ativa)
    novo_visitante = TicketVisitante(
        nome=nome,
        placa=placa,
        cnh=cnh,
        modelo=modelo,
        cor=cor,
        numero_vaga=vaga_livre
    )

    # 4. Persistência da Entrada
    try:
        repositorio.registrar_entrada(novo_visitante)
        
        # Mensagem de Sucesso
        msg = (
            f"Entrada Registrada!\n"
            f"   👤 {nome}\n"
            f"   🚘 {placa}\n"
            f"   📍 VAGA: {vaga_livre}"
        )
        show_success(msg)
        
        # 5. OFERECER CADASTRO FREQUENTE (Só se for novo)
        if eh_novo_cadastro:
            print("\n" + Colors.CYAN + "-"*50 + Colors.RESET)
            print(f"Deseja salvar {nome} como {Colors.BOLD}VISITANTE FREQUENTE{Colors.RESET}?")
            salvar, _ = get_valid_input("Salvar cadastro para a próxima vez? (s/n): ", validate_yes_no)
            
            if salvar == 's':
                freq = Visitante(nome=nome, placa=placa, cnh=cnh, modelo=modelo, cor=cor)
                try:
                    repositorio.adicionar_visitante_cadastro(freq)
                    print(f"\n{Colors.GREEN}⭐ Cadastro salvo! Na próxima, basta digitar a placa.{Colors.RESET}")
                    input("Pressione Enter para continuar...")
                except Exception as e:
                    show_warning(f"Não foi possível salvar cadastro frequente: {e}")

    except Exception as e:
        show_error(f"Erro ao registrar entrada: {e}")