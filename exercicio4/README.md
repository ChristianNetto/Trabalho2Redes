# Exercício 4 — Servidor de hora com threads

## Dependências

Python 3.10 ou superior. Somente biblioteca padrão (`socket`, `threading`, `argparse` e `datetime`); não é necessário instalar pacotes com pip.

## Execução

Comandos a partir da raiz do repositório. No primeiro terminal:

```bash
python3 exercicio4/servidor_hora.py --host 0.0.0.0 --porta 7000
```

Em outro terminal:

```bash
python3 exercicio4/cliente_hora.py --host 127.0.0.1 --porta 7000
```

`--host` define a interface de escuta no servidor ou o endereço do servidor no cliente.
`--porta` define a porta TCP. Os valores acima são os padrões; para outra máquina, substitua `127.0.0.1` pelo IP do servidor.
No Windows, use `python` no lugar de `python3`, se esse for o comando da instalação.

## Funcionamento

A abertura da conexão solicita a hora. O servidor responde com a hora local da máquina no formato `HH:MM:SS` e fecha a conexão.
O cliente recebe toda a resposta, mostra a hora no console e desconecta. Possui timeout de 10 segundos e trata conexão recusada.
Cada conexão é atendida em uma thread. Após enviar a hora, o servidor incrementa o total de clientes atendidos e registra data/hora, IP/porta e contador acumulado.
O incremento e seu log são protegidos por `threading.Lock`, evitando alterações simultâneas no contador, que começa em zero a cada inicialização.
Erros de conexão são tratados na thread correspondente, mantendo o servidor em funcionamento para os outros clientes.
Encerre o servidor com `Ctrl+C`.
