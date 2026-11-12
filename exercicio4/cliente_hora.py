# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 4: cliente TCP que solicita e exibe a hora do servidor.

import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description="Cliente do servidor de hora TCP.")
    parser.add_argument("--host", default="127.0.0.1", help="Host do servidor (padrão: 127.0.0.1).")
    parser.add_argument("--porta", type=int, default=7000, help="Porta TCP (padrão: 7000).")
    args = parser.parse_args()

    try:
        # Conectar solicita a hora; o servidor encerra a conexão após responder.
        with socket.create_connection((args.host, args.porta), timeout=10) as cliente:
            partes = []
            while True:
                dados = cliente.recv(1024)
                if not dados:
                    break
                partes.append(dados)
            if partes:
                print(b"".join(partes).decode("utf-8"))
            else:
                print("O servidor encerrou a conexão sem enviar a hora.")
    except ConnectionRefusedError:
        print("Conexão recusada. Verifique se o servidor está em execução e confira host e porta.")
    except socket.timeout:
        print("Tempo limite ao conectar ou aguardar a hora.")
    except (OSError, UnicodeError, OverflowError) as erro:
        print(f"Erro de comunicação: {erro}")
    except KeyboardInterrupt:
        print("\nCliente encerrado.")


if __name__ == "__main__":
    main()
