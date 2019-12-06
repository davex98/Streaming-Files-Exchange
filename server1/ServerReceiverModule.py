import socket
import queue
from typing import Dict, List


# Dict(thread_pool, isBusy, queue)
class ServerReceiverModule:
    def __init__(self, client_id, clients_dict: Dict[str, List], client_socket):
        self.client_id = client_id
        self.clients_dict = clients_dict
        self.client_socket: socket.socket = client_socket

    @staticmethod
    def parse_msg(data):
        return data.split(sep=';')

    def receive_data(self):
        while True:
            this_cli_q: queue.Queue = self.clients_dict[f'{self.client_id}'][2]
            data = this_cli_q.get()
            cli_2_id, file_name = self.parse_msg(data)

            # Check if cli_2 is busy
            if self.clients_dict[f'{cli_2_id}'][1]:
                this_cli_q.put('BUSY')
                # ??
                continue
            else:
                self.clients_dict[f'{cli_2_id}'][1] = True
                this_cli_q.put('NOT_BUSY')
                this_cli_q = self.clients_dict[f'{cli_2_id}'][2]

                buffer_size = 16
                while True:
                    data = self.client_socket.recv(buffer_size).decode('utf-8')
                    this_cli_q.put(data)
                    if data == 'END':
                        self.clients_dict[f'{cli_2_id}'][1] = False
                        break
