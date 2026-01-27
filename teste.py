"""
Script de Teste Rápido (Smoke Test).
Objetivo: Validar se a nova arquitetura (Apto -> Morador -> Carro) está gravando no banco.
"""
import os
from src.repositories.estacionamento_repository import EstacionamentoRepository
from src.classes.Apartamento import Apartamento
from src.classes.Morador import Morador
from src.classes.Veiculo import Veiculo

# Define um banco de teste para não sujar o oficial (opcional)
DB_PATH = "src/db/estacionamento_teste.db"

# Apaga o banco anterior para garantir teste limpo
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

print("🚀 INICIANDO TESTE DE BACKEND...\n")

try:
    # 1. Inicializa a Facade (Isso deve criar as tabelas)
    print("1. Criando Banco de Dados...", end=" ")
    with EstacionamentoRepository(DB_PATH) as repo:
        print("✅ OK")

        # 2. Testa Criar Apartamento
        print("2. Criando Apartamento 101...", end=" ")
        novo_apto = Apartamento(numero="101", bloco="A", vagas=2)
        id_apto = repo.criar_apartamento(novo_apto)
        
        if id_apto:
            print(f"✅ OK (ID: {id_apto})")
        else:
            print("❌ FALHA")
            exit()

        # 3. Testa Criar Morador (Vinculado ao ID do Apto)
        print("3. Criando Morador 'João'...", end=" ")
        novo_morador = Morador(nome="João Silva", cnh="12345678910", id_apartamento=id_apto)
        id_morador = repo.adicionar_morador(novo_morador)
        
        if id_morador:
            print(f"✅ OK (ID: {id_morador})")
        else:
            print("❌ FALHA")
            exit()

        # 4. Testa Criar Veículo (Vinculado ao Morador)
        print("4. Criando Veículo 'ABC-1234'...", end=" ")
        novo_veiculo = Veiculo(placa="ABC-1234", modelo="Fiat Uno", cor="Branco", morador_id=id_morador)
        repo.adicionar_veiculo(novo_veiculo)
        print("✅ OK")

        # 5. Testa a Lógica de Contagem (A Parte Crítica!)
        print("5. Testando Contagem de Vagas do Apto...", end=" ")
        qtd = repo.contar_carros_do_apartamento(id_apto)
        if qtd == 1:
            print(f"✅ SUCESSO! (Encontrou {qtd} carro)")
        else:
            print(f"❌ ERRO (Esperava 1, achou {qtd})")

        # 6. Testa Leitura Reversa (Do ID para o Texto)
        print("6. Testando Leitura de Dados...", end=" ")
        m = repo.buscar_morador_por_id(id_morador)
        a = repo.buscar_apartamento_por_id(m.id_apartamento)
        print(f"\n   -> Morador recuperado: {m.nome}")
        print(f"   -> Mora no: {a.rotulo}")
        print("✅ OK")

    print("\n🎉 CONCLUSÃO: O BACKEND ESTÁ SÓLIDO! PODE SEGUIR PARA O FRONT.")

except Exception as e:
    print(f"\n❌ ERRO CRÍTICO NO TESTE: {e}")