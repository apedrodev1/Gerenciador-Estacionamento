"""
Módulo de Queries SQL (Refatorado v2).
Reflete a arquitetura Relacional: Apartamento -> Morador -> Veículo.
"""

# ==============================================================================
# 1. CRIAÇÃO DE TABELAS (DDL)
# ==============================================================================

# [NOVO] Tabela Mestra de Unidades
CREATE_TABLE_APARTAMENTOS = """
CREATE TABLE IF NOT EXISTS apartamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL,
    bloco TEXT,
    vagas INTEGER DEFAULT 2,
    UNIQUE(numero, bloco)
);
"""

# [ALTERADO] Agora referencia a tabela apartamentos
CREATE_TABLE_MORADORES = """
CREATE TABLE IF NOT EXISTS moradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnh TEXT NOT NULL,
    id_apartamento INTEGER NOT NULL,
    FOREIGN KEY(id_apartamento) REFERENCES apartamentos(id) ON DELETE CASCADE
);
"""

# [MANTIDO] Tabela de Pessoas (Visitantes)
CREATE_TABLE_VISITANTES_CADASTRO = """
CREATE TABLE IF NOT EXISTS visitantes_cadastrados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cnh TEXT NOT NULL,
    data_cadastro TEXT
);
"""

# [MANTIDO] Tabela Central de Carros
CREATE_TABLE_VEICULOS = """
CREATE TABLE IF NOT EXISTS veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT UNIQUE NOT NULL,
    modelo TEXT,
    cor TEXT,
    estacionado INTEGER DEFAULT 0, -- 0=Fora, 1=Dentro
    morador_id INTEGER,
    visitante_id INTEGER,
    FOREIGN KEY(morador_id) REFERENCES moradores(id) ON DELETE CASCADE,
    FOREIGN KEY(visitante_id) REFERENCES visitantes_cadastrados(id) ON DELETE CASCADE
);
"""

# [MANTIDO] Tabela de Operação Rotativa
CREATE_TABLE_TICKETS = """
CREATE TABLE IF NOT EXISTS tickets_visitantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL,
    numero_vaga INTEGER,
    entrada TEXT NOT NULL,
    id_visitante INTEGER,
    FOREIGN KEY(id_visitante) REFERENCES visitantes_cadastrados(id)
);
"""

CREATE_TABLE_HISTORICO = """
CREATE TABLE IF NOT EXISTS historico_movimentacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT NOT NULL,
    placa TEXT NOT NULL,
    tipo_veiculo TEXT,  
    tipo_evento TEXT    
);
"""


# ==============================================================================
# 2. APARTAMENTOS (NOVO CRUD)
# ==============================================================================

INSERT_APARTAMENTO = "INSERT INTO apartamentos (numero, bloco, vagas) VALUES (?, ?, ?);"

SELECT_ALL_APARTAMENTOS = "SELECT * FROM apartamentos ORDER BY numero, bloco;"

SELECT_APARTAMENTO_BY_ID = "SELECT * FROM apartamentos WHERE id=?;"

# Busca composta para evitar duplicidade (Ex: Apto 101, Bloco A)
SELECT_APARTAMENTO_BY_NUM_BLOCO = "SELECT * FROM apartamentos WHERE numero=? AND bloco=?;"


# ==============================================================================
# 3. MORADORES (CRUD Atualizado)
# ==============================================================================

# Agora salvamos o ID do apartamento, não o número direto
INSERT_MORADOR = "INSERT INTO moradores (nome, cnh, id_apartamento) VALUES (?, ?, ?);"

# O SELECT simples retorna o ID. Se precisar do numero, o Python busca no objeto Apartamento ou fazemos JOIN.
SELECT_ALL_MORADORES = "SELECT * FROM moradores;"

SELECT_MORADOR_BY_ID = "SELECT * FROM moradores WHERE id = ?;"

# Busca moradores de um apartamento específico (Pelo ID do apto)
SELECT_MORADORES_BY_APTO_ID = "SELECT * FROM moradores WHERE id_apartamento = ?;"

UPDATE_MORADOR = "UPDATE moradores SET nome=?, cnh=?, id_apartamento=? WHERE id=?;"

DELETE_MORADOR = "DELETE FROM moradores WHERE id=?;"


# ==============================================================================
# 4. VISITANTES (CADASTRO PESSOA)
# ==============================================================================
INSERT_VISITANTE_CADASTRO = "INSERT INTO visitantes_cadastrados (nome, cnh, data_cadastro) VALUES (?, ?, ?);"
SELECT_ALL_VISITANTES = "SELECT * FROM visitantes_cadastrados ORDER BY nome;"
SELECT_VISITANTE_BY_ID = "SELECT * FROM visitantes_cadastrados WHERE id = ?;"
UPDATE_VISITANTE = "UPDATE visitantes_cadastrados SET nome=?, cnh=? WHERE id=?;"
DELETE_VISITANTE = "DELETE FROM visitantes_cadastrados WHERE id=?;"


# ==============================================================================
# 5. VEÍCULOS (CRUD + OPERAÇÃO)
# ==============================================================================
INSERT_VEICULO = """
INSERT INTO veiculos (placa, modelo, cor, morador_id, visitante_id, estacionado)
VALUES (?, ?, ?, ?, ?, ?);
"""
# Conta quantos veículos estão vinculados a moradores de um apto específico
SELECT_COUNT_VEICULOS_BY_APTO_ID = """
SELECT COUNT(*) 
FROM veiculos v
JOIN moradores m ON v.morador_id = m.id
WHERE m.id_apartamento = ?;
"""
SELECT_VEICULO_BY_PLACA = "SELECT * FROM veiculos WHERE placa = ?;"
SELECT_VEICULOS_BY_MORADOR_ID = "SELECT * FROM veiculos WHERE morador_id = ?;"
SELECT_VEICULOS_BY_VISITANTE_ID = "SELECT * FROM veiculos WHERE visitante_id = ?;"
SELECT_ALL_PLACAS = "SELECT placa FROM veiculos;"

UPDATE_VEICULO = "UPDATE veiculos SET modelo=?, cor=?, morador_id=?, visitante_id=? WHERE placa=?;"
DELETE_VEICULO = "DELETE FROM veiculos WHERE placa=?;"

# Catraca
SET_VEICULO_ESTACIONADO = "UPDATE veiculos SET estacionado = 1 WHERE placa = ?;"
SET_VEICULO_SAIDA = "UPDATE veiculos SET estacionado = 0 WHERE placa = ?;"


# ==============================================================================
# 6. TICKETS (CATRACA VISITANTE)
# ==============================================================================
INSERT_TICKET = "INSERT INTO tickets_visitantes (placa, numero_vaga, entrada, id_visitante) VALUES (?, ?, ?, ?);"
SELECT_TICKET_ATIVO = "SELECT * FROM tickets_visitantes WHERE placa = ?;"
SELECT_ALL_TICKETS = "SELECT * FROM tickets_visitantes;"
SELECT_VAGAS_OCUPADAS_VISITANTES = "SELECT numero_vaga FROM tickets_visitantes;"
DELETE_TICKET = "DELETE FROM tickets_visitantes WHERE id=?;"


# ==============================================================================
# 7. RELATÓRIOS E MAPA (SUPER QUERY COM JOIN)
# ==============================================================================

SELECT_OCUPACAO_COMPLETA = """
-- 1. Veículos de Moradores (Estacionados)
SELECT 
    'MORADOR' as tipo,              -- Coluna 0
    a.numero as apto_num,           -- Coluna 1
    a.bloco as apto_bloco,          -- Coluna 2
    NULL as vaga_visitante,         -- Coluna 3 (Vazio para morador)
    m.nome as proprietario,         -- Coluna 4
    v.placa,                        -- Coluna 5
    v.modelo,                       -- Coluna 6
    v.cor                           -- Coluna 7
FROM veiculos v
JOIN moradores m ON v.morador_id = m.id
JOIN apartamentos a ON m.id_apartamento = a.id
WHERE v.estacionado = 1

UNION ALL

-- 2. Visitantes (Tickets Ativos)
-- Agora fazemos JOIN com 'veiculos' para tentar achar a cor/modelo se existir cadastro
SELECT 
    'VISITANTE' as tipo,            -- Coluna 0
    NULL as apto_num,               -- Coluna 1 (Vazio para visitante)
    NULL as apto_bloco,             -- Coluna 2 (Vazio para visitante)
    t.numero_vaga as vaga_visitante,-- Coluna 3
    COALESCE(vc.nome, 'AVULSO') as proprietario, -- Coluna 4
    t.placa,                        -- Coluna 5
    COALESCE(v.modelo, '---') as modelo, -- Coluna 6 (Busca no carro, se não, ---)
    COALESCE(v.cor, '---') as cor        -- Coluna 7 (Busca no carro, se não, ---)
FROM tickets_visitantes t
LEFT JOIN visitantes_cadastrados vc ON t.id_visitante = vc.id
LEFT JOIN veiculos v ON t.placa = v.placa -- JOIN NOVO: Busca dados do carro pela placa
;
"""

# ==============================================================================
# 8. HISTÓRICO
# ==============================================================================
INSERT_HISTORICO = "INSERT INTO historico_movimentacao (data_hora, placa, tipo_veiculo, tipo_evento) VALUES (?, ?, ?, ?);"

SELECT_HISTORICO_RECENTE = """
    SELECT data_hora, placa, tipo_veiculo, tipo_evento 
    FROM historico_movimentacao 
    ORDER BY id DESC 
    LIMIT 50;
"""

SELECT_HISTORICO_BY_PLACA = """
    SELECT data_hora, placa, tipo_veiculo, tipo_evento 
    FROM historico_movimentacao 
    WHERE placa = ? 
    ORDER BY id DESC;
"""