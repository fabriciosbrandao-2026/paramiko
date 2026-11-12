# Comandos de teste por caso (bash do WSL, dentro de ~/projeto-redes/modulo-b)

Antes de tudo (em cada terminal novo):

    source ~/venv-redes/bin/activate
    export SSH_SENHA='Redes@2026'
    sudo service ssh start

## Caso 1
    python caso01_primeiro_comando.py
Esperado: whoami=r1, e `comando-inexistente` com codigo 127.

## Caso 2
    python caso02_coleta_em_lote.py && cat inventario_coletado.csv
Teste de falha: troque a porta de R3 no inventario.json para 2299, rode de novo e restaure.

## Caso 3
    ssh-keygen -t ed25519 -f ~/.ssh/id_redes -C "gerente-redes" -N ""
    for u in r1 r2 r3; do ssh-copy-id -i ~/.ssh/id_redes.pub $u@127.0.0.1; done
    sed -i "s|SEU_USUARIO|$USER|g" inventario_chave.json
    python caso03_chaves.py
(o script remove SSH_SENHA do proprio processo; o teste negativo aponta para chave inexistente)

## Caso 4
    python caso04_shell_interativo.py
Esperado: no invoke_shell, pwd=/tmp e $AMBIENTE=PRODUCAO; no exec_command, home e vazio.

## Caso 5
    python caso05_alteracao_segura.py
    python caso05_alteracao_segura.py      # idempotencia: rode duas vezes
    cat /home/r1/dispositivo.cfg           # deve haver UMA linha ntp_server=10.0.0.50

## Caso 6
    for i in 1 2 3 4 5 6 7; do python caso06_backup.py; sleep 1; done
    ls backups/R1 | wc -l      # deve ser 5
    cat backup.log

## Caso 7
    python caso07_distribuicao.py

## Caso 8 (provocar o desvio antes)
    sudo sed -i 's/^ntp_server=.*/ntp_server=10.0.0.50/' /home/r1/dispositivo.cfg /home/r2/dispositivo.cfg /home/r3/dispositivo.cfg
    sudo sed -i 's/^snmp_community=.*/snmp_community=privada-forte/' /home/r1/dispositivo.cfg /home/r3/dispositivo.cfg
    sudo sed -i 's/^snmp_community=.*/snmp_community=public/' /home/r2/dispositivo.cfg
    python caso08_auditoria.py
Esperado: R1 e R3 CONFORME, R2 NAO CONFORME.

## Caso 9
    python caso09_monitoramento.py
Alertas: troque LIMITE_DISCO para 1 e rode de novo. Carga:
    yes > /dev/null &   (2 ou 3 vezes)   ->  rode o script  ->  killall yes

## Caso 10
    sudo mkdir -p /run/sshd
    sudo /usr/sbin/sshd -p 2222
    python caso10_bastion.py

## Caso 11
    python caso11_resiliencia.py
Esperado: SAUDAVEL=OK, SENHA-ERRADA=AUTENTICACAO (1 tentativa), PORTA-FECHADA=CONEXAO RECUSADA (1 tentativa), SEM-RESPOSTA=TIMEOUT (3 tentativas).
