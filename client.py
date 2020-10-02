"""
Naveh Marchoom
312275746
"""
from socket import *
from os import listdir, getcwd
from os.path import isfile, join
import sys

EOF_FLAG = b'0xFF'

mode = sys.argv[1]
dest_ip = sys.argv[2]
dest_port = int(sys.argv[3])

if mode == "1":
    """
    On the first mode we first look at the directory we are running from, and make a list
    of all the files in this directory. We create a message which start with "1", then the port
    we are planning to listen on, and then a list of all the files in the directory. 
    """
    listen_port = int(sys.argv[4])
    my_path = getcwd()
    file_list = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    message = "1 " + str(listen_port) + " " + " ".join(file_list)

    """
    Now, we open a client socket to the server and send him our message to tell him
    we are going to listen on the given port for clients who want to download files from us
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((dest_ip, dest_port))
    s.send(message.encode("utf-8"))
    s.close()

    """
    Now we open a server socket, on which we wait for clients to connect us.
    On every connection accepted we recieve the name of the file the client want
    to download from us, and then we send him the requested file, 1024 bytes at a time.
    In order to mark the end of the transfer we made b'0x00' the EOF flag which when will 
    be sent will tell the client that we finished transfering the file.
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("localhost", listen_port))
    s.listen(5)
    while True:
        client_socket, client_address = s.accept()
        file_to_send = client_socket.recv(1024).decode()
        if file_to_send in file_list:
            file = open(file_to_send, "rb")
            while True:
                info = file.read(1024)
                if info == b'':
                    client_socket.send(EOF_FLAG)
                    break
                client_socket.send(info)
            file.close()


elif mode == "2":
    """
    On this mode we will recieve a search keyword from the user, which we will send
    to the server on a message that begins with the digit 2.
    We will recieve from the server a list of all the files that contains that keyword, each with
    their address location. We will print to the user a prompt to choose which file he want to download.
    """
    keyword = input("Search:")
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((dest_ip, dest_port))
    message = "2 " + keyword
    s.send(message.encode("utf-8"))
    data = s.recv(1024).decode().rstrip(", \n")
    s.close()
    if data != "":
        data = list(map(lambda x: x.split(" "), data.split(", ")))
        for i, f in enumerate(data):
            print(i + 1, f[0])
        file_number = int(input("Choose:")) - 1

        """
        If the file chose by the user exists, open a client connection to the address added to
        that file on the data given by the server, and send that server the name of the file we want to
        download. After that start reading bytes from the server while writing them into the file we want,
        until we get a EOF_FLAG from the server on which we will close the file and close the connection to the
        server.
        """
        if data[file_number] is not None:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((data[file_number][1], int(data[file_number][2])))
            s.send(data[file_number][0].encode("utf-8"))
            file = open(data[file_number][0], "wb")
            while True:
                info = s.recv(1024)
                if info == EOF_FLAG:
                    break
                file.write(info)
            file.close()
            s.close()
