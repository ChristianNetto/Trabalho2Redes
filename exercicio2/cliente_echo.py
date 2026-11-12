# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 2: cliente de eco UDP com limite de tamanho e timeout.

import argparse
import socket


MAX_PAYLOAD_UDP = 65507


def main():
    parser = argparse.ArgumentParser(description="Cliente echo UDP/IPv4.")
    parser.add_argument("--host", default="127.0.0.1", help="Host do servidor (padrão: 127.0.0.1).")
    parser.add_argument("--porta", type=int, default=6000, help="Porta UDP (padrão: 6000).")
    parser.add_argument("--timeout", type=float, default=5.0, help="Espera pela resposta em segundos (padrão: 5).")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout deve ser maior que zero")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
            cliente.settimeout(args.timeout)
            # Em UDP, connect define o destino dos datagramas, sem handshake TCP.
            cliente.connect((args.host, args.porta))
            while True:
                mensagem = input("Mensagem (sair para encerrar): ")
                if mensagem.strip().lower() == "sair":
                    break
                if not mensagem.strip():
                    print("Digite uma mensagem não vazia.")
                    continue
                dados = mensagem.encode("utf-8")
                if len(dados) > MAX_PAYLOAD_UDP:
                    print(f"Mensagem com {len(dados)} bytes. O máximo é {MAX_PAYLOAD_UDP} bytes.")
                    continue
                try:
                    cliente.send(dados)
                    resposta = cliente.recv(MAX_PAYLOAD_UDP)
                    print(f"Eco: {resposta.decode('utf-8')}")
                except socket.timeout:
                    print("Tempo limite: o servidor não respondeu. Você pode enviar outra mensagem.")
                except ConnectionRefusedError:
                    print("Servidor indisponível. Verifique host e porta.")
    except (OSError, UnicodeError, OverflowError, ValueError) as erro:
        print(f"Erro de comunicação: {erro}")
    except (KeyboardInterrupt, EOFError):
        print("\nCliente encerrado.")


if __name__ == "__main__":
    main()
