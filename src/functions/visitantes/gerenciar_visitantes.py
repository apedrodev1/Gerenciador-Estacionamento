"""
Módulo de Gerenciamento de Visitantes Frequentes.
Permite cadastrar prestadores de serviço e parentes para agilizar a entrada.
Localização: src/functions/visitantes/gerenciar_visitantes.py
"""
from src.classes.Visitante.VisitanteCadastro import VisitanteCadastro
from src.utils.input_handler import get_valid_input
from src.utils.validations import (
    validate_names, validate_placa, validate_cnh, 
    validate_yes_no, validate_placa_unica, validate_cnh_unica
)
from src.ui.tables import criar_tabela
from src.ui.colors import Colors
from src.ui.components import header, menu_option, show_success, show_error, show_warning

# --- HELPER DE LISTAGEM ---

def _selecionar_visitante_cadastro(repositorio, acao_titulo="SELECIONAR", apenas_listar=False):
    """Exibe tabela de cadastros frequentes e permite seleção por ID."""
    cadastrados = repositorio.listar_visitantes_cadastrados()
    
    # Prepara dados para tabela Rich
    # Colunas: ID, Nome, Placa, Modelo, CNH
    dados = [
        [str(v.id), v.nome, v.placa, v.modelo, v.cnh]
        for v in cadastrados
    ]
    ids_validos = [v.id for v in cadastrados]

    titulo = "VISITANTES FREQUENTES" if apenas_listar else f"{acao_titulo} VISITANTE"
    criar_tabela(titulo, ["ID", "Nome", "Placa", "Modelo", "CNH"], dados)

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
            return next(v for v in cadastrados if v.id == int(id_str))
        show_warning("ID inválido.")

# --- AÇÕES CRUD ---

def adicionar_visitante_form(repositorio):
    header("NOVO VISITANTE FREQUENTE")
    print(f"{Colors.DIM}ℹ️  Este cadastro agiliza a entrada na portaria.{Colors.RESET}")
    
    # Validações de Unicidade
    print("⏳ Carregando validações...")
    placas_ocupadas = repositorio.listar_todas_placas()
    cnhs_ocupadas = repositorio.listar_todas_cnhs()
    
    nome, _ = get_valid_input("\nNome Completo: ", validate_names)
    placa, _ = get_valid_input("Placa: ", lambda x: validate_placa_unica(x, placas_ocupadas))
    cnh, _ = get_valid_input("CNH: ", lambda x: validate_cnh_unica(x, cnhs_ocupadas))
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")

    novo_visitante = VisitanteCadastro(
        nome=nome, placa=placa, cnh=cnh, modelo=modelo, cor=cor
    )

    try:
        repositorio.adicionar_visitante_cadastro(novo_visitante)
        show_success(f"Visitante {nome} cadastrado com sucesso!")
    except Exception as e:
        show_error(f"Erro ao salvar: {e}")

def editar_visitante_form(repositorio):
    visitante = _selecionar_visitante_cadastro(repositorio, acao_titulo="EDITAR")
    if not visitante: return

    while True:
        header(f"EDITANDO: {visitante.nome.upper()}")
        print(f"1. Nome:    {visitante.nome}")
        print(f"2. Placa:   {visitante.placa}")
        print(f"3. CNH:     {visitante.cnh}")
        print(f"4. Veículo: {visitante.modelo} / {visitante.cor}")
        print("-" * 40)
        menu_option("0", "💾 SALVAR E SAIR")
        
        opcao = input(f"\n{Colors.CYAN}Alterar campo: {Colors.RESET}").strip()

        if opcao == '0':
            try:
                repositorio.atualizar_visitante_cadastro(visitante)
                show_success("Dados atualizados!")
            except Exception as e: show_error(f"Erro: {e}")
            break
        
        elif opcao == '1': visitante.nome, _ = get_valid_input("Novo Nome: ", validate_names)
        elif opcao == '2': visitante.placa, _ = get_valid_input("Nova Placa: ", validate_placa)
        elif opcao == '3': visitante.cnh, _ = get_valid_input("Nova CNH: ", validate_cnh) 
        elif opcao == '4': 
            visitante.modelo = input("Novo Modelo: ")
            visitante.cor = input("Nova Cor: ")
        else:
            show_warning("Opção inválida.")

def remover_visitante_form(repositorio):
    visitante = _selecionar_visitante_cadastro(repositorio, acao_titulo="REMOVER")
    if not visitante: return 

    print(f"\n{Colors.RED}Remover cadastro de {visitante.nome} ({visitante.placa})?{Colors.RESET}")
    confirmar, _ = get_valid_input("Confirmar exclusão? (s/n): ", validate_yes_no)
    
    if confirmar == 's':
        try:
            repositorio.remover_visitante_cadastro(visitante.id)
            show_success("Cadastro removido.")
        except Exception as e:
            show_error(f"Erro ao remover: {e}")

# --- MENU PRINCIPAL INTERNO ---

def menu_gerenciar_visitantes(repositorio):
    while True:
        header("GESTÃO DE VISITANTES FREQUENTES ⭐")
        menu_option("1", "Cadastrar Novo Frequentador")
        menu_option("2", "Editar Cadastro")
        menu_option("3", "Remover Cadastro")
        menu_option("4", "Listar Todos")
        print("-" * 30)
        menu_option("0", "Voltar")
        
        opcao = input(f"\n{Colors.CYAN}➤ Opção: {Colors.RESET}").strip()
        
        if opcao == '1': adicionar_visitante_form(repositorio)
        elif opcao == '2': editar_visitante_form(repositorio)
        elif opcao == '3': remover_visitante_form(repositorio)
        elif opcao == '4': _selecionar_visitante_cadastro(repositorio, apenas_listar=True)
        elif opcao == '0': break