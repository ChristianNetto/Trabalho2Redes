# Integrantes: Christian Netto Moura e Marcio Antonio Ribeiro Junior
# Exercício 10: testes de integração com conexões WebSocket reais.

from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest

from websockets.exceptions import ConnectionClosed
from websockets.sync.client import connect


PASTA = Path(__file__).resolve().parent
AMBIENTE = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")


def porta_livre():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class TesteChatWebSocket(unittest.TestCase):
    def setUp(self):
        # Cada teste executa o servidor em um processo e uma porta independentes.
        temporario = tempfile.TemporaryDirectory()
        self.addCleanup(temporario.cleanup)
        self.pasta_temporaria = Path(temporario.name)
        self.log = self.pasta_temporaria / "servidor.log"
        saida = self.log.open("wb")
        self.addCleanup(saida.close)
        self.porta = porta_livre()
        self.uri = f"ws://127.0.0.1:{self.porta}"
        self.servidor = subprocess.Popen(
            [sys.executable, "-u", str(PASTA / "servidor_ws.py"), "--host", "127.0.0.1", "--porta", str(self.porta)],
            stdout=saida, stderr=subprocess.STDOUT, env=AMBIENTE,
        )
        self.addCleanup(self.parar_processo, self.servidor)
        self.conexoes = ExitStack()
        self.addCleanup(self.conexoes.close)
        self.esperar(lambda: "Ctrl+C" in self.ler_log() or self.servidor.poll() is not None)
        self.assertIsNone(self.servidor.poll(), self.ler_log())

    @staticmethod
    def parar_processo(processo):
        if processo.poll() is None:
            if os.name == "nt":
                # O launcher do Python em um venv pode criar um processo filho.
                # Encerra a árvore inteira para liberar os logs no Windows.
                subprocess.run(
                    ["taskkill", "/PID", str(processo.pid), "/T", "/F"],
                    capture_output=True, check=True, timeout=5,
                )
            else:
                processo.terminate()
            processo.wait(timeout=5)

    def ler_log(self):
        return self.log.read_text(encoding="utf-8")

    def esperar(self, condicao):
        limite = time.monotonic() + 5
        while time.monotonic() < limite:
            if condicao():
                return
            time.sleep(0.02)
        self.fail(f"Tempo limite na verificação. Log do servidor:\n{self.ler_log()}")

    def conectar(self, nickname):
        ws = self.conexoes.enter_context(connect(self.uri, proxy=None, open_timeout=3, close_timeout=1))
        ws.send(nickname)
        # Aguarda o cadastro no servidor antes de iniciar os envios do teste.
        self.esperar(lambda: f"{nickname} conectado:" in self.ler_log())
        return ws

    def verificar_servidor(self):
        self.assertIsNone(self.servidor.poll(), self.ler_log())
        self.assertNotIn("Traceback", self.ler_log())

    def test_broadcast_para_demais_clientes(self):
        clientes = [self.conectar(nome) for nome in ("Ana", "Beto", "Caio")]
        clientes[0].send("Olá, ação!\nSegunda linha")
        # Beto e Caio recebem a mensagem; Ana (remetente) não recebe
        for ws in (clientes[1], clientes[2]):
            self.assertEqual(ws.recv(timeout=3), "[Ana]: Olá, ação!\nSegunda linha")
        with self.assertRaises(TimeoutError):
            clientes[0].recv(timeout=0.2)
        # A mesma conexão continua ativa para mensagens em ambos os sentidos.
        clientes[1].send("Resposta")
        for ws in (clientes[0], clientes[2]):
            self.assertEqual(ws.recv(timeout=3), "[Beto]: Resposta")
        with self.assertRaises(TimeoutError):
            clientes[1].recv(timeout=0.2)
        self.verificar_servidor()

    def test_envios_simultaneos(self):
        nomes = ("Ana", "Beto", "Caio")
        clientes = [self.conectar(nome) for nome in nomes]

        def enviar(ws):
            for numero in range(10):
                ws.send(f"Mensagem {numero}")

        with ThreadPoolExecutor(max_workers=3) as executor:
            list(executor.map(enviar, clientes))
        for ws, remetente in zip(clientes, nomes):
            esperadas = {
                f"[{outro}]: Mensagem {numero}"
                for outro in nomes if outro != remetente
                for numero in range(10)
            }
            recebidas = [ws.recv(timeout=3) for _ in range(20)]
            self.assertEqual(len(recebidas), 20)
            self.assertEqual(set(recebidas), esperadas)
        self.verificar_servidor()

    def test_mensagens_vazias_nao_sao_transmitidas(self):
        ana = self.conectar("Ana")
        beto = self.conectar("Beto")
        for mensagem in ("", "   ", "\t\n"):
            ana.send(mensagem)
        # Uma mensagem posterior marca que as anteriores já foram processadas.
        ana.send("Válida")
        self.assertEqual(beto.recv(timeout=3), "[Ana]: Válida")
        with self.assertRaises(TimeoutError):
            ana.recv(timeout=0.1)
        with self.assertRaises(TimeoutError):
            beto.recv(timeout=0.1)

    def test_nickname_vazio_fecha_apenas_conexao_invalida(self):
        ana = self.conectar("Ana")
        beto = self.conectar("Beto")
        with connect(self.uri, proxy=None, open_timeout=3, close_timeout=1) as invalido:
            invalido.send("   ")
            with self.assertRaises(ConnectionClosed):
                invalido.recv(timeout=3)
            self.assertEqual(invalido.close_code, 1008)
        ana.send("Continuo conectada")
        self.assertEqual(beto.recv(timeout=3), "[Ana]: Continuo conectada")
        self.verificar_servidor()

    def test_dados_binarios_nao_derrubam_servidor(self):
        ana = self.conectar("Ana")
        beto = self.conectar("Beto")
        for identificar in (False, True):
            with self.subTest(nickname_enviado=identificar):
                with connect(self.uri, proxy=None, open_timeout=3, close_timeout=1) as invalido:
                    if identificar:
                        invalido.send("Binario")
                    invalido.send(b"dados binarios")
                    with self.assertRaises(ConnectionClosed):
                        invalido.recv(timeout=3)
                    self.assertEqual(invalido.close_code, 1003)
        ana.send("Servidor ativo")
        self.assertEqual(beto.recv(timeout=3), "[Ana]: Servidor ativo")
        self.verificar_servidor()

    def test_saida_normal_preserva_demais_clientes(self):
        ana = self.conectar("Ana")
        beto = self.conectar("Beto")
        caio = self.conectar("Caio")
        beto.close()
        self.esperar(lambda: "Beto desconectado." in self.ler_log())
        ana.send("Depois da saída")
        self.assertEqual(caio.recv(timeout=3), "[Ana]: Depois da saída")
        self.verificar_servidor()

    def test_queda_abrupta_preserva_chat_e_novas_conexoes(self):
        ana = self.conectar("Ana")
        beto = self.conectar("Beto")
        # Encerra o TCP diretamente, sem enviar o frame de fechamento WebSocket.
        beto.socket.shutdown(socket.SHUT_RDWR)
        beto.socket.close()
        self.esperar(lambda: "Beto desconectado." in self.ler_log())
        caio = self.conectar("Caio")
        ana.send("Depois da queda")
        self.assertEqual(caio.recv(timeout=3), "[Ana]: Depois da queda")
        with self.assertRaises(TimeoutError):
            ana.recv(timeout=0.2)
        self.verificar_servidor()

    def test_cliente_terminal_envia_recebe_e_sai(self):
        ana = self.conectar("Ana")
        log_cliente = self.pasta_temporaria / "cliente.log"
        with log_cliente.open("wb") as saida:
            cliente = subprocess.Popen(
                [sys.executable, "-u", str(PASTA / "cliente_ws.py"), "--host", "127.0.0.1", "--porta", str(self.porta)],
                stdin=subprocess.PIPE, stdout=saida, stderr=subprocess.STDOUT, env=AMBIENTE,
            )
            try:
                # Também valida a nova solicitação quando o nickname é vazio.
                cliente.stdin.write("\nDuda\n".encode("utf-8"))
                cliente.stdin.flush()
                self.esperar(lambda: "Duda conectado:" in self.ler_log())
                ana.send("Recebida enquanto aguarda teclado")
                self.esperar(lambda: "[Ana]: Recebida enquanto aguarda teclado" in log_cliente.read_text(encoding="utf-8"))
                cliente.stdin.write("   \nOlá da Duda\n".encode("utf-8"))
                cliente.stdin.flush()
                self.assertEqual(ana.recv(timeout=3), "[Duda]: Olá da Duda")
                cliente.stdin.write(b"sair\n")
                cliente.stdin.flush()
                cliente.wait(timeout=5)
                self.assertEqual(cliente.returncode, 0)
            finally:
                self.parar_processo(cliente)
                cliente.stdin.close()
        texto = log_cliente.read_text(encoding="utf-8")
        self.assertIn("O nickname não pode ser vazio.", texto)
        self.assertIn("Digite uma mensagem não vazia.", texto)
        self.assertNotIn("Traceback", texto)
        self.esperar(lambda: "Duda desconectado." in self.ler_log())
        beto = self.conectar("Beto")
        ana.send("Ainda conectado")
        self.assertEqual(beto.recv(timeout=3), "[Ana]: Ainda conectado")
        self.verificar_servidor()

    def test_cliente_trata_conexao_recusada(self):
        resultado = subprocess.run(
            [sys.executable, str(PASTA / "cliente_ws.py"), "--host", "127.0.0.1", "--porta", str(porta_livre())],
            input="Teste\n", capture_output=True, encoding="utf-8", env=AMBIENTE, timeout=15,
        )
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        self.assertIn("Conexão recusada", resultado.stdout)
        self.assertNotIn("Traceback", resultado.stdout + resultado.stderr)


if __name__ == "__main__":
    unittest.main()
