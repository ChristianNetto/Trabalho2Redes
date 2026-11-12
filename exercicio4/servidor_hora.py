# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 4: servidor de hora com threads e contador protegido por Lock.

import argparse
from datetime import datetime
import socket
import threading


total_atendidos = 0
lock_contador = threading.Lock()


def atender_cliente(conexao, endereco):
    global total_atendidos
    try:
        with conexao:
            # A conexão é a solicitação: envia a hora e fecha o socket em seguida.
            agora = datetime.now()
            conexao.sendall(agora.strftime("%H:%M:%S").encode("utf-8"))
            # Incremento e log ficam na mesma seção crítica para manter a ordem.
            with lock_contador:
                total_atendidos += 1
                print(
                    f"[{agora:%Y-%m-%d %H:%M:%S}] "
                    f"{endereco[0]}:{endereco[1]} | Total atendidos: {total_atendidos}",
                    flush=True,
                )
    except OSError as erro:
        # Um erro nesta conexão não interrompe o atendimento dos demais clientes.
        print(f"Erro com {endereco[0]}:{endereco[1]}: {erro}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Servidor de hora TCP com threads.")
    parser.add_argument("--host", default="0.0.0.0", help="Interface de escuta (padrão: 0.0.0.0).")
    parser.add_argument("--porta", type=int, default=7000, help="Porta TCP (padrão: 7000).")
    args = parser.parse_args()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((args.host, args.porta))
            servidor.listen()
            print(f"Servidor de hora em {args.host}:{args.porta}. Ctrl+C para encerrar.", flush=True)
            while True:
                conexao, endereco = servidor.accept()
                threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except (OSError, OverflowError) as erro:
        print(f"Erro no servidor: {erro}")


if __name__ == "__main__":
    main()
