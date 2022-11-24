import unittest
from unittest import mock
from io import StringIO

from server import Server
from client import Client


class TestClientServer(unittest.TestCase):
    @mock.patch("socket.socket.connect")
    @mock.patch("socket.socket.recv")
    @mock.patch("socket.socket.send")
    def test_client(self, send_mock, recv_mock, conn_mock):
        file = open("urls.txt", "r", encoding="utf_8")
        urls = file.readlines()
        print_data = [url.strip() + ": Hello from server!" for url in urls]

        send_data = [url.strip().encode(encoding="utf_8") for url in urls]
        send_data.append("!disconnect".encode(encoding="utf_8"))

        file.close()

        recv_mock.return_value = "Hello from server!".encode(encoding="utf_8")

        client = Client(10, "urls.txt")
        with mock.patch(
            "client.sys.stdout", new_callable=StringIO
        ) as print_mock:
            client.work()
            print_client = print_mock.getvalue().split("\n")[:-1]

        send_client = []
        for call in send_mock.mock_calls:
            for args in call:
                for arg in args:
                    send_client.append(arg)

        self.assertCountEqual(print_data, print_client)
        self.assertCountEqual(send_data, send_client)
        self.assertEqual(client.counter, 100)
        self.assertEqual(len(conn_mock.mock_calls), 101)

    @mock.patch("socket.socket")
    def test_incorrect_url(self, socket_mock):
        recieved_data = ["https://vk"]
        recieved_data.append("!disconnect")

        sended_data = [url.encode(encoding="utf_8") for url in recieved_data]

        socket_mock.return_value.accept.return_value = (socket_mock, None)
        socket_mock.recv.side_effect = sended_data

        server = Server(1, 5)
        with mock.patch(
            "client.sys.stdout", new_callable=StringIO
        ) as print_mock:
            server.work()
            print_server = print_mock.getvalue().split("\n")[:-1]

        print_data = "URL https://vk does not exist"

        self.assertEqual(print_data, print_server[0])
        self.assertEqual(server.counter, 0)

    @mock.patch("server.Server.fetch_url")
    @mock.patch("socket.socket")
    def test_server(self, socket_mock, fetch_mock):
        file = open("urls.txt", "r", encoding="utf_8")
        urls = file.readlines()

        recieved_data = [url.strip() for url in urls]
        recieved_data.append("!disconnect")

        sended_data = [url.encode(encoding="utf_8") for url in recieved_data]

        file.close()

        socket_mock.return_value.accept.return_value = (socket_mock, None)
        socket_mock.recv.side_effect = sended_data

        server = Server(10, 5)
        with mock.patch(
            "client.sys.stdout", new_callable=StringIO
        ) as print_mock:
            server.work()
            print_server = print_mock.getvalue().split("\n")[:-1]

        print_data = [f"URL downloaded: {i}" for i in range(1, 101)]

        fetch_client = []
        for call in fetch_mock.mock_calls:
            for args in call:
                for arg in args:
                    if len(arg) > 1:
                        fetch_client.append(arg)

        self.assertEqual(print_data, print_server)
        self.assertCountEqual(fetch_client, recieved_data[:-1])
        self.assertEqual(server.counter, 100)


if __name__ == "__main__":
    unittest.main()
