# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 2: servidor de eco UDP.

import argparse
import socket


MAX_PAYLOAD_UDP = 65507


def main():
    parser = argparse.ArgumentParser(description="Servidor echo UDP/IPv4.")
    parser.add_argument("--host", default="0.0.0.0", help="Interface de escuta (padrão: 0.0.0.0).")
    parser.add_argument("--porta", type=int, default=6000, help="Porta UDP (padrão: 6000).")
    args = parser.parse_args()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
            servidor.bind((args.host, args.porta))
            print(f"Servidor UDP em {args.host}:{args.porta}. Ctrl+C para encerrar.", flush=True)
            while True:
                try:
                    # Recebe o datagrama inteiro; o limite é em bytes, não em caracteres.
                    dados, endereco = servidor.recvfrom(MAX_PAYLOAD_UDP + 1)
                    if not dados.strip() or len(dados) > MAX_PAYLOAD_UDP:
                        continue
                    print(f"{endereco[0]}:{endereco[1]}: {dados.decode('utf-8', errors='replace')}", flush=True)
                    # Devolve os mesmos bytes, sem alterar o conteúdo recebido.
                    servidor.sendto(dados, endereco)
                except OSError as erro:
                    print(f"Erro ao atender datagrama: {erro}", flush=True)
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except (OSError, OverflowError) as erro:
        print(f"Erro no servidor: {erro}")


if __name__ == "__main__":
    main()
