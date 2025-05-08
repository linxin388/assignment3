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

                threading.Thread(target=self.print_tuple_space_summary, daemon=True).start()

                while True:
                    client_socket, client_address = server_socket.accept()
                    self.client_count += 1
                    threading.Thread(target=self.handle_client, args=(client_socket,)).start()
            except socket.error as e:
                print(f"Error starting server: {e}")

        def handle_client(self, client_socket):
            try:
                with client_socket:
                    while True:
                        request = client_socket.recv(1024).decode('utf-8')
                        if not request:
                            break
                        response = self.process_request(request)
                        client_socket.send(response.encode('utf-8'))
            except socket.error as e:
                print(f"Error handling client: {e}")
        def process_request(self, request):
            self.operation_count +=1
            command = request[3]
            key = request[5:].split('')[0]
            value = request[5:].split('',1)[1]if command == 'P'else''

            response = ""
            with threading.Lock():
                if command == 'R':
                    self.read_count +=1
                    response = self.process_read(key)
                elif command == 'G':
                    self.get_count +=1
                    response=self.process_get(key)
                elif command == 'P':
                    self.put_count +=1
                    response = self.process_put(key,value)
                else:
                    self.error_count +=1
                    response = "024 ERR invalid command"
                return response
        def process_read(self,key):
            value = self.tuple_space.get(key)
            if value:
                response = f"{len(f'OK({key},{value})read'):03d}OK({key},{value})read"
            else:
                self.error_count +=1
                response = "024 ERR " + key + " does not exist"
            return response

        def process_get(self, key):
            value = self.tuple_space.pop(key, None)
            if value:
                response = f"{len(f'OK ({key}, {value}) removed'):03d} OK ({key}, {value}) removed"
            else:
                self.error_count += 1
                response = "024 ERR " + key + " does not exist"
            return response

        def process_put(self, key, value):
            if key in self.tuple_space:
                self.error_count += 1
                response = "024 ERR " + key + " already exists"
            else:
                self.tuple_space[key] = value
                response = f"{len(f'OK ({key}, {value}) added'):03d} OK ({key}, {value}) added"
            return response

