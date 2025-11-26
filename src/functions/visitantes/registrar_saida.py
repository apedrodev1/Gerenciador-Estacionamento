from src.utils.input_handler import get_valid_input
from src.utils.validations import validate_placa, validate_yes_no

def registrar_saida_visitante(estacionamento, repositorio):
    """
    Fluxo:
    1. Pede a placa.
    2. Busca o visitante na lista de ativos.
    3. Calcula tempo e mostra resumo.
    4. Remove do banco.
    """
    print("\n--- 🏁 Registrar Saída de Visitante ---")

    # 1. Pede a placa para buscar
    placa_busca, _ = get_valid_input("Digite a placa do veículo: ", validate_placa)

    # 2. Busca no Banco (Trazemos todos os ativos e filtramos no Python por simplicidade)
    # Em um sistema real com milhares de carros, faríamos uma query específica: "SELECT * FROM ... WHERE placa = ?"
    visitantes_ativos = repositorio.listar_visitantes_ativos()
    
    # Filtra a lista procurando a placa (case insensitive já tratado na validação)
    visitante_encontrado = None
    for v in visitantes_ativos:
        if v.placa == placa_busca:
            visitante_encontrado = v
            break
    
    if not visitante_encontrado:
        print(f"❌ Veículo com placa {placa_busca} não encontrado no pátio.")
        return

    # 3. Cálculos de Encerramento (Usando a Classe de Lógica)
    minutos_totais = estacionamento.calcular_tempo_permanencia(visitante_encontrado)
    horas = int(minutos_totais // 60)
    minutos = int(minutos_totais % 60)
    
    # Verifica vencimento (O Trigger visual de saída)
    venceu = estacionamento.verificar_ticket_vencido(visitante_encontrado)
    aviso_vencimento = "⚠️  TICKET VENCIDO! (Cobrar Multa)" if venceu else "✅ Dentro do limite"

    print("\n" + "="*40)
    print(f"RESUMO DA ESTADIA: {visitante_encontrado.nome}")
    print(f"Placa: {visitante_encontrado.placa}")
    print(f"Entrada: {visitante_encontrado.entrada.strftime('%d/%m %H:%M')}")
    print(f"Permanência: {horas}h {minutos}min")
    print(f"Status: {aviso_vencimento}")
    print("="*40 + "\n")

    # 4. Confirmação e Remoção
    confirmar, _ = get_valid_input("Confirmar saída e liberar vaga? (s/n): ", validate_yes_no)

    if confirmar == 's':
        try:
            repositorio.registrar_saida(visitante_encontrado.id)
            print(f"👋 Saída registrada. Vaga liberada.")
        except Exception as e:
            print(f"❌ Erro ao dar baixa no banco: {e}")
    else:
        print("Operação cancelada.")