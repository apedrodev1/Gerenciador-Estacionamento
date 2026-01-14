"""
Ponto de entrada principal.
Apenas inicializa e chama o menu UI.
"""
from dotenv import load_dotenv
from src.utils.setup import inicializar_sistema
from src.ui.menu import executar_menu_principal

# Carrega variáveis de ambiente
load_dotenv()

def main():
    # 1. Preparação (Setup)
    repo, estacionamento = inicializar_sistema()

    # 2. Execução (UI)
    executar_menu_principal(repo, estacionamento)

if __name__ == "__main__":
    main()