"""
Ações de CRUD (Create, Update, Delete) para Moradores.
Contém a lógica dos formulários.
"""
from src.classes.Morador import Morador
from src.utils.input_handler import get_valid_input
from src.utils.validations import (
    validate_names, validate_placa, validate_cnh, validate_apartamento,
    validate_yes_no, validate_placa_unica, validate_cnh_unica
)
from src.ui.colors import Colors
from src.ui.components import header, menu_option, show_success, show_error, show_warning
# Importa os helpers que acabamos de criar
from .helpers import solicitar_input_vaga, selecionar_morador_da_lista

def adicionar_morador_form(repositorio, estacionamento):
    header("NOVO CADASTRO DE MORADOR")
    
    placas_ocupadas = repositorio.listar_todas_placas()
    cnhs_ocupadas = repositorio.listar_todas_cnhs()
    
    print("\nPreencha os dados:")
    nome, _ = get_valid_input("Nome Completo: ", validate_names)
    apto, _ = get_valid_input("Apartamento: ", validate_apartamento)
    placa, _ = get_valid_input("Placa: ", lambda x: validate_placa_unica(x, placas_ocupadas))
    cnh, _ = get_valid_input("CNH: ", lambda x: validate_cnh_unica(x, cnhs_ocupadas))
    modelo = input("Modelo (opcional): ")
    cor = input("Cor (opcional): ")

    vaga_id = solicitar_input_vaga(estacionamento)

    novo_morador = Morador(nome=nome, apartamento=apto, placa=placa, cnh=cnh, 
                           modelo=modelo, cor=cor, vaga_id=vaga_id)
    try:
        repositorio.adicionar_morador(novo_morador)
        show_success(f"Morador {nome} cadastrado com sucesso!")
    except Exception as e:
        show_error(f"Erro ao salvar: {e}")

def remover_morador_form(repositorio):
    morador = selecionar_morador_da_lista(repositorio, acao_titulo="REMOVER")
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
    morador = selecionar_morador_da_lista(repositorio, acao_titulo="EDITAR")
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
        
        elif opcao == '1': morador.nome, _ = get_valid_input("Novo Nome: ", validate_names)
        elif opcao == '2': morador.apartamento, _ = get_valid_input("Novo Apto: ", validate_apartamento)
        elif opcao == '3': morador.placa, _ = get_valid_input("Nova Placa: ", validate_placa)
        elif opcao == '4': morador.cnh, _ = get_valid_input("Nova CNH: ", validate_cnh)
        elif opcao == '5': 
            morador.modelo = input("Novo Modelo: ")
            morador.cor = input("Nova Cor: ")
        elif opcao == '6':
            print(f"(Atual: {morador.vaga_id}) - Digite Enter para limpar a vaga.")
            morador.vaga_id = solicitar_input_vaga(estacionamento)
        else:
            show_warning("Opção inválida.")








