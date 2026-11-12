# Trabalho 2 — Redes de Computadores 2

Professor: Alessandro Vivas Andrade.

Integrantes:

- Christian Netto Moura
- Marcio Antonio Ribeiro Junior

Implementação dos exercícios **1 a 4** de comunicação cliente-servidor com sockets TCP e UDP.
Requer Python **3.10 ou superior**, em Linux ou ambiente compatível.
Todos os programas utilizam exclusivamente a biblioteca padrão; não há dependências para instalar com pip.

| Exercício | Conteúdo | Instruções |
| --- | --- | --- |
| 1 | Cliente-servidor TCP com múltiplos clientes e confirmação | [README](exercicio1/README.md) |
| 2 | Echo UDP com limite de payload e timeout | [README](exercicio2/README.md) |
| 3 | Chat TCP com nickname, broadcast e threads | [README](exercicio3/README.md) |
| 4 | Hora via TCP, threads e contador protegido por Lock | [README](exercicio4/README.md) |

Execute os comandos dos READMEs a partir da raiz deste repositório, iniciando o servidor antes dos clientes, em terminais separados.
Para executar em outra máquina, informe ao cliente o IP da máquina do servidor em `--host` e utilize a mesma `--porta` nos dois programas.
Os servidores escutam em `0.0.0.0` por padrão; os clientes usam `127.0.0.1` para testes na mesma máquina.
Encerre os servidores com `Ctrl+C`.
