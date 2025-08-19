import socket
import prot
import os
import base64
from pathlib import Path

# -----------------------------
# Server folder where files are stored
# -----------------------------
server_folder = Path(r'C:\Users\USER\Documents\py_server')

# Dictionary to keep track of file uploads and duplicates
files = {}

# -----------------------------
# Function: Download a file from server
# -----------------------------
def Download(list):
    # list[1] -> file name and type
    list[1:]=[" ".join(list[1:])]
    try:
        # Check if the file exists in the server dictionary
        if list[1] not in files:
            return "error","The file is not in the server... "

        # Full path to the file
        file_path = server_folder.joinpath(Path(list[1]))

        # Read the file in binary mode
        with open(file_path, "rb") as file:
            file = file.read()

            # Encode file to Base64 and decode to string
            encoded_file = base64.b64encode(file).decode()

            if encoded_file:
                return "succes",encoded_file

            return "error","Could not download this file.."

    except Exception as error:
        print(str(error))
        return str(error)

# -----------------------------
# Function: Upload a file to server
# -----------------------------
def Upload(list):
    # list[2] -> file name and type
    # list[1] -> file content (Base64 encoded)
    list[2:]=[" ".join(list[2:])] #(incase of a file name with spaces)

    try:
        # Check for duplicates
        if list[2] in files:
            old_name = list[2]
            files[list[2]] += 1

            # Change file name according to how many duplicates exist
            list[2] = Path(list[2])
            list[2] = str(list[2].with_stem(list[2].stem + f"({files[old_name]})"))
            files[list[2]] = 0
        else:
            files[list[2]] = 0  # No duplicates

        # Full path for saving the file
        full_path = server_folder.joinpath(Path(list[2]))

        # Decode Base64 content back to bytes
        list[1] = base64.b64decode(list[1])

        # Write the file to server folder
        with open(full_path, "wb") as file:
            file.write(list[1])

        # Check if the file is readable
        if os.access(full_path, os.R_OK):
            return "succes",f"Successfully Uploaded {list[2]} !"
        else:
            files[old_name] -= 1
            files.pop(list[2])
            return "error","An error occurred while uploading, please upload again"
    except Exception as error:
        print(str(error))
        return str(error)

# -----------------------------
# Setup server socket
# -----------------------------
serv = socket.socket()
serv.bind(("0.0.0.0", 60123))
serv.listen(1)
print("Server is listening...")

# Accept a client connection
cli_sock, cli_addr = serv.accept()

# -----------------------------
# Map commands to functions
# -----------------------------
functions = {"UPLOAD": Upload, "DOWNLOAD": Download}

# -----------------------------
# Main server loop
# -----------------------------
while True:
    try:
        # Receive message and split into command and arguments
        list = prot.receive_msg(cli_sock).split()

        # Exit condition
        if list[0] == "EXIT":
            break
        # Call the appropriate function and send back the response
        answer = functions[list[0]](list)
        cli_sock.send(prot.create_msg_with_header(answer[0]+" "+answer[1]).encode())
    except Exception as error:
        print(str(error))
        cli_sock.send(prot.create_msg_with_header(str(error)).encode())

# -----------------------------
# Close server
# -----------------------------
print("Server closed")
serv.close()
