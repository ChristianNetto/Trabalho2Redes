# Exercício 2 — Echo UDP

## Dependências

Python 3.10 ou superior. Somente biblioteca padrão (`socket` e `argparse`); não é necessário instalar pacotes com pip.

## Execução

Comandos a partir da raiz do repositório. No primeiro terminal:

```bash
python3 exercicio2/servidor_echo.py --host 0.0.0.0 --porta 6000
```

Em outro terminal:

```bash
python3 exercicio2/cliente_echo.py --host 127.0.0.1 --porta 6000 --timeout 5
```

`--host` define a interface de escuta no servidor ou o endereço de destino no cliente.
`--porta` define a porta UDP. `--timeout` é exclusivo do cliente e define a espera pela resposta em segundos, com valor positivo.
Os valores acima são os padrões. Para outra máquina, substitua `127.0.0.1` pelo IP do servidor.
No Windows, use `python` no lugar de `python3`, se esse for o comando da instalação.

## Funcionamento

O servidor imprime a mensagem e o IP/porta de origem e devolve exatamente os bytes recebidos, sem acrescentar prefixos ou quebras de linha ao datagrama.
O cliente exibe o eco e permite novos envios até `sair`. Mensagens vazias ou só com espaços são ignoradas.
O tamanho é verificado depois da codificação UTF-8: no máximo **65.507 bytes** de payload UDP/IPv4. Caracteres acentuados podem ocupar mais de um byte.
O timeout usa `socket.settimeout`: se uma resposta não chegar no prazo, o cliente avisa e permite outro envio.
Os sockets são fechados por context managers. Encerre o servidor com `Ctrl+C`.
