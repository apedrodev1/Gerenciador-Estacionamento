"""
Repositório de Usuários.
Responsabilidade: Gerenciar contas e Autenticação (Login).
Usa BCrypt para hashing de senhas.
Localização: src/repositories/usuario_repository.py
"""
import bcrypt
import sqlite3
from src.repositories.base_repository import BaseRepository
from src.db import queries
from src.classes.Usuario import Usuario

class UsuarioRepository(BaseRepository):
    
    def criar_usuario(self, usuario: Usuario):
        """
        Cria novo usuário, criptografando a senha antes de salvar.
        """
        if not usuario.senha_plana:
            raise ValueError("Senha é obrigatória para criação de usuário.")
            
        # 1. Criptografa a senha (Gera o Hash)
        # encode() converte string para bytes, necessário para o bcrypt
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(usuario.senha_plana.encode('utf-8'), salt)
        
        # 2. Salva no Banco
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.INSERT_USUARIO, (
                usuario.username,
                hash_bytes,  # Salvamos os bytes direto
                usuario.perfil
            ))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"O usuário '{usuario.username}' já existe.")
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return None

    def autenticar(self, username, senha_plana):
        """
        Verifica se o usuário e senha existem e batem.
        Retorna o objeto Usuario se OK, ou None se falhar.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_USUARIO_BY_USERNAME, (username,))
        row = cursor.fetchone()
        
        if not row:
            return None # Usuário não encontrado
            
        # Row: id, username, senha_hash, perfil
        id_db, user_db, hash_db, perfil_db = row
        
        # Verifica a senha usando bcrypt
        # checkpw compara a senha digitada (em bytes) com o hash do banco
        if bcrypt.checkpw(senha_plana.encode('utf-8'), hash_db):
            return Usuario(id=id_db, username=user_db, perfil=perfil_db, senha_hash=hash_db)
            
        return None # Senha incorreta

    def listar_todos(self):
        """Retorna lista de usuários (sem a senha/hash para segurança)."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_ALL_USUARIOS)
        lista = []
        for row in cursor.fetchall():
            # Row: id, username, perfil
            u = Usuario(id=row[0], username=row[1], perfil=row[2])
            lista.append(u)
        return lista

    def remover(self, id_usuario):
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_USUARIO, (id_usuario,))