"""
Funcionalidade: Edição de Visitantes Frequentes.
Permite alterar dados pessoais e gerenciar a frota (adicionar/remover carros).
Localização: src/functions/visitantes/crud/edicao.py
"""
from src.classes.Veiculo import Veiculo
from src.utils.input_handler import get_valid_input
from src.utils.validations import (
    validate_names, validate_cnh, validate_placa, validate_yes_no
)
from src.ui.colors import Colors
from src.ui.components import header, show_success, show_error, show_warning

from .helpers_visitante import selecionar_visitante

def editar_visitante_form(repositorio):
    """Sub-menu de edição do visitante selecionado."""
    
    # 1. Seleção
    visitante = selecionar_visitante(repositorio)
    if not visitante:
        return

    while True:
        # Recarrega dados frescos do banco (Pessoa)
        visitante = repositorio.buscar_visitante_por_id(visitante.id)
        
        # Busca Veículos vinculados a este visitante
        # (O Repositório precisa ter esse método implementado ou exposto)
        veiculos = repositorio.listar_veiculos_por_visitante(visitante.id)
        
        # --- CABEÇALHO DO MENU ---
        header(f"EDITANDO: {visitante.nome}")
        print(f"📄 CNH: {visitante.cnh}")
        print(f"📅 Desde: {visitante.data_cadastro.split('T')[0]}")
        
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
        print("3. Adicionar Veículo")
        print("4. Remover Veículo")
        print("0. Voltar")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == '0':
            break
            
        elif opcao == '1':
            _alterar_nome(repositorio, visitante)

        elif opcao == '2':
            _alterar_cnh(repositorio, visitante)

        elif opcao == '3':
            _adicionar_veiculo_visitante(repositorio, visitante)
            
        elif opcao == '4':
            _remover_veiculo_visitante(repositorio, veiculos)
            
        else:
            show_warning("Opção inválida!")

# --- FUNÇÕES AUXILIARES ---

def _alterar_nome(repositorio, visitante):
    novo_nome, _ = get_valid_input(f"Novo Nome ({visitante.nome}): ", validate_names)
    visitante.nome = novo_nome
    repositorio.atualizar_visitante_cadastro(visitante) # Verifique se o nome do método no repo é este
    show_success("Nome atualizado!")

def _alterar_cnh(repositorio, visitante):
    cnhs = repositorio.listar_todas_cnhs()
    def validador_cnh_edit(valor):
        val, erro = validate_cnh(valor)
        if erro: return None, erro
        if val in cnhs and val != visitante.cnh: return None, "CNH já existente."
        return val, None
    
    nova_cnh, _ = get_valid_input(f"Nova CNH ({visitante.cnh}): ", validador_cnh_edit)
    visitante.cnh = nova_cnh
    repositorio.atualizar_visitante_cadastro(visitante)
    show_success("CNH atualizada!")

def _adicionar_veiculo_visitante(repositorio, visitante):
    print(f"\n{Colors.BOLD}--- ADICIONAR VEÍCULO ---{Colors.RESET}")
    
    placas_existentes = repositorio.listar_todas_placas()
    
    def validador_placa(valor):
        val, erro = validate_placa(valor)
        if erro: return None, erro
        if val in placas_existentes: return None, "Placa já cadastrada."
        return val, None

    placa, _ = get_valid_input("Placa: ", validador_placa)
    modelo = input("Modelo: ").strip().upper()
    cor = input("Cor: ").strip().upper()
    
    # Cria veículo vinculado ao visitante_id
    novo_veiculo = Veiculo(
        placa=placa, 
        modelo=modelo, 
        cor=cor, 
        visitante_id=visitante.id, # VÍNCULO AQUI
        estacionado=False # Não ta passando, ou ta passando false, sem checar ver isso!
    )
    
    try:
        repositorio.adicionar_veiculo(novo_veiculo)
        show_success("Veículo adicionado!")
    except Exception as e:
        show_error(f"Erro ao adicionar: {e}")

def _remover_veiculo_visitante(repositorio, lista_veiculos):
    if not lista_veiculos:
        show_warning("Nada para remover.")
        return

    placa_alvo = input("Digite a PLACA para remover: ").strip().upper()
    
    # Busca na lista local (memória) pra ver se pertence a esse visitante
    veiculo = next((v for v in lista_veiculos if v.placa == placa_alvo), None)
    
    if veiculo:
        confirmar, _ = get_valid_input(f"Confirma remover {placa_alvo}? (s/n): ", validate_yes_no)
        if confirmar == 's':
            repositorio.remover_veiculo(placa_alvo)
            show_success("Veículo removido.")
    else:
        show_error("Placa não encontrada!")