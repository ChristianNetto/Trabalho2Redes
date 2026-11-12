# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 10: cliente Python de chat com WebSockets.

import argparse
import threading

from websockets.exceptions import ConnectionClosed, WebSocketException
from websockets.sync.client import connect


def receber_mensagens(websocket, encerrado):
    try:
        # A thread recebe enquanto a principal aguarda a entrada do teclado.
        for mensagem in websocket:
            print(mensagem, flush=True)
    except ConnectionClosed:
        if not encerrado.is_set():
            print("A conexão com o servidor foi interrompida.", flush=True)
    finally:
        if not encerrado.is_set():
            print("Conexão encerrada. Pressione Enter para sair.", flush=True)
        encerrado.set()


def main():
    parser = argparse.ArgumentParser(description="Cliente de chat WebSocket.")
    parser.add_argument("--host", default="127.0.0.1", help="Host do servidor (padrão: 127.0.0.1).")
    parser.add_argument("--porta", type=int, default=8765, help="Porta TCP (padrão: 8765).")
    args = parser.parse_args()
    if not 1 <= args.porta <= 65535:
        parser.error("--porta deve estar entre 1 e 65535")

    try:
        nickname = input("Nickname: ").strip()
        while not nickname:
            print("O nickname não pode ser vazio.")
            nickname = input("Nickname: ").strip()
        # Colchetes permitem usar também um endereço IPv6 em --host.
        host = f"[{args.host}]" if ":" in args.host else args.host
        uri = f"ws://{host}:{args.porta}"
        # A conexão é direta ao host informado, sem depender de proxy do sistema.
        with connect(uri, proxy=None, open_timeout=10, close_timeout=3) as websocket:
            websocket.send(nickname)
            encerrado = threading.Event()
            recepcao = threading.Thread(target=receber_mensagens, args=(websocket, encerrado), daemon=True)
            recepcao.start()
            print("Digite mensagens ou sair para encerrar.", flush=True)
            try:
                while not encerrado.is_set():
                    mensagem = input()
                    if encerrado.is_set() or mensagem.strip().lower() == "sair":
                        break
                    if not mensagem.strip():
                        print("Digite uma mensagem não vazia.")
                        continue
                    websocket.send(mensagem)
            finally:
                encerrado.set()
                # O fechamento WebSocket desbloqueia a thread de recepção.
                websocket.close()
                recepcao.join()
    except ConnectionRefusedError:
        print("Conexão recusada. Verifique se o servidor está em execução e confira host e porta.")
    except TimeoutError:
        print("Tempo limite ao conectar ao servidor.")
    except ConnectionClosed:
        print("A conexão com o servidor foi encerrada.")
    except (OSError, WebSocketException, ValueError) as erro:
        print(f"Erro de comunicação: {erro}")
    except (KeyboardInterrupt, EOFError):
        print("\nCliente encerrado.")


if __name__ == "__main__":
    main()
