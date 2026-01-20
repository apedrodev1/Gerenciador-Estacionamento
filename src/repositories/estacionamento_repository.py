"""
FACADE REPOSITORY (O Gerente).
Ele inicializa os sub-repositórios e delega as chamadas.
"""
from src.utils.db_connection import DatabaseManager

# Importa os sub-repositórios
from src.repositories.common_repository import CommonRepository
from src.repositories.morador_repository import MoradorRepository
from src.repositories.visitante_repository import VisitanteRepository

class EstacionamentoRepository:
    def __init__(self, db_path: str):
        self.db_manager = DatabaseManager(db_path)
        self.conn = None
        
        # Inicializa os especialistas
        self.common = CommonRepository(self.db_manager)
        self.moradores = MoradorRepository(self.db_manager)
        self.visitantes = VisitanteRepository(self.db_manager)
        
        # Cria tabelas (Via Common)
        self.common.criar_tabelas()

    def __enter__(self):
        self.conn = self.db_manager.__enter__()
        # Passa a conexão ativa para todos os filhos
        self.common.set_connection(self.conn)
        self.moradores.set_connection(self.conn)
        self.visitantes.set_connection(self.conn)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_manager.__exit__(exc_type, exc_val, exc_tb)
        self.conn = None
        # Limpa conexão dos filhos
        self.common.set_connection(None)
        self.moradores.set_connection(None)
        self.visitantes.set_connection(None)

    # --- DELEGAÇÃO (MANTÉM COMPATIBILIDADE) ---
    
    # Comum
    def listar_todas_placas(self): return self.common.listar_todas_placas()
    def listar_todas_cnhs(self): return self.common.listar_todas_cnhs()
    def listar_ocupacao_total(self): return self.common.listar_ocupacao_total()

    # Moradores (Redireciona para self.moradores)
    def adicionar_morador(self, m): return self.moradores.adicionar(m)
    def listar_moradores(self): return self.moradores.listar()
    def contar_moradores_estacionados(self): return self.moradores.contar_moradores_estacionados()
    def buscar_morador_por_placa(self, p): return self.moradores.buscar_por_placa(p)
    def atualizar_morador(self, m): return self.moradores.atualizar(m)
    def remover_morador(self, id): return self.moradores.remover(id)
    def registrar_entrada_morador(self, p): return self.moradores.registrar_entrada(p)
    def registrar_saida_morador(self, p): return self.moradores.registrar_saida(p)

    # Visitantes Cadastro (Redireciona para self.visitantes)
    def adicionar_visitante_cadastro(self, v): return self.visitantes.adicionar_cadastro(v)
    def listar_visitantes_cadastrados(self): return self.visitantes.listar_cadastros()
    def buscar_visitante_cadastro_por_placa(self, p): return self.visitantes.buscar_cadastro_por_placa(p)
    def atualizar_visitante_cadastro(self, v): return self.visitantes.atualizar_cadastro(v)
    def remover_visitante_cadastro(self, id): return self.visitantes.remover_cadastro(id)

    # Visitantes Ativos (Redireciona para self.visitantes)
    def registrar_entrada(self, v): return self.visitantes.registrar_entrada(v)
    def registrar_saida(self, id): return self.visitantes.registrar_saida(id)
    def listar_visitantes_ativos(self): return self.visitantes.listar_ativos()
    def buscar_visitante_por_placa(self, p): return self.visitantes.buscar_ativos_por_placa(p)
    def buscar_vagas_ocupadas_visitantes(self): return self.visitantes.buscar_vagas_ocupadas()
    def contar_visitantes_ativos(self): return self.visitantes.contar_ativos()