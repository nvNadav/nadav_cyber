import socket
import prot
import base64
import os
from pathlib import Path

# -----------------------------
# Setup client socket
# -----------------------------
cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cli.connect(("127.0.0.1", 60123))

# Example file and client folder paths
file_send = r"C:\Users\USER\Documents\examples\client_server_2.7.txt"
client_folder = Path(r"C:\Users\USER\Documents\py_client")

# -----------------------------
# Function: Upload a file
# -----------------------------
def Upload(sock):
    try:
        # Ask user for the file path to upload
        file_path = input("What is the file path? ")

        # Read file as bytes
        with open(file_path, "rb") as f:
            file = f.read()

            # Encode file in base64 and decode to string
            file = base64.b64encode(file).decode()

            # Create protocol message: UPLOAD + file contents + file name
            msg = prot.create_msg_with_header("UPLOAD " + file + f" {Path(file_path).name}")

            # Send message to server
            cli.send(msg.encode())

            # Receive server response
            return prot.receive_msg(cli)
    except Exception as error:
        print(str(error))

# -----------------------------
# Function: Download a file
# -----------------------------
def Download(sock):
    try:
        # Ask user for the file name to download
        file_name = input("What is the file name? ")

        # Create protocol message: DOWNLOAD + file name
        msg = prot.create_msg_with_header("DOWNLOAD " + file_name)
        cli.send(msg.encode())

        # Receive the file from server
        downloaded_file = prot.receive_msg(sock)

        # Decode Base64 string back to bytes
        downloaded_file = base64.b64decode(downloaded_file)

        # Create full path in client folder
        full_path = client_folder.joinpath(Path(file_name))

        # Save the downloaded bytes to a file
        with open(full_path, "wb") as file:
            file.write(downloaded_file)

        # Check if file is readable
        if os.access(full_path, os.R_OK):
            return f"Successfully downloaded {file_name}!"
        else:
            return f"Could not download {file_name}"
    except Exception as error:
        return str(error)

# -----------------------------
# Map commands to functions
# -----------------------------
functions = {"UPLOAD": Upload, "DOWNLOAD": Download}

# -----------------------------
# Main client loop
# -----------------------------
while True:
    try:
        request = input("Upload, Download or Exit? ").upper()

        if request == "EXIT":
            cli.send(prot.create_msg_with_header("EXIT").encode())
            break

        if request not in functions:
            print("The function that you entered does not exist...")
            continue

        # Call the appropriate function and print the result
        answer = functions[request](cli)
        print(answer)
    except Exception as error:
        print(str(error))

# -----------------------------
# Close client
# -----------------------------
print("Client closed")
cli.close()
