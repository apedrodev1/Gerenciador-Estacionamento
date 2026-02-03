"""
Funcionalidade: Cadastro de Novos Moradores.
Fluxo: 
1. Identifica/Cria Apartamento (Entidade Física).
2. Valida limite de vagas do Apartamento.
3. Coleta dados Pessoais (Cria Morador vinculado ao ID do Apto).
4. Coleta dados do Veículo (se houver vaga).
Localização: src/functions/moradores/crud/cadastro.py
"""
from src.classes.Morador import Morador
from src.classes.Veiculo import Veiculo
from src.classes.Apartamento import Apartamento
from src.utils.input_handler import get_valid_input
from src.utils.validations import (
    validate_names, validate_cnh, validate_apartamento, 
    validate_placa, validate_yes_no
)
from src.ui.colors import Colors
from src.ui.components import header, show_success, show_error, show_warning

def cadastrar_morador_form(repositorio):
    """
    Formulário Wizard para cadastrar morador e seu primeiro veículo.
    Agora respeita a integridade relacional (Apartamento -> Morador -> Veículo).
    """
    header("NOVO MORADOR")
    
    # =========================================================================
    # PASSO 1: IDENTIFICAÇÃO DO APARTAMENTO (Onde ele mora?)
    # =========================================================================
    print(f"\n{Colors.BOLD}1. Endereço do Morador{Colors.RESET}")
    
    # 1.1 Coleta Número
    # Nota: validate_apartamento verifica apenas formato numérico/string simples
    num_apto, _ = get_valid_input("Número do Apartamento: ", validate_apartamento)
    
    # 1.2 Coleta Bloco (Opcional)
    bloco = input("Bloco (opcional, Enter para pular): ").strip().upper()
    
    # 1.3 Busca ou Cria o Apartamento no Banco
    print(f"{Colors.DIM}Verificando unidade residencial...{Colors.RESET}")
    
    apto_obj = repositorio.buscar_apartamento_por_rotulo(num_apto, bloco)
    
    if apto_obj:
        # Já existe: Usamos o ID dele
        id_apto_final = apto_obj.id
        print(f"✔ Unidade {apto_obj.rotulo} selecionada (ID: {id_apto_final}).")
    else:
        # Não existe: Criamos agora
        print(f"ℹ Unidade {num_apto} {bloco} não cadastrada. Criando nova...")
        novo_apto = Apartamento(numero=num_apto, bloco=bloco) # Vagas padrão = 2
        id_apto_final = repositorio.criar_apartamento(novo_apto)
        
        if not id_apto_final:
            show_error("Erro crítico ao criar unidade. Cadastro cancelado.")
            return
        
        # Recarrega o objeto para ter certeza que temos os dados (ex: limite de vagas)
        apto_obj = repositorio.buscar_apartamento_por_id(id_apto_final)

    # =========================================================================
    # PASSO 2: DADOS PESSOAIS
    # =========================================================================
    print(f"\n{Colors.BOLD}2. Dados Pessoais{Colors.RESET}")
    
    # Validação de CNH Duplicada
    cnhs_existentes = repositorio.listar_todas_cnhs()
    
    nome, _ = get_valid_input("Nome Completo: ", validate_names)
    
    def validador_cnh_unica(valor):
        val, erro = validate_cnh(valor)
        if erro: return None, erro
        if val in cnhs_existentes: return None, "Esta CNH já está cadastrada no sistema."
        return val, None

    cnh, _ = get_valid_input("CNH: ", validador_cnh_unica)
    
    # =========================================================================
    # PASSO 3: DADOS DO VEÍCULO (Com verificação de cota)
    # =========================================================================
    print(f"\n{Colors.BOLD}3. Veículo Principal{Colors.RESET}")
    
    # Verifica a cota do APARTAMENTO (não do morador)
    qtd_carros_atual = repositorio.contar_carros_do_apartamento(id_apto_final)
    limite_vagas = apto_obj.vagas
    
    placa, modelo, cor = None, None, None
    cadastrar_carro = False
    
    if qtd_carros_atual >= limite_vagas:
        print(f"{Colors.RED}⛔ O Apartamento {apto_obj.rotulo} já atingiu o limite de {limite_vagas} veículos.{Colors.RESET}")
        print(f"{Colors.DIM}(Veículos atuais vinculados a esta unidade: {qtd_carros_atual}){Colors.RESET}")
        
        confirmar, _ = get_valid_input("Deseja continuar o cadastro SEM veículo? (s/n): ", validate_yes_no)
        if confirmar == 'n':
            return # Cancela tudo
    else:
        # Tem vaga sobrando
        print(f"{Colors.BLUE}ℹ Ocupação do Apto: {qtd_carros_atual}/{limite_vagas} vagas.{Colors.RESET}")
        cadastrar_carro = True
        
        placas_existentes = repositorio.listar_todas_placas()
        
        def validador_placa_unica(valor):
            val, erro = validate_placa(valor)
            if erro: return None, erro
            if val in placas_existentes: return None, f"A placa {val} já pertence a outro cadastro."
            return val, None

        placa, _ = get_valid_input("Placa do Veículo: ", validador_placa_unica)
        modelo = input("Modelo/Marca: ").strip().upper()
        cor = input("Cor: ").strip().upper()

    # =========================================================================
    # PASSO 4: PERSISTÊNCIA (Salvar Tudo)
    # =========================================================================
    print(f"\n{Colors.DIM}Salvando registros...{Colors.RESET}")
    
    try:
        # 1. Salva Morador (Vinculado ao ID do Apto)
        novo_morador = Morador(
            nome=nome, 
            cnh=cnh, 
            id_apartamento=id_apto_final # <--- FK Aqui
        )
        id_morador_gerado = repositorio.adicionar_morador(novo_morador)
        
        if not id_morador_gerado:
            raise ValueError("Falha ao gerar ID do morador.")

        # 2. Salva Veículo (Se aplicável)
        msg_veiculo = "\n  🚫 Sem veículo (Cota cheia ou não informado)"
        
        if cadastrar_carro and placa:
            novo_veiculo = Veiculo(
                placa=placa,
                modelo=modelo,
                cor=cor,
                morador_id=id_morador_gerado,
                estacionado=False
            )
            repositorio.adicionar_veiculo(novo_veiculo)
            msg_veiculo = f"\n   🚗 Veículo: {modelo} - {placa}"

        msg_final = (
            f"Cadastro Realizado!\n"
            f"   🏠 Unidade: {apto_obj.rotulo}\n"
            f"   👤 Morador: {nome}"
            f"{msg_veiculo}\n"
            f""
        )
        show_success(msg_final)
        
    except Exception as e:
        show_error(f"Erro ao salvar no banco de dados: {e}")