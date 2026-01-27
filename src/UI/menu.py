"""
Gerenciador do Menu Principal (Interface).
Localização: src/ui/menu.py
"""
from src.ui.components import header, menu_option, show_warning, clear_screen, Colors
from src.ui.mapa import exibir_mapa_estacionamento
from src.functions.relatorios.exibir_relatorios import menu_relatorios

# Imports dos Controllers (Lógica)
from src.functions.moradores.catraca.entrada_morador import registrar_entrada_morador
from src.functions.moradores.catraca.saida_morador import registrar_saida_morador
from src.functions.moradores.menu_morador import executar_menu_moradores
from src.functions.visitantes.catraca_visitantes.registrar_entrada import registrar_entrada_visitante
from src.functions.visitantes.catraca_visitantes.registrar_saida import registrar_saida_visitante
from src.functions.visitantes.gerenciar_visitantes import menu_gerenciar_visitantes
from src.functions.visitantes.listar_visitantes import listar_visitantes_ativos

def exibir_dashboard_topo(estacionamento, repo):
    """Monta o cabeçalho dinâmico com duas barras e alertas."""
    
    # 1. Coleta de Dados
    qtd_visitantes = repo.contar_visitantes_ativos()
    qtd_moradores = repo.contar_moradores_estacionados()
    
    # Verifica Tickets Vencidos
    visitantes_ativos = repo.listar_visitantes_ativos()
    tickets_vencidos = sum(1 for v in visitantes_ativos if estacionamento.verificar_ticket_vencido(v))

    # 2. Cálculos de Capacidade
    cap_visitantes = estacionamento.capacidade_visitantes # Ex: 20
    cap_moradores = estacionamento.capacidade_total - cap_visitantes # Ex: 100 - 20 = 80
    
    livres_visitantes = cap_visitantes - qtd_visitantes
    
    # 3. Gerador de Barra Visual (Função Auxiliar)
    def gerar_barra(atual, total, cor_preenchida):
        tamanho_barra = 15 # Caracteres
        if total == 0: total = 1 # Evita divisão por zero
        percentual = min(atual / total, 1.0)
        chars_cheios = int(percentual * tamanho_barra)
        chars_vazios = tamanho_barra - chars_cheios
        return f"{cor_preenchida}{'█' * chars_cheios}{Colors.RESET}{Colors.DIM}{'░' * chars_vazios}{Colors.RESET}"

    # Barra Visitantes (Verde/Vermelha)
    cor_vis = Colors.RED if livres_visitantes == 0 else Colors.GREEN
    barra_vis = gerar_barra(qtd_visitantes, cap_visitantes, cor_vis)
    
    # Barra Moradores (Azul)
    barra_mor = gerar_barra(qtd_moradores, cap_moradores, Colors.CYAN)

    # 4. Montagem do Texto
    linha_visitantes = f"VISITANTES: {barra_vis} {qtd_visitantes}/{cap_visitantes}"
    linha_moradores  = f"MORADORES:  {barra_mor} {qtd_moradores}/{cap_moradores}"
    
    # Status Geral
    if tickets_vencidos > 0:
        status_extra = f" | {Colors.RED}⚠ {tickets_vencidos} VENCIDO(S){Colors.RESET}"
    else:
        status_extra = f" | {Colors.GREEN}Tickets OK{Colors.RESET}"

    subtitulo = (
        f"{linha_visitantes}\n"
        f"{linha_moradores}{status_extra}"
    )
    
    header(estacionamento.nome, subtitulo)

def executar_menu_principal(repo, estacionamento):
    """Loop principal da interface."""
    with repo:
        while True:
            exibir_dashboard_topo(estacionamento, repo)

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
            menu_option("9", "Relatórios e Auditoria")
            print("-" * 50)
            menu_option("0", "Sair")

            opcao = input(f"\n{Colors.CYAN}➤ Navegar para: {Colors.RESET}").strip()

            if opcao == '1': registrar_entrada_visitante(estacionamento, repo)
            elif opcao == '2': registrar_saida_visitante(estacionamento, repo)
            elif opcao == '3': listar_visitantes_ativos(estacionamento, repo)
            elif opcao == '4': menu_gerenciar_visitantes(repo) 
            elif opcao == '5': registrar_entrada_morador(repo, estacionamento)
            elif opcao == '6': registrar_saida_morador(repo)
            elif opcao == '7': menu_gerenciar_moradores(repo, estacionamento)
            elif opcao == '8': exibir_mapa_estacionamento(repo)
            elif opcao == '9': menu_relatorios(repo)
            elif opcao == '0':
                clear_screen()
                print(f"\n{Colors.GREEN}👋 Sistema finalizado. Até a próxima!{Colors.RESET}")
                break
            else:
                show_warning("Opção desconhecida.")