class Usuario:
    def __init__(self, username, senha_plana=None, perfil="portaria", id=None, senha_hash=None):
        """
        Representa um usuário do sistema.
        
        :param username: Login (ex: 'porteiro_joao')
        :param senha_plana: A senha digitada (ex: '123456'). Usada apenas na criação/login.
        :param perfil: Nível de acesso ('portaria', 'administrativo', 'gerencia').
        :param senha_hash: O hash criptografado (vêm do banco).
        """
        self.id = id
        self.username = username
        self.perfil = perfil
        
        # A lógica é: Ou temos a senha plana (para criar hash) ou já temos o hash (do banco)
        self.senha_plana = senha_plana 
        self.senha_hash = senha_hash

    def __str__(self):
        return f"👤 {self.username} [{self.perfil.upper()}]"