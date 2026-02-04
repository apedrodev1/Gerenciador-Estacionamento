import pytest
import sqlite3
from src.repositories.estacionamento_repository import EstacionamentoRepository
from src.classes.Morador import Morador
from src.classes.Apartamento import Apartamento

class TestIntegracaoMorador:
    """
    Testa se o sistema consegue Salvar, Ler e Deletar no Banco de Dados (SQLite).
    Usa um banco em memória (:memory:) para não afetar o arquivo real.
    """

    @pytest.fixture
    def repo(self):
        """
        Cria um banco temporário e JÁ ABRE a conexão.
        Retorna o repositório pronto para uso.
        """
        # 1. Instancia
        repositorio = EstacionamentoRepository(":memory:")
        
        # 2. Abre Conexão (Simula o 'with repository:')
        repositorio.__enter__()
        
        # 3. Cria Tabelas
        repositorio.common.criar_tabelas()
        
        yield repositorio
        
        # 4. Fecha Conexão ao final do teste
        repositorio.__exit__(None, None, None)

    def test_criar_e_recuperar_morador(self, repo):
        """Cenário: Cadastrar um morador e ver se ele foi salvo."""
        
        # 1. Preparação - Usando Keyword Arguments para evitar confusão de ordem
        novo_apto = Apartamento(numero="101", bloco="A")
        repo.apartamentos.adicionar(novo_apto)
        
        apto_banco = repo.apartamentos.buscar_por_rotulo("101", "A")
        assert apto_banco is not None
        
        # 2. Ação
        novo_morador = Morador(
            nome="Teste da Silva", 
            cnh="12345678900", 
            id_apartamento=apto_banco.id
        )
        
        id_gerado = repo.moradores.adicionar(novo_morador)
        
        # 3. Verificação
        morador_recuperado = repo.moradores.buscar_por_id(id_gerado)
        
        assert morador_recuperado is not None
        assert morador_recuperado.nome == "Teste Da Silva"
        assert morador_recuperado.id_apartamento == apto_banco.id

    def test_impedir_morador_sem_apartamento(self, repo):
        """Cenário: Tentar cadastrar morador em apartamento inexistente (Integridade FK)."""
        
        morador_fantasma = Morador(
            nome="Fantasma", 
            cnh="99999999999", 
            id_apartamento=999
        )
        
        with pytest.raises(sqlite3.IntegrityError):
            repo.moradores.adicionar(morador_fantasma)

    def test_excluir_morador(self, repo):
        """Cenário: Cadastrar e depois excluir."""
        # Setup
        apto = Apartamento(numero="200", bloco="B")
        repo.apartamentos.adicionar(apto)
        apto_banco = repo.apartamentos.buscar_por_rotulo("200", "B")
        
        # CORREÇÃO: Usando argumentos nomeados aqui também!
        m = Morador(
            nome="Deletável", 
            cnh="11111111111", 
            id_apartamento=apto_banco.id
        )
        id_m = repo.moradores.adicionar(m)
        
        # Ação
        repo.moradores.remover(id_m)
        
        # Verificação
        busca = repo.moradores.buscar_por_id(id_m)
        assert busca is None