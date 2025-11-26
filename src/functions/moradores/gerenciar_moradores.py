from src.classes.Morador import Morador
from src.utils.input_handler import get_valid_input, clear_screen
from src.utils.validations import validate_names, validate_placa, validate_cnh, validate_apartamento, validate_yes_no

# --- FUNÇÃO AUXILIAR (O SELETOR) ---

def _selecionar_morador_da_lista(repositorio, acao_titulo="SELECIONAR"):
    """
    Exibe a lista de moradores e pede para o usuário digitar um ID.
    Retorna: O objeto Morador selecionado ou None (se cancelar/lista vazia).
    """
    clear_screen()
    moradores = repositorio.listar_moradores()

    print(f"\n--- 📋 {acao_titulo} MORADOR ---")
    
    if not moradores:
        print("\n❌ Nenhum morador cadastrado para selecionar.")
        input("\nPressione Enter para voltar...")
        return None

    # Cabeçalho da Tabela
    print(f"{'ID':<4} {'NOME':<20} {'APTO':<8} {'PLACA':<10} {'VAGA'}")
    print("-" * 60)

    # Exibe as linhas
    ids_validos = []
    for m in moradores:
        ids_validos.append(m.id)
        vaga_info = m.vaga_id if m.vaga_id else "---"
        print(f"{m.id:<4} {m.nome:<20} {m.apartamento:<8} {m.placa:<10} {vaga_info}")
    print("-" * 60)

    # Loop de Seleção
    while True:
        id_str = input("\nDigite o ID do morador (ou 0 para cancelar): ").strip()

        if id_str == '0':
            return None

        if not id_str.isdigit():
            print("❌ Por favor, digite um número válido.")
            continue
        
        id_escolhido = int(id_str)

        if id_escolhido in ids_validos:
            # Retorna o objeto morador correspondente ao ID
            return next(m for m in moradores if m.id == id_escolhido)
        else:
            print("❌ ID não encontrado na lista acima. Tente novamente.")

# --- FORMULÁRIOS ---

def adicionar_morador_form(repositorio):
    """Formulário para criar um novo morador."""
    clear_screen()
    print("\n--- 🆕 NOVO MORADOR ---")
    
    nome, _ = get_valid_input("Nome: ", validate_names)
    apto, _ = get_valid_input("Apartamento: ", validate_apartamento)
    placa, _ = get_valid_input("Placa: ", validate_placa)
    cnh, _ = get_valid_input("CNH: ", validate_cnh)
    
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")
    
    vaga_str = input("Número da Vaga Fixa (ou Enter para sem vaga): ")
    vaga_id = int(vaga_str) if vaga_str.isdigit() else None

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
        input("\nPressione Enter para continuar...")
    except Exception as e:
        print(f"\n❌ Erro ao salvar: {e}")
        input("\nPressione Enter para continuar...")

def remover_morador_form(repositorio):
    """Remove um morador usando o seletor visual e confirmação detalhada."""
    
    # 1. Usa o seletor para pegar o objeto (já trata lista vazia e ID inválido)
    morador_alvo = _selecionar_morador_da_lista(repositorio, acao_titulo="REMOVER")
    
    if not morador_alvo:
        return # Usuário cancelou ou lista vazia

    # 2. Exibe o alerta detalhado (Sua solicitação)
    print("\n" + "!"*40)
    print(f"⚠️  ATENÇÃO: Você selecionou:")
    print(f"   Nome: {morador_alvo.nome}")
    print(f"   Apto: {morador_alvo.apartamento}")
    print(f"   Placa: {morador_alvo.placa}")
    print("!"*40)

    # 3. Confirmação Final
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

def menu_gerenciar_moradores(repositorio):
    """Menu Principal de Moradores."""
    while True:
        clear_screen()
        print("\n--- 🏘️  GESTÃO DE MORADORES ---")
        print("1. Adicionar Morador")
        print("2. Remover Morador")
        print("3. Listar Moradores (Visualizar)")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == '1':
            adicionar_morador_form(repositorio)
        elif opcao == '2':
            remover_morador_form(repositorio)
        elif opcao == '3':
            # Reutiliza o seletor apenas para visualização
            _selecionar_morador_da_lista(repositorio, acao_titulo="VISUALIZAR")
        elif opcao == '0':
            break
        else:
            print("❌ Opção inválida.")
            input("Enter...")