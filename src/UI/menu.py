"""
Gerenciador do Menu Principal (Interface).
Ponto central que integra todos os módulos do sistema.
Localização: src/ui/menu.py
"""
import getpass
from src.ui.components import header, menu_option, show_warning, clear_screen, Colors
from src.ui.mapa import exibir_mapa_estacionamento
from src.classes.Usuario import Usuario

# --- Imports dos Módulos Especialistas ---
from src.functions.catraca.controle_acesso import registrar_acesso_unificado
from src.functions.visitantes.catraca.listar_ativos import listar_visitantes_ativos
from src.functions.visitantes.menu_visitante import executar_menu_visitantes
from src.functions.moradores.menu_morador import executar_menu_moradores
from src.functions.relatorios.exibir_relatorios import menu_relatorios 

def exibir_dashboard_topo(estacionamento, repo, usuario):
    """Monta o cabeçalho dinâmico com estatísticas e nome do usuário."""
    
    # Busca contagem de tickets ativos (Visitantes no pátio)
    tickets_ativos = len(repo.listar_tickets_ativos())
    
    livres = estacionamento.capacidade_visitantes - tickets_ativos

    if livres <= 0:
        cor_status = Colors.RED
        texto_status = "LOTADO (Visitantes) ⛔"
    else:
        cor_status = Colors.GREEN
        texto_status = f"{livres} VAGAS LIVRES ✅"

    # Mostra quem está logado no subtítulo
    subtitulo = f"Status: {texto_status} | 👤 {usuario.username} ({usuario.perfil.upper()})"
    header(estacionamento.nome, subtitulo)

def criar_novo_usuario_sistema(repo):
    """Tela exclusiva de gerente para criar novos acessos."""
    clear_screen()
    header("NOVO USUÁRIO DO SISTEMA", "Acesso Restrito à Gerência")
    
    try:
        nome = input("👤 Novo Username: ").strip()
        if not nome: return
        
        senha = getpass.getpass("🔑 Nova Senha:   ").strip()
        print("\nPerfis Disponíveis: portaria | administrativo | gerencia")
        perfil = input("🛡️  Perfil: ").strip().lower()
        
        if perfil not in ['portaria', 'administrativo', 'gerencia']:
            show_warning("Perfil inválido! Cancelando...")
            return

        novo = Usuario(username=nome, senha_plana=senha, perfil=perfil)
        repo.usuarios.criar_usuario(novo)
        
        print(f"\n✅ Usuário '{nome}' criado com sucesso!")
        input("Pressione ENTER...")
        
    except Exception as e:
        show_warning(f"Erro ao criar usuário: {e}")

def executar_menu_principal(repo, estacionamento, usuario):
    """Loop principal da interface com controle de acesso."""
    
    with repo:
        while True:
            # 1. Desenha Cabeçalho (Agora com nome do usuário)
            exibir_dashboard_topo(estacionamento, repo, usuario)

            # 2. Desenha Opções (Filtradas por Perfil)
            
            # --- BLOCO 1: OPERAÇÃO (Todos veem) ---
            print(f"{Colors.BOLD} 🚧 OPERAÇÃO DIÁRIA (PORTARIA){Colors.RESET}")
            menu_option("1", "CATRACA (Entrada/Saída Rápida)") 
            menu_option("2", "Monitorar Pátio (Visitantes Ativos)")
            menu_option("5", "Mapa Visual do Estacionamento")
            print("")
            
            # --- BLOCO 2: GESTÃO (Apenas Admin/Gerente) ---
            if usuario.perfil in ['administrativo', 'gerencia']:
                print(f"{Colors.BOLD} 🏢 GESTÃO ADMINISTRATIVA{Colors.RESET}")
                menu_option("3", "Gestão de MORADORES & APARTAMENTOS") 
                menu_option("4", "Gestão de VISITANTES FREQUENTES") 
                menu_option("5", "Mapa Visual do Estacionamento")
                print("")
            
            # --- BLOCO 3: RELATÓRIOS (Apenas Admin/Gerente) ---
            if usuario.perfil in ['administrativo', 'gerencia']:
                print(f"{Colors.BOLD} 📊 AUDITORIA & RELATÓRIOS{Colors.RESET}")
                menu_option("5", "Mapa Visual do Estacionamento") 
                menu_option("6", "Relatórios e Histórico")
                print("-" * 50)
            
            # --- BLOCO 4: SISTEMA (Apenas Gerente) ---
            if usuario.perfil == 'gerencia':
                print(f"{Colors.BOLD} 🔐 ADMINISTRAÇÃO DO SISTEMA{Colors.RESET}")
                menu_option("9", "Criar Novo Usuário de Acesso")
                print("-" * 50)

            menu_option("0", "Sair")

            # 3. Captura Input
            opcao = input(f"\n{Colors.CYAN}➤  Navegar para: {Colors.RESET}").strip()

            # 4. Roteamento com Proteção
            if opcao == '1':
                registrar_acesso_unificado(repo, estacionamento)
            
            elif opcao == '2':
                listar_visitantes_ativos(repo)
            
            elif opcao == '3':
                if usuario.perfil == 'portaria': show_warning("Acesso Negado!"); continue
                executar_menu_moradores(repo)
                
            elif opcao == '4':
                if usuario.perfil == 'portaria': show_warning("Acesso Negado!"); continue
                executar_menu_visitantes(repo)
                
            elif opcao == '5':
                if usuario.perfil == 'portaria': show_warning("Acesso Negado!"); continue
                exibir_mapa_estacionamento(repo)
                
            elif opcao == '6':
                if usuario.perfil == 'portaria': show_warning("Acesso Negado!"); continue
                menu_relatorios(repo)
            
            elif opcao == '9':
                if usuario.perfil != 'gerencia': show_warning("Acesso Negado!"); continue
                criar_novo_usuario_sistema(repo)

            elif opcao == '0':
                clear_screen()
                print(f"\n{Colors.GREEN}👋 Sistema finalizado. Até a próxima!{Colors.RESET}")
                break
            
            else:
                show_warning("Opção desconhecida ou indisponível.")