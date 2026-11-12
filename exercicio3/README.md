# Exercício 3 — Chat TCP

## Dependências

Python 3.10 ou superior. Somente biblioteca padrão (`socket`, `threading` e `argparse`); não é necessário instalar pacotes com pip.

## Execução

Comandos a partir da raiz do repositório. No primeiro terminal:

```bash
python3 exercicio3/servidor_chat.py --host 0.0.0.0 --porta 5001
```

Em dois ou mais terminais, execute um cliente em cada um:

```bash
python3 exercicio3/cliente_chat.py --host 127.0.0.1 --porta 5001
```

`--host` define a interface de escuta no servidor ou o endereço do servidor no cliente.
`--porta` define a porta TCP. Os valores acima são os padrões; para outra máquina, substitua `127.0.0.1` pelo IP do servidor.
No Windows, use `python` no lugar de `python3`, se esse for o comando da instalação.

## Funcionamento

Cada cliente solicita um nickname não vazio e envia mensagens enquanto uma thread separada recebe as mensagens da sala.
O servidor mantém uma thread por conexão e transmite cada mensagem para os outros clientes no formato `[Nome]: mensagem`.
Os participantes são notificados quando alguém entra ou sai. Digite `sair` para encerrar somente seu cliente; os demais continuam conectados.
Mensagens vazias ou só com espaços não são transmitidas. Desconexões inesperadas são tratadas e o cliente é removido da sala.
O cadastro de clientes e o envio a cada socket são protegidos por locks. O protocolo usa linhas UTF-8: a primeira contém o nickname; as seguintes contêm as mensagens.
Ao encerrar o cliente, `shutdown` interrompe a leitura da thread de recepção antes do fechamento do socket. Se o servidor encerrar enquanto o cliente aguarda o teclado, pressione Enter para sair.
Encerre o servidor com `Ctrl+C`.
