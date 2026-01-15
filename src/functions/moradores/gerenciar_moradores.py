"""
Módulo de Gerenciamento de Moradores.
Contém os fluxos de Cadastro, Edição, Remoção e Listagem.
Localização: src/functions/moradores/gerenciar_moradores.py
"""
from src.classes.Morador import Morador
from src.utils.input_handler import get_valid_input, clear_screen
from src.utils.validations import (
    validate_names, validate_placa, validate_cnh, validate_apartamento, 
    validate_yes_no, validate_placa_unica, validate_cnh_unica, validate_yes_no
)
from src.ui.tables import criar_tabela
from src.ui.colors import Colors
from src.ui.components import header, menu_option, show_success, show_error, show_warning

# --- HELPERS (Lógica Repetitiva) ---

def _solicitar_input_vaga(estacionamento):
    """
    Pede uma vaga fixa usando o padrão visual do sistema.
    Retorna: Inteiro (Vaga) ou None (Se não quiser/pular).
    """
    # 1. Validação Personalizada: Aceita 's', 'n' ou Vazio
    # Se vazio (''), retorna 'n' para simplificar a lógica abaixo.
    def validar_opcao_vaga(texto):
        if not texto.strip(): return 'n', None # Enter = Não
        return validate_yes_no(texto)

    # 2. Pergunta Inicial (Usa o input handler padrão)
    opcao, _ = get_valid_input(
        "\nAtribuir vaga fixa numérica? (s/n/Enter para pular): ", 
        validar_opcao_vaga
    )
    
    if opcao == 'n':
        return None

    # 3. Pergunta da Vaga (Usa input handler + validação do estacionamento)
    # Criamos um lambda para conectar a validação do objeto estacionamento ao input handler
    def validar_numero_vaga(texto):
        if not texto.isdigit(): 
            return None, "Digite apenas números inteiros."
        v_num = int(texto)
        sucesso, msg = estacionamento.validar_atribuicao_vaga_morador(v_num)
        if sucesso:
            return v_num, None
        return None, msg

    vaga_id, _ = get_valid_input(
        f"Número da Vaga (Acima de {estacionamento.capacidade_total}): ", 
        validar_numero_vaga
    )
    
    return vaga_id

def _selecionar_morador_da_lista(repositorio, acao_titulo="SELECIONAR", apenas_listar=False):
    """Mostra tabela e retorna o morador escolhido (ou None)."""
    moradores = repositorio.listar_moradores()
    
    dados = [
        [str(m.id), m.nome, m.apartamento, m.placa, 
         f"[cyan]{m.vaga_id}[/cyan]" if m.vaga_id else "[dim]Rotativa[/dim]"]
        for m in moradores
    ]
    ids_validos = [m.id for m in moradores]

    titulo = "LISTA DE MORADORES" if apenas_listar else f"{acao_titulo} MORADOR"
    criar_tabela(titulo, ["ID", "Nome", "Apto", "Placa", "Vaga Fixa"], dados)

    if not ids_validos:
        input(f"\n{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")
        return None

    if apenas_listar:
        input(f"\n{Colors.DIM}Pressione Enter para voltar ao menu...{Colors.RESET}")
        return None

    while True:
        id_str = input(f"\n{Colors.CYAN}Digite o ID (ou 0 para cancelar): {Colors.RESET}").strip()
        if id_str == '0': return None
        
        if id_str.isdigit() and int(id_str) in ids_validos:
            return next(m for m in moradores if m.id == int(id_str))
        show_warning("ID inválido ou não encontrado.")

# --- AÇÕES CRUD ---

def adicionar_morador_form(repositorio, estacionamento):
    header("NOVO CADASTRO DE MORADOR")
    
    # Carrega validações
    placas_ocupadas = repositorio.listar_todas_placas()
    cnhs_ocupadas = repositorio.listar_todas_cnhs()
    
    # Coleta dados
    print("\nPreencha os dados:")
    nome, _ = get_valid_input("Nome Completo: ", validate_names)
    apto, _ = get_valid_input("Apartamento: ", validate_apartamento)
    placa, _ = get_valid_input("Placa: ", lambda x: validate_placa_unica(x, placas_ocupadas))
    cnh, _ = get_valid_input("CNH: ", lambda x: validate_cnh_unica(x, cnhs_ocupadas))
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")

    # Usa o Helper de Vaga
    vaga_id = _solicitar_input_vaga(estacionamento)

    novo_morador = Morador(nome=nome, apartamento=apto, placa=placa, cnh=cnh, 
                           modelo=modelo, cor=cor, vaga_id=vaga_id)
    try:
        repositorio.adicionar_morador(novo_morador)
        show_success(f"Morador {nome} cadastrado com sucesso!")
    except Exception as e:
        show_error(f"Erro ao salvar: {e}")

def remover_morador_form(repositorio):
    morador = _selecionar_morador_da_lista(repositorio, acao_titulo="REMOVER")
    if not morador: return 

    print(f"\n{Colors.RED}{'!'*40}\n   CONFIRMAÇÃO: {morador.nome} (Apto {morador.apartamento})\n{'!'*40}{Colors.RESET}")
    
    confirmar, _ = get_valid_input("Deseja apagar este registro? (s/n): ", validate_yes_no)
    if confirmar == 's':
        try:
            repositorio.remover_morador(morador.id)
            show_success("Registro removido.")
        except Exception as e:
            show_error(f"Erro ao remover: {e}")

def editar_morador_form(repositorio, estacionamento):
    morador = _selecionar_morador_da_lista(repositorio, acao_titulo="EDITAR")
    if not morador: return

    while True:
        header(f"EDITANDO: {morador.nome.upper()}")
        print(f"1. Nome:        {morador.nome}")
        print(f"2. Apartamento: {morador.apartamento}")
        print(f"3. Placa:       {morador.placa}")
        print(f"4. CNH:         {morador.cnh}")
        print(f"5. Modelo/Cor:  {morador.modelo} / {morador.cor}")
        print(f"6. Vaga Fixa:   {morador.vaga_id if morador.vaga_id else 'Sem Vaga'}")
        print("-" * 40)
        menu_option("0", "💾 SALVAR E SAIR")
        
        opcao = input(f"\n{Colors.CYAN}Alterar campo: {Colors.RESET}").strip()

        if opcao == '0':
            try:
                repositorio.atualizar_morador(morador)
                show_success("Dados atualizados!")
            except Exception as e: show_error(f"Erro: {e}")
            break
        
        # Mapeamento simples de opções
        elif opcao == '1': morador.nome, _ = get_valid_input("Novo Nome: ", validate_names)
        elif opcao == '2': morador.apartamento, _ = get_valid_input("Novo Apto: ", validate_apartamento)
        elif opcao == '3': morador.placa, _ = get_valid_input("Nova Placa: ", validate_placa)
        elif opcao == '4': morador.cnh, _ = get_valid_input("Nova CNH: ", validate_cnh)
        elif opcao == '5': 
            morador.modelo = input("Novo Modelo: ")
            morador.cor = input("Nova Cor: ")
        elif opcao == '6':
            print(f"(Atual: {morador.vaga_id}) - Digite Enter para limpar a vaga.")
            morador.vaga_id = _solicitar_input_vaga(estacionamento)
        else:
            show_warning("Opção inválida.")

# --- MENU (Controller) ---

def menu_gerenciar_moradores(repositorio, estacionamento):
    """Sub-menu de gestão de moradores."""
    while True:
        header("GESTÃO DE MORADORES 🏘️")
        menu_option("1", "Adicionar Novo")
        menu_option("2", "Editar Cadastro")
        menu_option("3", "Remover")
        menu_option("4", "Listar Todos")
        print("-" * 30)
        menu_option("0", "Voltar")
        
        opcao = input(f"\n{Colors.CYAN}➤  Opção: {Colors.RESET}").strip()
        
        if opcao == '1': adicionar_morador_form(repositorio, estacionamento)
        elif opcao == '2': editar_morador_form(repositorio, estacionamento)
        elif opcao == '3': remover_morador_form(repositorio)
        elif opcao == '4': _selecionar_morador_da_lista(repositorio, apenas_listar=True)
        elif opcao == '0': break