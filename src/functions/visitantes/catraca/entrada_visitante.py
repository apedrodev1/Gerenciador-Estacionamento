"""
Módulo de Entrada de Visitantes (Catraca).
Fluxo: 
1. Verifica Vagas (Via Classe Estacionamento).
2. Identifica Veículo (cadastrado ou rotativo).
3. Gera Ticket.
Localização: src/functions/visitantes/catraca/entrada_visitante.py
"""
from src.classes.Visitante.TicketVisitante import TicketVisitante
from src.classes.Visitante.Visitante import Visitante
from src.classes.Veiculo import Veiculo

from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_names, validate_yes_no, validate_cnh
from src.ui.components import header, show_success, show_error, show_warning, Colors

def registrar_entrada_visitante(repositorio, estacionamento, placa_pre_validada=None):
    header("REGISTRAR ENTRADA (VISITANTE)")
    
    # =========================================================================
    # 1. GESTÃO DE VAGAS (Delegada para a Classe Estacionamento)
    # =========================================================================
    tickets_ativos = repositorio.listar_tickets_ativos()
    
    # Converte para set de strings, pois o método da classe espera comparar strings/ints de forma robusta
    vagas_ocupadas = {str(t.numero_vaga) for t in tickets_ativos}
    
    # A classe Estacionamento decide qual vaga dar (respeitando o limite do .env)
    vaga_livre = estacionamento.alocar_vaga_livre(estacionamento.capacidade_visitantes, vagas_ocupadas)

    if vaga_livre is None:
        show_error("O estacionamento está LOTADO para visitantes!")
        return

    # Feedback visual usando dados da Classe
    livres = estacionamento.capacidade_visitantes - len(vagas_ocupadas)
    print(f"ℹ Vagas Livres: {livres} | Dirija-se a {Colors.BOLD}{Colors.GREEN}Vaga {vaga_livre}{Colors.RESET}")
    print("-" * 50)

    # =========================================================================
    # 2. IDENTIFICAÇÃO (Fluxo Inteligente)
    # =========================================================================
    if placa_pre_validada:
        placa = placa_pre_validada
        # print(f"Placa já cadastrada: {placa}")
    else:
        placa, _ = get_valid_input("\nDigite a PLACA do veículo: ", validate_placa)

    veiculo = repositorio.buscar_veiculo_por_placa(placa)
    
    id_visitante_vinculado = None
    nome_motorista = "rotativo"
    
    # --- CENÁRIO A: CARRO JÁ CADASTRADO ---
    if veiculo:
        if veiculo.morador_id:
            show_warning("Este veículo pertence a um MORADOR.")
            print("Use o menu de Entrada de Moradores.")
            return

        if veiculo.visitante_id:
            visitante = repositorio.buscar_visitante_por_id(veiculo.visitante_id)
            if visitante:   
                id_visitante_vinculado = visitante.id
                nome_motorista = visitante.nome

    # --- CENÁRIO B: CARRO DESCONHECIDO (ROTATIVO) ---
    else:
        print(f"\n{Colors.YELLOW}ℹ Visitante Rotativo (Não cadastrado).{Colors.RESET}")
        print("Preencha dados básicos para o Ticket:")
        nome_motorista, _ = get_valid_input("Nome do Motorista: ", validate_names)

    # =========================================================================
    # 3. GERAÇÃO DO TICKET
    # =========================================================================
    try:
        novo_ticket = TicketVisitante(
            placa=placa,
            numero_vaga=vaga_livre,
            id_visitante=id_visitante_vinculado
        )
        repositorio.criar_ticket(novo_ticket)
        repositorio.registrar_log_visitante(placa, "ENTRADA")
        
        msg = (
            f"Entrada Autorizada!\n"
            f"   👤 {nome_motorista}\n"
            f"   🚘 {placa}\n"
            f"   📍 VAGA: {vaga_livre}"
        )
        show_success(msg)

        # 4. UPSELL -- 
        if not veiculo:
            print("\n" + Colors.CYAN + "-"*50 + Colors.RESET)
            print(f"Deseja salvar {nome_motorista} no {Colors.BOLD}CADASTRO DOS VISITANTES{Colors.RESET}?")
            salvar, _ = get_valid_input("Salvar cadastro para a próxima vez? (s/n): ", validate_yes_no)
            
            if salvar == 's':
                _converter_rotativo_em_cadastrado(repositorio, nome_motorista, placa)

    except Exception as e:
        show_error(f"Erro ao criar ticket: {e}")

def _converter_rotativo_em_cadastrado(repositorio, nome, placa):
    try:
        print(f"{Colors.DIM}Criando cadastro...{Colors.RESET}")
        cnh, _ = get_valid_input("Digite a CNH para finalizar o cadastro: ", validate_cnh)
        
        nova_pessoa = Visitante(nome=nome, cnh=cnh)
        id_pessoa = repositorio.adicionar_visitante_cadastro(nova_pessoa)
        
        modelo = input("Modelo do carro (opcional): ").strip().upper()
        cor = input("Cor (opcional): ").strip().upper()
        
        novo_carro = Veiculo(
            placa=placa, 
            modelo=modelo, 
            cor=cor, 
            visitante_id=id_pessoa, 
            estacionado=True
        )
        repositorio.adicionar_veiculo(novo_carro)
        repositorio.vincular_cadastro_a_ticket(placa, id_pessoa)
        
        show_success("Cadastro Realizado!")
        
    except Exception as e:
        show_warning(f"Não foi possível completar o cadastro: {e}")