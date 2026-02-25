"""
Repositório de Funcionários.
Responsabilidade: CRUD completo de Funcionários (RH).
Localização: src/repositories/funcionario_repository.py
"""
import sqlite3
from src.repositories.base_repository import BaseRepository
from src.classes.Funcionario import Funcionario
from src.db import queries

class FuncionarioRepository(BaseRepository):

    def adicionar(self, funcionario: Funcionario) -> int:
        """
        Cadastra um novo funcionário.
        Retorna o ID gerado ou lança erro se CPF já existir.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute(queries.INSERT_FUNCIONARIO, (
                funcionario.nome,
                funcionario.cpf,  
                funcionario.cargo,
                funcionario.cnh,  
                funcionario.id_usuario 
            ))
            return cursor.lastrowid
            
        except sqlite3.IntegrityError:
            raise ValueError(f"Já existe um funcionário com o CPF {funcionario.cpf}.")
        except Exception as e:
            print(f"Erro ao adicionar funcionário: {e}")
            return None

    def listar(self) -> list[Funcionario]:
        """Retorna todos os funcionários do sistema."""
        cursor = self._get_cursor()
        lista = []
        try:
            cursor.execute(queries.SELECT_ALL_FUNCIONARIOS)
            for row in cursor.fetchall():
                lista.append(self._montar_objeto(row))
            return lista
        except Exception as e:
            print(f"Erro ao listar funcionários: {e}")
            return []

    def buscar_por_id(self, id_func: int) -> Funcionario:
        """Busca funcionário pelo ID."""
        cursor = self._get_cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE id = ?", (id_func,))
        row = cursor.fetchone()
        
        if row:
            return self._montar_objeto(row)
        return None

    def buscar_por_cpf(self, cpf: str) -> Funcionario:
        """Busca funcionário pelo CPF exato."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_FUNCIONARIO_BY_CPF, (cpf,))
        row = cursor.fetchone()
        
        if row:
            return self._montar_objeto(row)
        return None

    def atualizar(self, funcionario: Funcionario):
        """Atualiza dados cadastrais (CPF e CNH são imutáveis no banco)."""
        cursor = self._get_cursor()
        cursor.execute(queries.UPDATE_FUNCIONARIO, (
            funcionario.nome,
            funcionario.cargo,
            funcionario.id_usuario,
            funcionario.id 
        ))

    def remover(self, id_func: int):
        """
        Realiza a EXCLUSÃO FÍSICA.
        O 'ON DELETE CASCADE' do banco apagará automaticamente o veículo e a vaga da Zona C.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_FUNCIONARIO, (id_func,))

    def _montar_objeto(self, row) -> Funcionario:
        """Helper para converter tupla do banco em Objeto."""
        # Colunas SQL V3: id, nome, cpf, cargo, cnh, id_usuario
        return Funcionario(
            id=row[0],
            nome=row[1],
            cpf=row[2],
            cargo=row[3],
            cnh=row[4],
            id_usuario=row[5]
        )