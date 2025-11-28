from src.classes.Morador import Morador
from src.utils.input_handler import get_valid_input, clear_screen
from src.utils.validations import validate_names, validate_placa, validate_cnh, validate_apartamento, validate_yes_no

# --- FUNÇÕES AUXILIARES (UI) ---

def _renderizar_tabela(moradores):
    """
    Apenas desenha a tabela na tela. 
    Não pede input e não limpa a tela (para ser flexível).
    Retorna uma lista com os IDs válidos exibidos.
    """
    if not moradores:
        print("\n❌ Nenhum morador cadastrado.")
        return []

    # Cabeçalho da Tabela
    print(f"{'ID':<4} {'NOME':<20} {'APTO':<8} {'PLACA':<10} {'VAGA'}")
    print("-" * 60)

    ids_validos = []
    for m in moradores:
        ids_validos.append(m.id)
        vaga_info = m.vaga_id if m.vaga_id else "---"
        print(f"{m.id:<4} {m.nome:<20} {m.apartamento:<8} {m.placa:<10} {vaga_info}")
    print("-" * 60)
    
    return ids_validos

def _selecionar_morador_da_lista(repositorio, acao_titulo="SELECIONAR"):
    """
    Fluxo completo: Limpa tela -> Mostra Tabela -> Pede ID.
    Retorna o Objeto ou None.
    """
    clear_screen()
    moradores = repositorio.listar_moradores()

    print(f"\n--- 📋 {acao_titulo} MORADOR ---")
    
    # Usa a função auxiliar para desenhar (DRY)
    ids_validos = _renderizar_tabela(moradores)
    
    if not ids_validos:
        input("\nPressione Enter para voltar...")
        return None

    # Loop de Seleção (Só acontece se tiver moradores)
    while True:
        id_str = input("\nDigite o ID do morador (ou 0 para cancelar): ").strip()

        if id_str == '0':
            return None

        if not id_str.isdigit():
            print("❌ Por favor, digite um número válido.")
            continue
        
        id_escolhido = int(id_str)

        if id_escolhido in ids_validos:
            return next(m for m in moradores if m.id == id_escolhido)
        else:
            print("❌ ID não encontrado na lista acima. Tente novamente.")

# --- FORMULÁRIOS ---

def adicionar_morador_form(repositorio, estacionamento):
    """Formulário para criar um novo morador."""
    clear_screen()
    print("\n--- 🆕 NOVO MORADOR ---")
    
    nome, _ = get_valid_input("Nome: ", validate_names)
    apto, _ = get_valid_input("Apartamento: ", validate_apartamento)
    placa, _ = get_valid_input("Placa: ", validate_placa)
    cnh, _ = get_valid_input("CNH: ", validate_cnh)
    
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")
    
    while True:
        vaga_str = input(f"Número da Vaga Fixa (Acima de {estacionamento.capacidade_total} ou Enter para sem vaga): ")
        
        if not vaga_str: # Vazio = Sem vaga
            vaga_id = None
            break
            
        if not vaga_str.isdigit():
            print("❌ Digite apenas números.")
            continue
            
        vaga_id = int(vaga_str)

        valido, msg_erro = estacionamento.validar_atribuicao_vaga_morador(vaga_id)
        
        if valido:
            break
        else:
            print(f"❌ {msg_erro}")

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
        print(f"\n✅ Morador {nome} (Apto {apto}) cadastrado com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro ao salvar: {e}")
    
    input("\nPressione Enter para continuar...")

def remover_morador_form(repositorio):
    """Remove um morador usando o seletor visual."""
    
    # Usa o seletor (que já tem a lógica de input de ID)
    morador_alvo = _selecionar_morador_da_lista(repositorio, acao_titulo="REMOVER")
    
    if not morador_alvo:
        return 

    print("\n" + "!"*40)
    print(f"⚠️  ATENÇÃO: Você selecionou:")
    print(f"   Nome: {morador_alvo.nome}")
    print(f"   Apto: {morador_alvo.apartamento}")
    print(f"   Placa: {morador_alvo.placa}")
    print("!"*40)

    confirmar, _ = get_valid_input(f"\nDeseja MESMO remover este morador? (s/n): ", validate_yes_no)

    if confirmar == 's':
        try:
            repositorio.remover_morador(morador_alvo.id)
            print(f"\n🗑️  Morador {morador_alvo.nome} removido permanentemente.")
        except Exception as e:
            print(f"\n❌ Erro ao remover: {e}")
    else:
        print("\n↩️  Operação cancelada.")
    
    input("\nPressione Enter para continuar...")

# --- MENU PRINCIPAL ---

def menu_gerenciar_moradores(repositorio, estacionamento):
    """Menu Principal de Moradores."""
    while True:
        clear_screen()
        print("\n--- 🏘️  GESTÃO DE MORADORES ---")
        print("1. Adicionar Morador")
        print("2. Remover Morador")
        print("3. Listar Moradores (Visualizar)")
        print("0. Voltar ao Menu Principal (ou pressione Enter)") # UX Melhorada
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == '1':
            adicionar_morador_form(repositorio, estacionamento)
        
        elif opcao == '2':
            remover_morador_form(repositorio)
        
        elif opcao == '3':
            clear_screen()
            print("\n--- 📋 LISTA DE MORADORES ---")
            moradores = repositorio.listar_moradores()
            _renderizar_tabela(moradores)
            input("\nPressione Enter para voltar...")
        
        elif opcao == '0' or opcao == '': 
            break
        
        else:
            print("❌ Opção inválida.")
            