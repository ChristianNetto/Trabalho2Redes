# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 1: cliente TCP com envio contínuo de mensagens.

import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="Cliente TCP.")
    parser.add_argument("--host", default="127.0.0.1", help="Host do servidor (padrão: 127.0.0.1).")
    parser.add_argument("--porta", type=int, default=5000, help="Porta TCP (padrão: 5000).")
    args = parser.parse_args()

    try:
        # O timeout evita espera indefinida pela conexão ou pela confirmação.
        with socket.create_connection((args.host, args.porta), timeout=10) as cliente:
            with cliente.makefile("r", encoding="utf-8") as entrada:
                while True:
                    mensagem = input("Mensagem (sair para encerrar): ")
                    if mensagem.strip().lower() == "sair":
                        break
                    if not mensagem.strip():
                        print("Digite uma mensagem não vazia.")
                        continue
                    cliente.sendall((mensagem + "\n").encode("utf-8"))
                    resposta = entrada.readline()
                    if not resposta:
                        print("O servidor encerrou a conexão.")
                        break
                    print(resposta.rstrip("\r\n"))
    except ConnectionRefusedError:
        print("Conexão recusada. Verifique se o servidor está em execução e confira host e porta.")
    except socket.timeout:
        print("Tempo limite ao conectar ou aguardar a resposta do servidor.")
    except (OSError, UnicodeError, OverflowError) as erro:
        print(f"Erro de comunicação: {erro}")
    except (KeyboardInterrupt, EOFError):
        print("\nCliente encerrado.")


if __name__ == "__main__":
    main()
