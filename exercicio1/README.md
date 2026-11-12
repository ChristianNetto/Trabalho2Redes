# Exercício 1 — Cliente-servidor TCP

## Dependências

Python 3.10 ou superior. Somente biblioteca padrão (`socket`, `threading`, `argparse` e `datetime`); não é necessário instalar pacotes com pip.

## Execução

Comandos a partir da raiz do repositório. No primeiro terminal:

```bash
python3 exercicio1/servidor.py --host 0.0.0.0 --porta 5000
```

Em outro terminal, para cada cliente:

```bash
python3 exercicio1/cliente.py --host 127.0.0.1 --porta 5000
```

`--host` define a interface de escuta do servidor ou o endereço do servidor no cliente.
`--porta` define a porta TCP. Os valores acima são os padrões; para outra máquina, substitua `127.0.0.1` pelo IP do servidor.
No Windows, use `python` no lugar de `python3`, se esse for o comando da instalação.

## Funcionamento

O servidor atende cada conexão em uma thread, registra data/hora, IP, porta e mensagem, e responde `Mensagem recebida`.
O cliente envia mensagens continuamente e mostra uma confirmação por mensagem. Digite `sair` para desconectar; mensagens vazias ou só com espaços são ignoradas.
As mensagens usam UTF-8 e uma quebra de linha como delimitador, permitindo separar mensagens mesmo quando o TCP fragmenta ou agrupa os dados.
O cliente trata conexão recusada e possui timeout de 10 segundos para conexão e resposta. Os sockets são fechados por context managers, inclusive em caso de erro.
Encerre o servidor com `Ctrl+C`.
