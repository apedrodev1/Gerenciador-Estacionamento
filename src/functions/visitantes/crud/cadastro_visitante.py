"""
Funcionalidade: Cadastro de Visitantes Frequentes.
Permite registrar prestadores de serviço ou parentes e, opcionalmente, seus veículos.
Localização: src/functions/visitantes/crud/cadastro_visitante.py
"""
from src.classes.Visitante.Visitante import Visitante
from src.classes.Veiculo import Veiculo
from src.utils.input_handler import get_valid_input
from src.utils.validations import (
    validate_names, validate_cnh, validate_placa, validate_yes_no
)
from src.ui.colors import Colors
from src.ui.components import header, show_success, show_error

def cadastrar_visitante_form(repositorio):
    """
    Formulário para criar um novo Visitante Frequente.
    Separa a criação da Pessoa da criação do Veículo.
    """
    header("CADASTRAR NOVO VISITANTE")
    print(f"{Colors.DIM}ℹ Este cadastro agiliza a entrada de prestadores e parentes.{Colors.RESET}")
    
    # =========================================================================
    # PASSO 1: DADOS PESSOAIS
    # =========================================================================
    print(f"\n{Colors.BOLD}1. Dados Pessoais{Colors.RESET}")
    
    # Validação de CNH Duplicada (Regra de Negócio)
    cnhs_existentes = repositorio.listar_todas_cnhs()
    
    nome, _ = get_valid_input("Nome Completo: ", validate_names)
    
    def validador_cnh_unica(valor):
        val, erro = validate_cnh(valor)
        if erro: return None, erro
        if val in cnhs_existentes: return None, "CNH já cadastrada no sistema."
        return val, None

    cnh, _ = get_valid_input("CNH: ", validador_cnh_unica)
    
    # =========================================================================
    # PASSO 2: VEÍCULO (OPCIONAL)
    # =========================================================================
    print(f"\n{Colors.BOLD}2. Veículo Principal{Colors.RESET}")
    
    tem_carro, _ = get_valid_input("O visitante possui veículo padrão? (s/n): ", validate_yes_no)
    
    placa, modelo, cor = None, None, None
    
    if tem_carro == 's':
        placas_existentes = repositorio.listar_todas_placas()
        
        def validador_placa_unica(valor):
            val, erro = validate_placa(valor)
            if erro: return None, erro
            if val in placas_existentes: return None, "Placa já cadastrada no sistema."
            return val, None

        placa, _ = get_valid_input("Placa: ", validador_placa_unica)
        modelo = input("Marca/Modelo: ").strip().upper()
        cor = input("Cor: ").strip().upper()
    else:
        print(f"{Colors.DIM}>> Cadastro apenas da pessoa (sem veículo vinculado).{Colors.RESET}")

    # =========================================================================
    # PASSO 3: PERSISTÊNCIA
    # =========================================================================
    print(f"\n{Colors.DIM}Salvando registros...{Colors.RESET}")
    
    try:
        # 1. Salva a PESSOA (Visitante)
        novo_visitante = Visitante(nome=nome, cnh=cnh)
        
        # O repositório salva e retorna o ID gerado pelo banco
        id_gerado = repositorio.adicionar_visitante_cadastro(novo_visitante)
        
        if not id_gerado:
            raise ValueError("Erro ao gerar ID do visitante.")

        # 2. Salva o VEÍCULO (Se houver)
        msg_veiculo = "🚶 Sem veículo cadastrado."
        msg_ticket = ""

        if placa and modelo:
            novo_veiculo = Veiculo(
                placa=placa,
                modelo=modelo,
                cor=cor,
                visitante_id=id_gerado, # VÍNCULO IMPORTANTE
                estacionado=False
            )
            repositorio.adicionar_veiculo(novo_veiculo)
            msg_veiculo = f"🚗 {modelo} - {placa}"

            # --- CORREÇÃO: VINCULA TICKET AVULSO SE EXISTIR ---
            # Se o carro já estiver no pátio como avulso, atualizamos o ticket agora!
            ticket_ativo = repositorio.buscar_ticket_ativo(placa)
            if ticket_ativo:
                 repositorio.vincular_cadastro_a_ticket(placa, id_gerado)
                 msg_ticket = f"\n{Colors.CYAN}ℹ Ticket ativo encontrado e atualizado para este cadastro.{Colors.RESET}"
            # --------------------------------------------------

        show_success(f"Visitante Cadastrado com Sucesso!")
        print(f"👤 {nome}")
        print(msg_veiculo)
        if msg_ticket: print(msg_ticket) 
        
    except Exception as e:
        show_error(f"Erro ao salvar no banco de dados: {e}")