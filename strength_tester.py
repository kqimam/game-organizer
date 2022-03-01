# Author: Kaiser Imam
# Date: 2/23/2021
# Description: Microservice that receives a password from a client and evaluates it using the zxcvbn API.
#
# Before using this program, first install zxcvbn using the command "pip install zxcvbn" on the Windows Command Prompt.
# Instructions taken from the zxcvbn Python documentation at https://github.com/dwolfhub/zxcvbn-python.
#
# If the installation fails due to your IDE and Windows not using the same version of python, specify the version of
# Python Windows should use by following this guide:
# https://stackoverflow.com/questions/5087831/how-should-i-set-default-python-version-in-windows
#
# Server code adapted from "Python Socket Programming Tutorial" https://www.youtube.com/watch?v=3QiPPX-KeSc

from zxcvbn import zxcvbn
import socket
import threading

# Define the server address and port
SERVER = '127.0.0.1'
PORT = 12345
ADDR = (SERVER, PORT)

# Create the listening socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the listening socket to the port
server.bind(ADDR)


def start():
    """Starts the server.  Creates a new thread whenever a client connects."""
    # Begin listening
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} Port {PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def handle_client(conn, addr):
    """
    Receives the password string, queries zxcvbn, and sends the password strength level and time to crack to the client
    as two strings.
    """
    print(f"[NEW CONNECTION] {addr} connected.")

    # Receive the password to be tested from the client and store it as a string
    pword = conn.recv(1024).decode()

    # Process the password with the zxcvbn API and receive the results in a dictionary
    zxcvbn_results = zxcvbn(pword)

    # zxcvbn uses 4 methods to estimate the time to crack according to https://github.com/dropbox/zxcvbn
    # For now this service will use "offline_fast_hashing_1e10_per_second", but this can easily be changed if needed

    strength_score = zxcvbn_results["score"]
    time_to_crack = zxcvbn_results["crack_times_display"]["offline_fast_hashing_1e10_per_second"]

    # Send the result strings back to the client in 2 send operations
    conn.send(str(strength_score).encode())
    conn.send(str(time_to_crack).encode())

    # Close the connection with the client
    conn.close()


print("[STARTING] Server is starting...")
start()
