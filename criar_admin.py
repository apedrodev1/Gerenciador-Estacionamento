"""
Script de Bootstrapping.
Rode APENAS UMA VEZ para criar o usuário administrador inicial.
"""
from src.repositories.estacionamento_repository import EstacionamentoRepository
from src.classes.Usuario import Usuario

def criar_admin():
    print("--- 🔐 CRIANDO USUÁRIO ADMIN ---")
    
    # CORREÇÃO: Passando o caminho do banco explicitamente
    repo = EstacionamentoRepository("src/db/estacionamento.db")
    
    with repo: # Abre conexão
        # Garante que a tabela existe
        repo.common.criar_tabelas()
        
        # Dados do Admin
        user = "admin"
        senha = "123" # Senha fraca só para teste inicial! Mude depois.
        
        try:
            # Tenta criar o usuário. Se já existir, vai cair no except.
            novo_admin = Usuario(username=user, senha_plana=senha, perfil="gerencia")
            repo.usuarios.criar_usuario(novo_admin)
            
            print(f"✅ Sucesso! Usuário: '{user}' / Senha: '{senha}' criado.")
            print("🚀 Agora você pode implementar a tela de login.")
            
        except ValueError as e:
            print(f"⚠️ Aviso: {e}")

if __name__ == "__main__":
    criar_admin()