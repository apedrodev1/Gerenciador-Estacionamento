"""
Gerenciador do Menu Principal (Interface).
Localização: src/ui/menu.py
"""
from src.ui.components import header, menu_option, show_warning, clear_screen, Colors
from src.ui.mapa import exibir_mapa_estacionamento

# Imports dos Controllers (Lógica)
from src.functions.moradores.catraca_moradores.entrada_morador import registrar_entrada_morador
from src.functions.moradores.catraca_moradores.saida_morador import registrar_saida_morador
from src.functions.moradores.gerenciar_moradores import menu_gerenciar_moradores
from src.functions.visitantes.catraca_visitantes.registrar_entrada import registrar_entrada_visitante
from src.functions.visitantes.catraca_visitantes.registrar_saida import registrar_saida_visitante
from src.functions.visitantes.listar_visitantes import listar_visitantes_ativos
from src.functions.visitantes.gerenciar_visitantes import menu_gerenciar_visitantes

def exibir_dashboard_topo(estacionamento, repo):
    """Monta o cabeçalho dinâmico."""
    # Atualiza contagem direto do banco
    estacionamento.ocupacao_atual = repo.contar_visitantes_ativos()
    
    ocupacao = estacionamento.ocupacao_atual
    total = estacionamento.capacidade_total
    livres = estacionamento.vagas_disponiveis

    if estacionamento.esta_lotado:
        cor_status = Colors.RED
        texto_status = "LOTADO ⛔"
    else:
        cor_status = Colors.GREEN
        texto_status = f"LIVRE ({livres} vagas) ✅"

    subtitulo = (
        f"Visitantes: {cor_status}{ocupacao}/{total}{Colors.RESET} | "
        f"Status: {texto_status}"
    )
    
    header(estacionamento.nome, subtitulo)

def executar_menu_principal(repo, estacionamento):
    """Loop principal da interface."""
    
    # O 'with repo' garante que conexões sejam abertas/fechadas corretamente
    with repo:
        while True:
            # 1. Desenha Cabeçalho
            exibir_dashboard_topo(estacionamento, repo)

            # 2. Desenha Opções
            print(f"{Colors.BOLD}   VISITANTES{Colors.RESET}")
            menu_option("1", "Registrar Entrada")
            menu_option("2", "Registrar Saída")
            menu_option("3", "Listar / Verificar Vencidos")
            menu_option("4", "Gerenciar Cadastros Frequentes") 
            print("")
            
            print(f"{Colors.BOLD}   MORADORES{Colors.RESET}")
            menu_option("5", "Entrada (Catraca)") 
            menu_option("6", "Saída (Catraca)")   
            menu_option("7", "Gerenciar Cadastros") 
            print("")
            
            print(f"{Colors.BOLD}   SISTEMA{Colors.RESET}")
            menu_option("8", "Mapa Geral do Pátio") 
            print("-" * 50)
            menu_option("0", "Sair")

            # 3. Captura Input
            opcao = input(f"\n{Colors.CYAN}➤ Navegar para: {Colors.RESET}").strip()

            # 4. Roteamento
            if opcao == '1':
                registrar_entrada_visitante(estacionamento, repo)
            elif opcao == '2':
                registrar_saida_visitante(estacionamento, repo)
            elif opcao == '3':
                listar_visitantes_ativos(estacionamento, repo)
            elif opcao == '4':
                menu_gerenciar_visitantes(repo) 
            
            elif opcao == '5':
                registrar_entrada_morador(repo)
            elif opcao == '6':
                registrar_saida_morador(repo)
            elif opcao == '7':
                menu_gerenciar_moradores(repo, estacionamento)
            
            elif opcao == '8':
                exibir_mapa_estacionamento(repo)
            
            elif opcao == '0':
                clear_screen()
                print(f"\n{Colors.GREEN}👋 Sistema finalizado. Até a próxima!{Colors.RESET}")
                break
            
            else:
                show_warning("Opção desconhecida.")