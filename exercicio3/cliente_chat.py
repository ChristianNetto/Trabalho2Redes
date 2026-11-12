# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 3: cliente de chat TCP com recepção em uma thread separada.

import argparse
import socket
import threading


def receber_mensagens(cliente, encerrado):
    try:
        with cliente.makefile("r", encoding="utf-8") as entrada:
            for linha in entrada:
                print(linha.rstrip("\r\n"), flush=True)
    except (OSError, UnicodeError) as erro:
        if not encerrado.is_set():
            print(f"Erro na recepção: {erro}")
    finally:
        if not encerrado.is_set():
            print("Conexão encerrada pelo servidor. Pressione Enter para sair.", flush=True)
        encerrado.set()


def main():
    parser = argparse.ArgumentParser(description="Cliente de chat TCP.")
    parser.add_argument("--host", default="127.0.0.1", help="Host do servidor (padrão: 127.0.0.1).")
    parser.add_argument("--porta", type=int, default=5001, help="Porta TCP (padrão: 5001).")
    args = parser.parse_args()

    try:
        nickname = input("Nickname: ").strip()
        while not nickname:
            print("O nickname não pode ser vazio.")
            nickname = input("Nickname: ").strip()
        with socket.create_connection((args.host, args.porta), timeout=10) as cliente:
            # O chat pode ficar ocioso enquanto espera mensagens de outros usuários.
            cliente.settimeout(None)
            cliente.sendall((nickname + "\n").encode("utf-8"))
            encerrado = threading.Event()
            recepcao = threading.Thread(target=receber_mensagens, args=(cliente, encerrado), daemon=True)
            recepcao.start()
            print("Digite mensagens ou sair para encerrar.", flush=True)
            try:
                while not encerrado.is_set():
                    mensagem = input()
                    if encerrado.is_set():
                        break
                    if mensagem.strip().lower() == "sair":
                        cliente.sendall(b"sair\n")
                        break
                    if not mensagem.strip():
                        print("Digite uma mensagem não vazia.")
                        continue
                    cliente.sendall((mensagem + "\n").encode("utf-8"))
            finally:
                encerrado.set()
                # shutdown interrompe a leitura bloqueada antes de fechar o socket.
                try:
                    cliente.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                recepcao.join()
    except ConnectionRefusedError:
        print("Conexão recusada. Verifique se o servidor está em execução e confira host e porta.")
    except socket.timeout:
        print("Tempo limite ao conectar ao servidor.")
    except (OSError, UnicodeError, OverflowError) as erro:
        print(f"Erro de comunicação: {erro}")
    except (KeyboardInterrupt, EOFError):
        print("\nCliente encerrado.")


if __name__ == "__main__":
    main()
