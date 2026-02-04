import pytest
from src.repositories.estacionamento_repository import EstacionamentoRepository
from src.classes.Veiculo import Veiculo
from src.classes.Morador import Morador
from src.classes.Apartamento import Apartamento

class TestFluxoMovimentacao:
    """
    Testa a 'Vida Real' do estacionamento:
    Carros entrando, saindo e gerando histórico.
    """
    
    @pytest.fixture
    def repo(self):
        """Setup do banco em memória."""
        repositorio = EstacionamentoRepository(":memory:")
        repositorio.__enter__()
        repositorio.common.criar_tabelas()
        yield repositorio
        repositorio.__exit__(None, None, None)

    def test_movimentacao_morador(self, repo):
        """
        Cenário: Morador chega, estaciona (status=1) e depois sai (status=0).
        Verifica se o log de histórico foi criado.
        """
        # 1. Setup (Apartamento + Morador + Carro)
        apto = Apartamento(numero="100", bloco="A")
        repo.apartamentos.adicionar(apto)
        apto_db = repo.apartamentos.buscar_por_rotulo("100", "A")
        
        mor = Morador(nome="Morador Teste", cnh="11111111111", id_apartamento=apto_db.id)
        id_mor = repo.moradores.adicionar(mor)
        
        # Carro é criado com hífen, mas a classe limpa para "MOR1234"
        carro = Veiculo(placa="MOR-1234", modelo="Civic", cor="Preto", morador_id=id_mor)
        repo.veiculos.adicionar(carro)
        
        placa_correta = carro.placa 
        
        # 2. REALIZAR ENTRADA
        repo.veiculos.registrar_entrada(placa_correta, tipo_dono="MORADOR")
        
        # Verificação 1: Carro deve constar como Estacionado no banco
        v_dentro = repo.veiculos.buscar_por_placa(placa_correta)
        
        assert v_dentro is not None  
        assert v_dentro.estacionado is True
        
        # 3. REALIZAR SAÍDA
        repo.veiculos.registrar_saida(placa_correta, tipo_dono="MORADOR")
        
        # Verificação 2: Carro deve constar como Fora
        v_fora = repo.veiculos.buscar_por_placa(placa_correta)
        assert v_fora.estacionado is False
        
        # 4. Verificação de Histórico (Auditoria)
        logs = repo.common.buscar_historico_por_placa(placa_correta)
        
        assert len(logs) == 2
        assert logs[0][3] == "SAIDA"   # Último evento (Ordem decrescente)
        assert logs[1][3] == "ENTRADA" # Penúltimo evento
        
        print("\n✅ Fluxo de Movimentação e Histórico validado com sucesso!")