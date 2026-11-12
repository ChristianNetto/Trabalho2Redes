# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 10: chat em tempo real com WebSockets.

import argparse
import asyncio

from websockets.asyncio.server import broadcast, serve
from websockets.exceptions import ConnectionClosed


# Somente conexões com um nickname válido participam do chat.
clientes = set()


async def atender_cliente(websocket):
    nickname = None
    try:
        # A primeira mensagem WebSocket identifica o remetente das próximas.
        identificacao = await websocket.recv()
        if not isinstance(identificacao, str):
            await websocket.close(code=1003, reason="O nickname deve ser texto.")
            return
        nickname = identificacao.strip()
        if not nickname:
            await websocket.close(code=1008, reason="O nickname não pode ser vazio.")
            return
        clientes.add(websocket)
        print(f"{nickname} conectado: {websocket.remote_address}", flush=True)

        async for mensagem in websocket:
            if not isinstance(mensagem, str):
                await websocket.close(code=1003, reason="Envie mensagens de texto.")
                return
            if not mensagem.strip():
                continue
            # Inclui o remetente. broadcast ignora conexões fechadas e falhas
            # individuais de envio, sem bloquear a entrega aos demais clientes.
            broadcast(clientes.copy(), f"[{nickname}]: {mensagem}")
    except ConnectionClosed:
        # Uma queda de conexão encerra somente o atendimento deste cliente.
        print(f"Conexão encerrada: {websocket.remote_address}", flush=True)
    finally:
        clientes.discard(websocket)
        if nickname:
            print(f"{nickname} desconectado.", flush=True)


async def executar_servidor(host, porta):
    # O contexto fecha o servidor e suas conexões quando a execução é cancelada.
    async with serve(atender_cliente, host, porta) as servidor:
        print(f"Chat WebSocket em ws://{host}:{porta}. Ctrl+C para encerrar.", flush=True)
        await servidor.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Servidor de chat WebSocket.")
    parser.add_argument("--host", default="0.0.0.0", help="Interface de escuta (padrão: 0.0.0.0).")
    parser.add_argument("--porta", type=int, default=8765, help="Porta TCP (padrão: 8765).")
    args = parser.parse_args()
    if not 1 <= args.porta <= 65535:
        parser.error("--porta deve estar entre 1 e 65535")

    try:
        asyncio.run(executar_servidor(args.host, args.porta))
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
    except OSError as erro:
        print(f"Erro no servidor: {erro}")


if __name__ == "__main__":
    main()
