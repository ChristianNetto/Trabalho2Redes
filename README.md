# Trabalho 2 — Redes de Computadores 2

Professor: Alessandro Vivas Andrade.

Integrantes:

- Christian Netto Moura
- Marcio Antonio Ribeiro Junior

Implementação dos exercícios **1 a 4 e 10** de comunicação cliente-servidor com sockets TCP, UDP e WebSockets.
Os exercícios **5 a 9** contêm capturas reais de tráfego, screenshots do Wireshark e análises dos protocolos HTTP, TCP, DNS, ICMP e DHCP.
Requer Python **3.10 ou superior**, em Linux ou ambiente compatível.
Os exercícios 1 a 4 utilizam exclusivamente a biblioteca padrão. O exercício 10 utiliza `websockets`; a instalação está descrita no README da pasta.

| Exercício | Conteúdo | Instruções |
| --- | --- | --- |
| 1 | Cliente-servidor TCP com múltiplos clientes e confirmação | [README](exercicio1/README.md) |
| 2 | Echo UDP com limite de payload e timeout | [README](exercicio2/README.md) |
| 3 | Chat TCP com nickname, broadcast e threads | [README](exercicio3/README.md) |
| 4 | Hora via TCP, threads e contador protegido por Lock | [README](exercicio4/README.md) |
| 5 | Tráfego HTTP | [README](exercicio5/README.md) |
| 6 | Estabelecimento e encerramento TCP | [README](exercicio6/README.md) |
| 7 | Resolução de nomes via DNS | [README](exercicio7/README.md) |
| 8 | Tráfego ICMP (ping) e RTT | [README](exercicio8/README.md) |
| 9 | Negociação DHCP e etapas DORA | [README](exercicio9/README.md) |
| 10 | Chat WebSocket com nickname e broadcast | [README](exercicio10/README.md) |

Execute os comandos dos READMEs a partir da raiz deste repositório, iniciando o servidor antes dos clientes, em terminais separados.
Para executar em outra máquina, informe ao cliente o IP da máquina do servidor em `--host` e utilize a mesma `--porta` nos dois programas.
Os servidores escutam em `0.0.0.0` por padrão; os clientes usam `127.0.0.1` para testes na mesma máquina.
Encerre os servidores com `Ctrl+C`.
