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
                funcionario.cpf,  # Já validado pelo Setter da classe
                funcionario.cargo,
                funcionario.cnh,  # Pode ser None
                funcionario.id_usuario # Pode ser None
            ))
            return cursor.lastrowid
            
        except sqlite3.IntegrityError:
            raise ValueError(f"Já existe um funcionário com o CPF {funcionario.cpf}.")
        except Exception as e:
            print(f"Erro ao adicionar funcionário: {e}")
            return None

    def listar(self) -> list[Funcionario]:
        """Retorna todos os funcionários ATIVOS."""
        cursor = self._get_cursor()
        cursor.execute(queries.SELECT_ALL_FUNCIONARIOS)
        
        lista = []
        for row in cursor.fetchall():
            lista.append(self._montar_objeto(row))
        return lista

    def buscar_por_id(self, id_func: int) -> Funcionario:
        """Busca funcionário pelo ID (mesmo inativos, se quiser mudar a query depois)."""
        # Nota: A query SELECT_ALL filtra ativos, mas buscar por ID geralmente queremos achar
        # mesmo se tiver demitido, para histórico.
        # Vamos usar uma query direta aqui para ser flexível.
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
        """Atualiza dados cadastrais."""
        cursor = self._get_cursor()
        cursor.execute(queries.UPDATE_FUNCIONARIO, (
            funcionario.nome,
            funcionario.cargo,
            funcionario.cnh,
            funcionario.id_usuario,
            funcionario.id # WHERE id = ?
        ))

    def remover(self, id_func: int):
        """
        Realiza a EXCLUSÃO LÓGICA (Demitir/Inativar).
        Não apaga o registro para manter histórico de quem liberou entradas antigas.
        """
        cursor = self._get_cursor()
        cursor.execute(queries.DELETE_FUNCIONARIO_LOGICO, (id_func,))

    def _montar_objeto(self, row) -> Funcionario:
        """Helper para converter tupla do banco em Objeto."""
        # Colunas: id, nome, cpf, cargo, cnh, ativo, id_usuario
        return Funcionario(
            id=row[0],
            nome=row[1],
            cpf=row[2],
            cargo=row[3],
            cnh=row[4],
            ativo=bool(row[5]),
            id_usuario=row[6]
        )