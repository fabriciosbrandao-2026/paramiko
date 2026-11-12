import conexao
import json

# Conectar-se ao equipamento R1 do inventário.
with open('inventario.json', 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

cliente = conexao.conectar(dados[0])

try:
    # Executar whoami, hostname, uptime -p e um comando inexistente.
    comandos = ["whoami", "hostname", "uptime -p", "damasceno"]

    # Exibir, para cada comando, o código de saída, a saída padrão e a saída de erro.
    for comando in comandos:
        codigo, saida, erro = conexao.executar(cliente, comando)
        print(f"Comando: {comando}")
        print(f"Código: {codigo}")
        print(f"Saída: {saida}")
        print(f"Erro: {erro}")
        print("========================================")
finally:
    cliente.close()