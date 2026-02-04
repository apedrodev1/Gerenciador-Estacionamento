import getpass
import os
from src.repositories.estacionamento_repository import EstacionamentoRepository

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def realizar_login(repo: EstacionamentoRepository):
    """
    Exibe a tela de login e bloqueia o programa até obter sucesso.
    Retorna o objeto Usuario logado.
    """
    while True:
        limpar_tela()
        print("="*40)
        print("🔐  SISTEMA DE ESTACIONAMENTO - LOGIN")
        print("="*40)
        
        user = input("👤 Usuário: ").strip()
        senha = getpass.getpass("🔑 Senha:   ").strip()
        
        with repo:
            usuario_logado = repo.usuarios.autenticar(user, senha)
        
        if usuario_logado:
            print(f"\n✅ Bem-vindo, {usuario_logado.username}!")
            input("Pressione ENTER para entrar...")
            return usuario_logado
        
        print("\n❌ Usuário ou senha incorretos!")
        if input("Tentar novamente? (S/N): ").lower() == 'n':
            print("Saindo...")
            exit()