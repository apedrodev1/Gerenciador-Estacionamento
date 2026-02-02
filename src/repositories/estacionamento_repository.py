"""
FACADE REPOSITORY (O Gerente).
Responsabilidade: Ponto único de acesso ao Banco de Dados.
Inicializa os sub-repositórios especializados e gerencia a transação.
Localização: src/repositories/estacionamento_repository.py
"""
from src.utils.db_connection import DatabaseManager

# Importa os 6 Repositórios Especializados (Incluindo ApartamentoRepository)
from src.repositories.common_repository import CommonRepository
from src.repositories.apartamento_repository import ApartamentoRepository
from src.repositories.morador_repository import MoradorRepository
from src.repositories.visitante_repository import VisitanteRepository
from src.repositories.veiculo_repository import VeiculoRepository
from src.repositories.ticket_repository import TicketRepository

class EstacionamentoRepository:
    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)
        self.conn = None
        
        # --- Inicializa os Especialistas ---
        self.common = CommonRepository(self.db_manager)
        self.apartamentos = ApartamentoRepository(self.db_manager) # [NOVO]
        self.moradores = MoradorRepository(self.db_manager)
        self.visitantes = VisitanteRepository(self.db_manager)
        self.veiculos = VeiculoRepository(self.db_manager)
        self.tickets = TicketRepository(self.db_manager)
        
        # Garante que as tabelas existam (DDL)
        self.common.criar_tabelas()

    def __enter__(self):
        """Abre a conexão e distribui para todos os filhos."""
        self.conn = self.db_manager.__enter__()
        
        # Injeta a conexão ativa em todos
        self.common.set_connection(self.conn)
        self.apartamentos.set_connection(self.conn) # [NOVO]
        self.moradores.set_connection(self.conn)
        self.visitantes.set_connection(self.conn)
        self.veiculos.set_connection(self.conn)
        self.tickets.set_connection(self.conn)
        
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fecha a conexão e limpa os filhos."""
        self.db_manager.__exit__(exc_type, exc_val, exc_tb)
        self.conn = None
        
        # Remove a referência da conexão
        self.common.set_connection(None)
        self.apartamentos.set_connection(None)
        self.moradores.set_connection(None)
        self.visitantes.set_connection(None)
        self.veiculos.set_connection(None)
        self.tickets.set_connection(None)

    # =========================================================================
    # ÁREA DE DELEGAÇÃO (Fachada)
    # =========================================================================

    # --- 1. COMUM ---
    def listar_ocupacao_completa(self): return self.common.listar_ocupacao_completa()
    def listar_historico_recente(self): return self.common.listar_historico_recente()
    def listar_todas_cnhs(self): return self.common.listar_todas_cnhs()

    # --- 2. APARTAMENTOS (NOVO BLOCO) ---
    def criar_apartamento(self, apto): return self.apartamentos.adicionar(apto)
    def listar_apartamentos(self): return self.apartamentos.listar()
    def buscar_apartamento_por_rotulo(self, num, bloco=""): return self.apartamentos.buscar_por_rotulo(num, bloco)
    def buscar_apartamento_por_id(self, id): return self.apartamentos.buscar_por_id(id)

    # --- 3. MORADORES ---
    def adicionar_morador(self, m): return self.moradores.adicionar(m)
    def listar_moradores(self): return self.moradores.listar()
    def buscar_morador_por_id(self, id): return self.moradores.buscar_por_id(id)
    def atualizar_morador(self, m): return self.moradores.atualizar(m)
    def remover_morador(self, id): return self.moradores.remover(id)
    
    # Buscas Relacionadas a Apto (Atualizadas para usar ID)
    def buscar_moradores_por_id_apartamento(self, id_apto): 
        return self.moradores.buscar_por_id_apartamento(id_apto)
    
    def listar_ids_apartamentos_ocupados(self): 
        return self.moradores.listar_ids_apartamentos_ocupados()

    # --- 4. VISITANTES ---
    def adicionar_visitante_cadastro(self, v): return self.visitantes.adicionar(v)
    def listar_visitantes_cadastrados(self): return self.visitantes.listar()
    def buscar_visitante_por_id(self, id): return self.visitantes.buscar_por_id(id)
    def atualizar_visitante_cadastro(self, v): return self.visitantes.atualizar(v)
    def remover_visitante_cadastro(self, id): return self.visitantes.remover(id)

    # --- 5. VEÍCULOS ---
    def adicionar_veiculo(self, v): return self.veiculos.adicionar(v)
    def listar_veiculos_por_morador(self, id_morador): return self.veiculos.listar_por_morador(id_morador)
    def listar_veiculos_por_visitante(self, id_visitante): return self.veiculos.listar_por_visitante(id_visitante)
    def listar_todas_placas(self): return self.veiculos.listar_todas_placas()
    def buscar_veiculo_por_placa(self, placa): return self.veiculos.buscar_por_placa(placa)
    def buscar_historico_por_placa(self, placa):return self.common.buscar_historico_por_placa(placa)
    def contar_carros_do_apartamento(self, id_apartamento):return self.apartamentos.contar_vagas_ocupadas(id_apartamento)
    def atualizar_veiculo(self, v): return self.veiculos.atualizar(v)
    def remover_veiculo(self, placa): return self.veiculos.remover(placa)
    def registrar_entrada_veiculo(self, placa, tipo_dono): return self.veiculos.registrar_entrada(placa, tipo_dono)
    def registrar_saida_veiculo(self, placa, tipo_dono): return self.veiculos.registrar_saida(placa, tipo_dono)

    # --- 6. TICKETS ---
    def criar_ticket(self, t): return self.tickets.criar_ticket(t)
    def buscar_ticket_ativo(self, placa): return self.tickets.buscar_ticket_ativo(placa)
    def listar_tickets_ativos(self): return self.tickets.listar_tickets_ativos()
    def remover_ticket(self, id): return self.tickets.remover_ticket(id)
    def registrar_log_visitante(self, placa, evento): self.veiculos.registrar_log_visitante(placa, evento)
    def listar_vagas_ocupadas_tickets(self): return self.tickets.listar_vagas_ocupadas()
