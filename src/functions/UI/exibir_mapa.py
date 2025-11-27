from src.utils.input_handler import clear_screen

def exibir_mapa_estacionamento(repositorio):
    clear_screen()
    print("\n--- 🗺️  MAPA GERAL DO ESTACIONAMENTO ---")
    
    ocupacao = repositorio.listar_ocupacao_total()
    
    if not ocupacao:
        print("\n📭 O estacionamento está completamente vazio.")
        input("\nPressione Enter para voltar...")
        return

    # Cabeçalho
    print(f"{'VAGA':<6} {'TIPO':<10} {'PLACA':<10} {'MODELO/COR':<20} {'MOTORISTA'}")
    print("=" * 70)

    for item in ocupacao:
        # Formatação Visual
        icone = "👤" if item['tipo'] == 'Morador' else "🚗"
        
        # Monta a string do modelo/cor
        detalhes = f"{item['modelo']} {item['cor']}"
        if len(detalhes) > 20: detalhes = detalhes[:17] + "..."

        print(f"{item['vaga']:<6} {icone} {item['tipo']:<7} {item['placa']:<10} {detalhes:<20} {item['nome']}")

    print("=" * 70)
    print(f"Total de Veículos: {len(ocupacao)}")
    