"""
Ponto de entrada principal.
Apenas inicializa e chama o menu UI.
"""
from dotenv import load_dotenv
from src.ui.auth import realizar_login
from src.utils.setup import inicializar_sistema
from src.ui.menu import executar_menu_principal 

# Carrega variáveis de ambiente
load_dotenv()

def main():
    # 1. Preparação (Setup do Banco e Classes)
    repo, estacionamento = inicializar_sistema()

    # 2. Segurança (Login)
    usuario_logado = realizar_login(repo)

    # 3. Execução (UI)
    executar_menu_principal(repo, estacionamento, usuario_logado)

if __name__ == "__main__":
    main()