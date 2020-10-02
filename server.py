"""
Naveh Marchoom
312275746
"""
from socket import *
import sys

file_list = {}

"""
We start a server TCP connection, and start waiting for connections:
"""
server = socket(AF_INET, SOCK_STREAM)
server_ip = sys.argv[1]
server_port = int(sys.argv[2])
server.bind((server_ip, server_port))
server.listen(5)
while True:
    """
    For each connection we recieve we get one command from the client, that start
    with the digit 1 or with the digit 2.
    """
    client_socket, client_address = server.accept()
    print("Connection accepted: ", client_address)
    data = client_socket.recv(1024).decode()
    arguments = data.split(" ")

    if arguments[0] == '1':
        """
        in case we get the digit 1, we add every file on the list we recieved to our file list as keys
        with the client address and the port he gave us as values.
        """
        for i in range(2, len(arguments)):
            file_list[arguments[i]] = (client_address[0], arguments[1])

    elif arguments[0] == '2':
        """
        in case we got the digit 2, we will look the rest of the message as a keyword in the filelist, and if
        we find files that have that keyword in their name, we will send them back with their info to the
        client.
        """
        message = ""
        for file_name in file_list:
            if file_name.find(arguments[1]) != -1:
                message += file_name + " " + file_list[file_name][0] + " " + file_list[file_name][1] + ", "
        message = message.rstrip(",") + "\n"
        client_socket.send(message.encode("utf-8"))

print("server disconnected")
