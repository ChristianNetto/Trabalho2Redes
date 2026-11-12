# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 1: servidor TCP com uma thread por cliente.

import argparse
from datetime import datetime
import socket
import threading


def atender_cliente(conexao, endereco):
    # Cada linha representa uma mensagem, pois o TCP transmite um fluxo de bytes.
    try:
        with conexao, conexao.makefile("r", encoding="utf-8") as entrada:
            for linha in entrada:
                mensagem = linha.rstrip("\r\n")
                if not mensagem.strip():
                    continue
                if mensagem.strip().lower() == "sair":
                    break
                data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{data_hora}] {endereco[0]}:{endereco[1]}: {mensagem}", flush=True)
                conexao.sendall("Mensagem recebida\n".encode("utf-8"))
    except (OSError, UnicodeError) as erro:
        print(f"Erro com {endereco[0]}:{endereco[1]}: {erro}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Servidor TCP multicliente.")
    parser.add_argument("--host", default="0.0.0.0", help="Interface de escuta (padrão: 0.0.0.0).")
    parser.add_argument("--porta", type=int, default=5000, help="Porta TCP (padrão: 5000).")
    args = parser.parse_args()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((args.host, args.porta))
            servidor.listen()
            print(f"Servidor TCP em {args.host}:{args.porta}. Ctrl+C para encerrar.", flush=True)
            while True:
                conexao, endereco = servidor.accept()
                # A thread permite atender outro cliente enquanto este envia mensagens.
                threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except (OSError, OverflowError) as erro:
        print(f"Erro no servidor: {erro}")


if __name__ == "__main__":
    main()
