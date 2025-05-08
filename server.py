import socket
import threading
import time
from collections import defaultdict

class TupleSpaceServer:
    def __init__(self, port):
        self.port = port
        self.tuple_space = {}
        self.client_count = 0
        self.operation_count = 0
        self.read_count = 0
        self.get_count = 0
        self.put_count = 0
        self.error_count = 0

        def start_server(self):
            try:
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind(('0.0.0.0', self.port))
                server_socket.listen(5)
                print(f"Server started on port {self.port}")