"""
Módulo de Gerenciamento de Moradores.
Contém os fluxos de Cadastro, Edição, Remoção e Listagem.
Localização: src/functions/moradores/gerenciar_moradores.py
"""
from src.classes.Morador import Morador
from src.utils.input_handler import get_valid_input, clear_screen
from src.utils.validations import (
    validate_names, validate_placa, validate_cnh, validate_apartamento, 
    validate_yes_no, validate_placa_unica, validate_cnh_unica
)
# IMPORTS VISUAIS (Nova UI)
from src.ui.tables import criar_tabela
from src.ui.colors import Colors
from src.ui.components import header, menu_option, show_success, show_error, show_warning

# --- FUNÇÕES AUXILIARES (UI) ---

def _selecionar_morador_da_lista(repositorio, acao_titulo="SELECIONAR", apenas_listar=False):
    """
    Fluxo: Mostra Tabela Rich -> Pede ID (ou pausa se for apenas leitura).
    Retorna o Objeto Morador ou None.
    """
    moradores = repositorio.listar_moradores()

    # Prepara dados para a tabela
    dados_linhas = []
    ids_validos = []
    
    for m in moradores:
        ids_validos.append(m.id)
        
        # Formatação condicional: Destaca vaga se existir
        if m.vaga_id:
            vaga_fmt = f"[cyan]{m.vaga_id}[/cyan]"
        else:
            vaga_fmt = "[dim]Rotativa[/dim]"
            
        dados_linhas.append([
            str(m.id),
            m.nome,
            m.apartamento,
            m.placa,
            vaga_fmt
        ])

    # Desenha Tabela
    # Se for apenas listar, mudamos o título para ficar contextual
    titulo_final = "LISTA DE MORADORES" if apenas_listar else f"{acao_titulo} MORADOR"
    
    criar_tabela(
        titulo=titulo_final,
        colunas=["ID", "Nome", "Apto", "Placa", "Vaga Fixa"],
        linhas=dados_linhas
    )
    
    # Se não tiver ninguém, pausa e sai
    if not ids_validos:
        input(f"\n{Colors.DIM}Pressione Enter para voltar...{Colors.RESET}")
        return None

    # MODO LEITURA: Se for apenas listar, não pede ID, só pausa.
    if apenas_listar:
        input(f"\n{Colors.DIM}Pressione Enter para voltar ao menu...{Colors.RESET}")
        return None

    # MODO SELEÇÃO: Pede ID
    while True:
        id_str = input(f"\n{Colors.CYAN}Digite o ID do morador (ou 0 para cancelar): {Colors.RESET}").strip()

        if id_str == '0':
            return None

        if not id_str.isdigit():
            show_warning("Digite apenas números.")
            continue
        
        id_escolhido = int(id_str)

        if id_escolhido in ids_validos:
            return next(m for m in moradores if m.id == id_escolhido)
        else:
            show_warning("ID não encontrado na lista acima.")

# --- FORMULÁRIOS --- CRIAR UM ARQUIVO SEPARADO DEPOIS?

def adicionar_morador_form(repositorio, estacionamento):
    """Formulário para criar um novo morador."""
    header("NOVO CADASTRO DE MORADOR")
    
    print(f"{Colors.DIM}⏳ Carregando validações de segurança...{Colors.RESET}")
    placas_ocupadas = repositorio.listar_todas_placas()
    cnhs_ocupadas = repositorio.listar_todas_cnhs()
    
    print("\nPreencha os dados:")
    nome, _ = get_valid_input("Nome Completo: ", validate_names)
    apto, _ = get_valid_input("Apartamento: ", validate_apartamento)
    
    # Validação com Unicidade (Impede duplicatas)
    placa, _ = get_valid_input("Placa do Veículo: ", lambda x: validate_placa_unica(x, placas_ocupadas))
    cnh, _ = get_valid_input("CNH do Titular: ", lambda x: validate_cnh_unica(x, cnhs_ocupadas))
    
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")

    # Lógica de Vaga
    vaga_id = None
    print("-" * 30)
    
    while True:
        tem_vaga = input("Atribuir vaga fixa numérica agora? (s/n): ").lower().strip()
        if tem_vaga == 'n':
            break
        elif tem_vaga == 's':
            vaga_str = input(f"Número da Vaga (Acima de {estacionamento.capacidade_total}): ")
            if vaga_str.isdigit():
                v_num = int(vaga_str)
                valido, msg = estacionamento.validar_atribuicao_vaga_morador(v_num)
                if valido:
                    vaga_id = v_num
                    break
                else:
                    show_warning(msg)
            else:
                show_warning("Digite um número válido.")
        else:
            print("Responda apenas 's' ou 'n'.")

    novo_morador = Morador(
        nome=nome,
        apartamento=apto,
        placa=placa,
        cnh=cnh,
        modelo=modelo,
        cor=cor,
        vaga_id=vaga_id
    )

    try:
        repositorio.adicionar_morador(novo_morador)
        show_success(f"Morador {nome} (Apto {apto}) cadastrado com sucesso!")
    except Exception as e:
        show_error(f"Erro ao salvar no banco: {e}")

def remover_morador_form(repositorio):
    """Remove um morador usando o seletor visual."""
    morador_alvo = _selecionar_morador_da_lista(repositorio, acao_titulo="REMOVER")
    
    if not morador_alvo:
        return 

    # Confirmação Visual
    print("\n" + Colors.RED + "!"*50 + Colors.RESET)
    print(f"{Colors.BOLD}   CONFIRMAÇÃO DE EXCLUSÃO{Colors.RESET}")
    print(f"   👤 Nome:  {morador_alvo.nome}")
    print(f"   🏠 Apto:  {morador_alvo.apartamento}")
    print(f"   🚘 Placa: {morador_alvo.placa}")
    print(Colors.RED + "!"*50 + Colors.RESET)

    confirmar, _ = get_valid_input(f"\nTem certeza que deseja apagar este registro? (s/n): ", validate_yes_no)

    if confirmar == 's':
        try:
            repositorio.remover_morador(morador_alvo.id)
            show_success("Registro removido do sistema.")
        except Exception as e:
            show_error(f"Erro ao remover: {e}")
    else:
        print(f"\n{Colors.YELLOW}↩️  Operação cancelada.{Colors.RESET}")
        input("Pressione Enter...")

def editar_morador_form(repositorio, estacionamento):
    """Formulário para editar dados."""
    morador = _selecionar_morador_da_lista(repositorio, acao_titulo="EDITAR")
    
    if not morador:
        return

    while True:
        # Usa o Header padrão para limpar a tela
        header(f"EDITANDO: {morador.nome.upper()}")
        
        # Mostra o estado atual
        print(f"1. Nome:        {morador.nome}")
        print(f"2. Apartamento: {morador.apartamento}")
        print(f"3. Placa:       {morador.placa}")
        print(f"4. CNH:         {morador.cnh}")
        print(f"5. Modelo:      {morador.modelo}")
        print(f"6. Cor:         {morador.cor}")
        print(f"7. Vaga Fixa:   {morador.vaga_id if morador.vaga_id else 'Sem Vaga'}")
        print("-" * 40)
        menu_option("0", "💾 SALVAR E SAIR")
        
        opcao = input(f"\n{Colors.CYAN}O que deseja alterar? {Colors.RESET}").strip()

        if opcao == '0':
            try:
                repositorio.atualizar_morador(morador)
                show_success("Dados atualizados com sucesso!")
            except Exception as e:
                show_error(f"Erro ao salvar: {e}")
            break

        elif opcao == '1':
            morador.nome, _ = get_valid_input(f"Novo Nome: ", validate_names)
        elif opcao == '2':
            morador.apartamento, _ = get_valid_input(f"Novo Apto: ", validate_apartamento)
        elif opcao == '3':
            morador.placa, _ = get_valid_input(f"Nova Placa: ", validate_placa)
        elif opcao == '4':
            morador.cnh, _ = get_valid_input(f"Nova CNH: ", validate_cnh)
        elif opcao == '5':
            morador.modelo = input("Novo Modelo: ")
        elif opcao == '6':
            morador.cor = input("Nova Cor: ")
        elif opcao == '7':
             novo_v = input("Nova Vaga Numérica (ou Enter para limpar): ")
             if not novo_v:
                 morador.vaga_id = None
             elif novo_v.isdigit():
                 v_num = int(novo_v)
                 val, msg = estacionamento.validar_atribuicao_vaga_morador(v_num)
                 if val: 
                     morador.vaga_id = v_num
                 else: 
                     show_warning(msg)
             else:
                 show_warning("Digite um número válido.")

# --- MENU PRINCIPAL INTERNO ---

def menu_gerenciar_moradores(repositorio, estacionamento):
    """Sub-menu de gestão de moradores."""
    while True:
        header("GESTÃO DE MORADORES 🏘️")
        
        menu_option("1", "Adicionar Novo Morador")
        menu_option("2", "Editar Dados Cadastrais")
        menu_option("3", "Remover Morador")
        menu_option("4", "Listar Cadastro Completo")
        print("-" * 50)
        menu_option("0", "Voltar ao Menu Principal")
        
        opcao = input(f"\n{Colors.CYAN}➤ Escolha uma opção: {Colors.RESET}").strip()
        
        if opcao == '1':
            adicionar_morador_form(repositorio, estacionamento)
        elif opcao == '2':
            editar_morador_form(repositorio, estacionamento)
        elif opcao == '3':
            remover_morador_form(repositorio)
        elif opcao == '4':
            _selecionar_morador_da_lista(repositorio, acao_titulo="VISUALIZAR", apenas_listar=True)
        elif opcao == '0': 
            break
        else:
            show_warning("Opção inválida.")