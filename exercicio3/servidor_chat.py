# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 3: chat TCP com threads e broadcast.

import argparse
import socket
import threading


# O lock protege o cadastro compartilhado pelas threads de atendimento.
clientes = {}
lock_clientes = threading.Lock()


def broadcast(mensagem, remetente):
    dados = (mensagem + "\n").encode("utf-8")
    with lock_clientes:
        destinatarios = list(clientes.items())
    for conexao, (_, lock_envio) in destinatarios:
        if conexao is remetente:
            continue
        try:
            # Impede que duas threads misturem mensagens no mesmo socket.
            with lock_envio:
                conexao.sendall(dados)
        except OSError:
            # Desbloqueia a leitura da thread responsável pelo cliente desconectado.
            try:
                conexao.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


def atender_cliente(conexao, endereco):
    nickname = None
    try:
        with conexao, conexao.makefile("r", encoding="utf-8") as entrada:
            # A primeira linha identifica o usuário; as demais são mensagens.
            linha = entrada.readline()
            if not linha:
                return
            nickname = linha.strip()
            if not nickname:
                return
            with lock_clientes:
                clientes[conexao] = (nickname, threading.Lock())
            print(f"{nickname} entrou ({endereco[0]}:{endereco[1]}).", flush=True)
            broadcast(f"{nickname} entrou na sala.", conexao)
            for linha in entrada:
                mensagem = linha.rstrip("\r\n")
                if mensagem.strip().lower() == "sair":
                    break
                if mensagem.strip():
                    broadcast(f"[{nickname}]: {mensagem}", conexao)
    except (OSError, UnicodeError) as erro:
        print(f"Erro com {endereco[0]}:{endereco[1]}: {erro}", flush=True)
    finally:
        with lock_clientes:
            removido = clientes.pop(conexao, None)
        if removido is not None:
            print(f"{nickname} saiu.", flush=True)
            broadcast(f"{nickname} saiu da sala.", conexao)


def main():
    parser = argparse.ArgumentParser(description="Servidor de chat TCP.")
    parser.add_argument("--host", default="0.0.0.0", help="Interface de escuta (padrão: 0.0.0.0).")
    parser.add_argument("--porta", type=int, default=5001, help="Porta TCP (padrão: 5001).")
    args = parser.parse_args()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            servidor.bind((args.host, args.porta))
            servidor.listen()
            print(f"Chat TCP em {args.host}:{args.porta}. Ctrl+C para encerrar.", flush=True)
            while True:
                conexao, endereco = servidor.accept()
                threading.Thread(target=atender_cliente, args=(conexao, endereco), daemon=True).start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except (OSError, OverflowError) as erro:
        print(f"Erro no servidor: {erro}")
    finally:
        # Encerra as conexões cadastradas ao parar o servidor.
        with lock_clientes:
            conexoes = list(clientes)
        for conexao in conexoes:
            try:
                conexao.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            conexao.close()


if __name__ == "__main__":
    main()
