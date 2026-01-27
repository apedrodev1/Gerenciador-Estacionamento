"""
Funcionalidade: Edição de Moradores.
Permite alterar dados pessoais, MUDAR de apartamento e gerenciar a frota.
Localização: src/functions/moradores/crud/edicao.py
"""
from src.classes.Veiculo import Veiculo
from src.classes.Apartamento import Apartamento
from src.utils.input_handler import get_valid_input
from src.utils.validations import (
    validate_names, validate_cnh, validate_apartamento, validate_placa, validate_yes_no
)
from src.ui.colors import Colors
from src.ui.components import header, show_success, show_error, show_warning

from .helpers_morador import selecionar_morador

def editar_morador_form(repositorio):
    """Sub-menu de edição do morador selecionado."""
    
    # 1. Seleção (Já usa o helper novo com tradução de IDs)
    morador = selecionar_morador(repositorio)
    if not morador:
        return

    while True:
        # Recarrega dados frescos do banco
        morador = repositorio.buscar_morador_por_id(morador.id)
        
        # Busca objetos relacionados para exibir bonito
        apto_obj = repositorio.buscar_apartamento_por_id(morador.id_apartamento)
        veiculos = repositorio.listar_veiculos_por_morador(morador.id)
        
        rotulo_apto = apto_obj.rotulo if apto_obj else "---"
        
        # --- CABEÇALHO DO MENU ---
        header(f"EDITANDO: {morador.nome}")
        print(f"📄 CNH: {morador.cnh}")
        print(f"🏠 Unidade: {rotulo_apto} (Vagas: {apto_obj.vagas if apto_obj else '?'})")
        
        print(f"\n{Colors.BOLD}--- VEÍCULOS VINCULADOS ---{Colors.RESET}")
        if not veiculos:
            print(f"{Colors.YELLOW}Nenhum veículo cadastrado.{Colors.RESET}")
        else:
            for v in veiculos:
                status = f"{Colors.GREEN}[NO PÁTIO]{Colors.RESET}" if v.estacionado else "[FORA]"
                print(f"🚗 {v.placa:<8} | {v.modelo:<15} | {v.cor:<10} {status}")
        
        print("-" * 50)
        print("1. Alterar Nome")
        print("2. Alterar CNH")
        print("3. MUDAR de Apartamento")
        print("4. Adicionar Veículo")
        print("5. Remover Veículo")
        print("0. Voltar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == '0':
            break
            
        elif opcao == '1':
            _alterar_nome(repositorio, morador)

        elif opcao == '2':
            _alterar_cnh(repositorio, morador)

        elif opcao == '3':
            _mudar_apartamento(repositorio, morador)

        elif opcao == '4':
            _adicionar_veiculo_extra(repositorio, morador, apto_obj)
            
        elif opcao == '5':
            _remover_veiculo_existente(repositorio, veiculos)
            
        else:
            show_warning("Opção inválida!")

# --- FUNÇÕES AUXILIARES DE EDÇÃO ---

def _alterar_nome(repositorio, morador):
    novo_nome, _ = get_valid_input(f"Novo Nome ({morador.nome}): ", validate_names)
    morador.nome = novo_nome
    repositorio.atualizar_morador(morador)
    show_success("Nome atualizado!")

def _alterar_cnh(repositorio, morador):
    cnhs = repositorio.listar_todas_cnhs()
    def validador_cnh_edit(valor):
        val, erro = validate_cnh(valor)
        if erro: return None, erro
        # Permite manter a própria CNH atual, bloqueia duplicatas de outros
        if val in cnhs and val != morador.cnh: return None, "CNH já existente."
        return val, None
    
    nova_cnh, _ = get_valid_input(f"Nova CNH ({morador.cnh}): ", validador_cnh_edit)
    morador.cnh = nova_cnh
    repositorio.atualizar_morador(morador)
    show_success("CNH atualizada!")

def _mudar_apartamento(repositorio, morador):
    """
    Logica complexa: Buscar ou Criar novo apto e atualizar o ID no morador.
    """
    print(f"\n{Colors.BOLD}--- MUDANÇA DE ENDEREÇO ---{Colors.RESET}")
    num_novo, _ = get_valid_input("Novo Número: ", validate_apartamento)
    bloco_novo = input("Novo Bloco (opcional): ").strip().upper()
    
    # 1. Busca se já existe
    novo_apto_obj = repositorio.buscar_apartamento_por_rotulo(num_novo, bloco_novo)
    
    if novo_apto_obj:
        id_novo = novo_apto_obj.id
        print(f"ℹ Mudando para unidade existente: {novo_apto_obj.rotulo}")
    else:
        # 2. Se não existe, cria
        print(f"ℹ Unidade {num_novo} {bloco_novo} nova. Criando...")
        novo_apto = Apartamento(numero=num_novo, bloco=bloco_novo)
        id_novo = repositorio.criar_apartamento(novo_apto)
        if not id_novo:
            show_error("Erro ao criar nova unidade.")
            return

    # 3. Valida se a nova unidade comporta os carros que o morador JÁ TEM?
    # Isso seria uma regra de ouro avançada. Por enquanto, vamos permitir a mudança,
    # mas avisar se estourar a cota.
    
    # Atualiza o vínculo
    morador.id_apartamento = id_novo
    repositorio.atualizar_morador(morador)
    show_success(f"Morador transferido para {num_novo} {bloco_novo}!")

def _adicionar_veiculo_extra(repositorio, morador, apto_obj):
    """Adiciona carro respeitando o limite do APARTAMENTO."""
    print(f"\n{Colors.BOLD}--- ADICIONAR VEÍCULO ---{Colors.RESET}")
    
    if not apto_obj:
        show_error("Erro de inconsistência: Morador sem apartamento vinculado.")
        return

    # 1. Verifica Cota do Apto
    qtd_atual = repositorio.contar_carros_do_apartamento(apto_obj.id)
    limite = apto_obj.vagas
    
    if qtd_atual >= limite:
        show_warning(f"Limite do Apto {apto_obj.rotulo} atingido ({qtd_atual}/{limite}).")
        print("Não é possível adicionar mais veículos a esta unidade.")
        return

    # 2. Fluxo Normal
    placas_existentes = repositorio.listar_todas_placas()
    def validador_placa(valor):
        val, erro = validate_placa(valor)
        if erro: return None, erro
        if val in placas_existentes: return None, "Placa já cadastrada."
        return val, None

    placa, _ = get_valid_input("Placa: ", validador_placa)
    modelo = input("Modelo: ").strip().upper()
    cor = input("Cor: ").strip().upper()
    
    novo_veiculo = Veiculo(placa=placa, modelo=modelo, cor=cor, morador_id=morador.id)
    try:
        repositorio.adicionar_veiculo(novo_veiculo)
        show_success("Veículo adicionado!")
    except Exception as e:
        show_error(f"Erro ao adicionar: {e}")

def _remover_veiculo_existente(repositorio, lista_veiculos):
    if not lista_veiculos:
        show_warning("Nada para remover.")
        return

    placa_alvo = input("Digite a PLACA para remover: ").strip().upper()
    
    veiculo = next((v for v in lista_veiculos if v.placa == placa_alvo), None)
    
    if veiculo:
        confirmar, _ = get_valid_input(f"Confirma remover {placa_alvo}? (s/n): ", validate_yes_no)
        if confirmar == 's':
            repositorio.remover_veiculo(placa_alvo)
            show_success("Veículo removido.")
    else:
        show_error("Placa não encontrada nesta frota.")