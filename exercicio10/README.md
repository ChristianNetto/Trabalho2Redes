# Exercício 10 — Chat em rede com WebSockets

## Dependências

Python 3.10 ou superior e a biblioteca `websockets`, fixada na versão 16.1.1 em `requirements.txt`.
Os comandos abaixo devem ser executados a partir da raiz do repositório, em Linux ou ambiente compatível.

```bash
python3 -m pip install -r exercicio10/requirements.txt
```

No Windows, use `python` no lugar de `python3`, se esse for o comando da instalação.

## Execução

Inicie o servidor no primeiro terminal:

```bash
python3 exercicio10/servidor_ws.py --host 0.0.0.0 --porta 8765
```

Em dois ou mais terminais, execute um cliente em cada um:

```bash
python3 exercicio10/cliente_ws.py --host 127.0.0.1 --porta 8765
```

- `--host`: interface de escuta no servidor (padrão `0.0.0.0`) ou endereço do servidor no cliente (padrão `127.0.0.1`).
- `--porta`: porta TCP do WebSocket, de 1 a 65535 (padrão `8765` nos dois programas).

Para conversar entre máquinas, informe no cliente o IP da máquina do servidor em `--host` e mantenha a mesma porta.

## Funcionamento

O cliente solicita um nickname não vazio. A primeira mensagem WebSocket enviada contém esse nickname; as seguintes são as mensagens do chat.
O servidor mantém as conexões ativas e faz broadcast no formato `[Nome]: mensagem` para **todos** os participantes identificados, incluindo quem enviou.
O cliente recebe mensagens em uma thread separada enquanto aguarda o teclado, permitindo comunicação em tempo real nos dois sentidos.

Mensagens vazias ou só com espaços são ignoradas. O protocolo aceita mensagens de texto; um nickname vazio ou o envio de dados binários encerra apenas a conexão inválida.
Digite `sair` para fechar seu cliente com o handshake de encerramento WebSocket. Encerre o servidor com `Ctrl+C`.
Conexões recusadas e desconexões inesperadas são tratadas. Se a conexão terminar enquanto o cliente aguarda o teclado, pressione Enter para sair.

## Testes

Depois de instalar a dependência:

```bash
python3 -m unittest discover -s exercicio10 -p "teste_*.py" -v
```

Os testes iniciam o servidor local em uma porta livre e usam conexões WebSocket reais para verificar broadcast incluindo o remetente, identificação por nickname, mensagens simultâneas, rejeição de entradas inválidas, desconexões normais e abruptas, conexão recusada e envio/recepção pelo cliente de terminal.
Usam `unittest` da biblioteca padrão, sem dependências adicionais.

APIs utilizadas: [servidor e broadcast](https://websockets.readthedocs.io/en/16.1.1/reference/asyncio/server.html) e [cliente com threads](https://websockets.readthedocs.io/en/16.1.1/reference/sync/client.html).
