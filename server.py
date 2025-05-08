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

        def print_tuple_space_summary(self):
            while True:
                try:
                    time.sleep(10)
                    tuple_count = len(self.tuple_space)
                    total_tuple_size = sum(len(key) + len(value) for key, value in self.tuple_space.items())
                    total_key_size = sum(len(key) for key in self.tuple_space.keys())
                    total_value_size = sum(len(value) for value in self.tuple_space.values())
                    average_tuple_size = total_tuple_size / tuple_count if tuple_count else 0
                    average_key_size = total_key_size / tuple_count if tuple_count else 0
                    average_value_size = total_value_size / tuple_count if tuple_count else 0

                    print("Tuple Space Summary:")
                    print(f"Number of tuples: {tuple_count}")
                    print(f"Average tuple size: {average_tuple_size}")
                    print(f"Average key size: {average_key_size}")
                    print(f"Average value size: {average_value_size}")
                    print(f"Total number of clients: {self.client_count}")
                    print(f"Total number of operations: {self.operation_count}")
                    print(f"Total READs: {self.read_count}")
                    print(f"Total GETs: {self.get_count}")
                    print(f"Total PUTs: {self.put_count}")
                    print(f"Total errors: {self.error_count}")
                except Exception as e:
                    print(f"Error printing summary: {e}")
                    break

        class TupleSpaceClient:
            def __init__(self, server_host, server_port, request_file_path):
                self.server_host = server_host
                self.server_port = server_port
                self.request_file_path = request_file_path

