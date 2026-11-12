import csv
import json
import conexao

# Lendo o arquivo JSON com o inventário
with open("inventario.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

comandos = ["whoami", "hostname", "uname -r", "uptime -p"]

with open("inventario_coletado.csv", "w", newline="", encoding="utf-8") as arquivo_csv:
    escritor = csv.writer(arquivo_csv)

    cabecalho = ["nome"] + comandos
    escritor.writerow(cabecalho)

    for maquina in dados:
        linha = [maquina["nome"]]
        
        try:
            cliente = conexao.conectar(maquina)
            print(f"Conectado em {maquina['nome']}")
            
            try:
                for comando in comandos:
                    codigo, saida, erro = conexao.executar(cliente, comando)
                    
                    if codigo == 0:
                        resultado = saida.strip()
                    else:
                        resultado = f"ERRO ({codigo}): {erro.strip()}"
                    
                    linha.append(resultado)
            finally:
                cliente.close()
                
        except Exception as e:
            print(f"Falha ao conectar em {maquina['nome']}: {e}")
            linha.extend([f"FALHA DE CONEXAO: {e}"] * len(comandos))

        escritor.writerow(linha)