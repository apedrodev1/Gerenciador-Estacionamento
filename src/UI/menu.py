"""
Gerenciador do Menu Principal (Interface).
Ponto central que integra todos os módulos do sistema.
Localização: src/ui/menu.py
"""
from src.ui.components import header, menu_option, show_warning, clear_screen, Colors
from src.ui.mapa import exibir_mapa_estacionamento

# --- Imports dos Módulos Especialistas ---

# 1. Catraca Unificada (Wrapper)
from src.functions.catraca.controle_acesso import registrar_acesso_unificado

# 2. Monitoramento
from src.functions.visitantes.catraca.listar_ativos import listar_visitantes_ativos

# 3. Gestão (CRUDs)
from src.functions.visitantes.menu_visitante import executar_menu_visitantes
from src.functions.moradores.menu_morador import executar_menu_moradores

# 4. Relatórios
from src.functions.relatorios.exibir_relatorios import menu_relatorios 


def exibir_dashboard_topo(estacionamento, repo):
    """Monta o cabeçalho dinâmico com estatísticas em tempo real."""
    
    # Busca contagem de tickets ativos (Visitantes no pátio)
    tickets_ativos = len(repo.listar_tickets_ativos())
    
    # CORREÇÃO AQUI: Usar o nome exato do atributo da sua classe Estacionamento
    # Antes estava: estacionamento.total_vagas_visitantes
    livres = estacionamento.capacidade_visitantes - tickets_ativos

    if livres <= 0:
        cor_status = Colors.RED
        texto_status = "LOTADO (Visitantes) ⛔"
    else:
        cor_status = Colors.GREEN
        texto_status = f"{livres} VAGAS LIVRES ✅"

    subtitulo = f"Status Pátio: {texto_status}"  # (possibilidade de correção) aqui podemos importar a classe Estacionamento e usar a propriedade Estacionamento.vagas_visitantes_disponiveis(self), mais simples eu acho / ou ajustar o .env. ver depois!
    header(estacionamento.nome, subtitulo)

def executar_menu_principal(repo, estacionamento):
    """Loop principal da interface."""
    
    # O 'with repo' garante que conexões sejam gerenciadas corretamente
    with repo:
        while True:
            # 1. Desenha Cabeçalho
            exibir_dashboard_topo(estacionamento, repo)

            # 2. Desenha Opções (Reorganizadas)
            
            print(f"{Colors.BOLD} 🚧 OPERAÇÃO DIÁRIA (PORTARIA){Colors.RESET}")
            menu_option("1", "CATRACA (Entrada/Saída Rápida)") 
            menu_option("2", "Monitorar Pátio (Visitantes Ativos)")
            print("")
            
            print(f"{Colors.BOLD} 🏢 GESTÃO ADMINISTRATIVA{Colors.RESET}")
            menu_option("3", "Gestão de MORADORES & APARTAMENTOS") 
            menu_option("4", "Gestão de VISITANTES") 
            print("")
            
            print(f"{Colors.BOLD} 📊 AUDITORIA & RELATÓRIOS{Colors.RESET}")
            menu_option("5", "Mapa Visual do Estacionamento") 
            menu_option("6", "Relatórios e Histórico")
            print("-" * 50)
            menu_option("0", "Sair")

            # 3. Captura Input
            opcao = input(f"\n{Colors.CYAN}➤ Navegar para: {Colors.RESET}").strip()

            # 4. Roteamento
            if opcao == '1':
                # O Wrapper Mágico que decide se é morador/visitante/entrada/saída
                registrar_acesso_unificado(repo, estacionamento)
            
            elif opcao == '2':
                listar_visitantes_ativos(repo)
            
            elif opcao == '3':
                executar_menu_moradores(repo)
                
            elif opcao == '4':
                executar_menu_visitantes(repo)
                
            elif opcao == '5':
                exibir_mapa_estacionamento(repo)
                
            elif opcao == '6':
                menu_relatorios(repo)
            
            elif opcao == '0':
                clear_screen()
                print(f"\n{Colors.GREEN}👋 Sistema finalizado. Até a próxima!{Colors.RESET}")
                break
            
            else:
                show_warning("Opção desconhecida.")