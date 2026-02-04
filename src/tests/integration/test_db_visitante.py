import pytest
from datetime import datetime
from src.repositories.estacionamento_repository import EstacionamentoRepository
from src.classes.Visitante.Visitante import Visitante
from src.classes.Visitante.TicketVisitante import TicketVisitante
from src.classes.Veiculo import Veiculo

class TestIntegracaoVisitante:
    """
    Testa o fluxo de Visitantes, Veículos e o Vínculo com Tickets.
    """

    @pytest.fixture
    def repo(self):
        """Banco em memória, zerado e pronto."""
        repositorio = EstacionamentoRepository(":memory:")
        repositorio.__enter__()
        repositorio.common.criar_tabelas()
        yield repositorio
        repositorio.__exit__(None, None, None)

    def test_cadastrar_visitante_com_veiculo(self, repo):
        """Cenário: Cadastro simples de visitante com carro."""
        
        # 1. Cria Visitante
        vis = Visitante(nome="Visitante João", cnh="12345678900")
        id_vis = repo.visitantes.adicionar(vis)
        
        # 2. Cria Veículo vinculado
        # O sistema vai salvar como "ABC1234" (Sem hífen)
        carro = Veiculo(
            placa="ABC-1234", 
            modelo="Fiat Uno", 
            cor="Branco", 
            visitante_id=id_vis
        )
        repo.veiculos.adicionar(carro)
        
        # 3. Verificação
        # CORREÇÃO: Buscamos pela placa sanitizada (sem hífen), pois é assim que o banco guarda
        v_banco = repo.veiculos.buscar_por_placa("ABC1234")
        
        assert v_banco is not None
        assert v_banco.visitante_id == id_vis
        assert v_banco.placa == "ABC1234"

    def test_vinculo_automatico_ticket(self, repo):
        """
        💎 O GRANDE TESTE (Cenário do dia a dia).
        """
        placa_input = "TST-9999"   # O que o usuário digita
        placa_limpa = "TST9999"    # Como o banco salva (sem hífen)
        
        # 1. Carro entra (Ticket Avulso - Sem ID de visitante)
        ticket_avulso = TicketVisitante(
            placa=placa_input, 
            numero_vaga=10, 
            entrada=datetime.now(), 
            id_visitante=None
        )
        repo.tickets.criar_ticket(ticket_avulso)
        
        # CORREÇÃO: Buscamos pela placa limpa, pois é assim que está no banco
        ticket_antes = repo.tickets.buscar_ticket_ativo(placa_limpa)
        
        assert ticket_antes is not None # Agora ele deve encontrar!
        assert ticket_antes.id_visitante is None # Confirma que é avulso
        
        # 2. Faz o Cadastro da Pessoa
        novo_vis = Visitante(nome="Dono do Carro", cnh="11122233344")
        id_gerado = repo.visitantes.adicionar(novo_vis)
        
        # 3. Faz o Cadastro do Carro
        novo_carro = Veiculo(
            placa=placa_input, # Passamos com hífen, o sistema limpa sozinho
            modelo="Gol", 
            cor="Prata", 
            visitante_id=id_gerado
        )
        repo.veiculos.adicionar(novo_carro)
        
        # SIMULAÇÃO DA REGRA DE NEGÓCIO:
        if ticket_antes:
            # Vincula usando a placa correta (limpa)
            repo.tickets.vincular_cadastro_a_ticket(placa_limpa, id_gerado)
            
        # 4. Verificação Final
        ticket_depois = repo.tickets.buscar_ticket_ativo(placa_limpa)
        
        assert ticket_depois.id_visitante == id_gerado
        print("\n✅ Vínculo automático funcionou! O ticket agora tem dono.")

    def test_validar_placa_duplicada(self, repo):
        """Não pode ter dois carros com a mesma placa no sistema."""
        
        vis = Visitante(nome="João", cnh="11111111111")
        id_vis = repo.visitantes.adicionar(vis)
        
        c1 = Veiculo(placa="ABC-1010", modelo="A", cor="A", visitante_id=id_vis)
        repo.veiculos.adicionar(c1)
        
        # Tenta cadastrar a mesma placa de novo
        c2 = Veiculo(placa="ABC-1010", modelo="B", cor="B", visitante_id=id_vis)
        
        import sqlite3
        with pytest.raises(sqlite3.IntegrityError):
            repo.veiculos.adicionar(c2)