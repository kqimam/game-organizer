# Author: Kaiser Imam
# Date: 2/23/2021
# Description: Example program that shows how to use the strength tester service.

import socket

# Define the address and port used to connect to the strength tester server
strength_tester_address = '127.0.0.1'
strength_tester_port = 12345


def test_program():
    """
    Test program showing how to use the strength tester microservice.
    """
    while True:
        pword = str(input("Please enter the password you would like to test: "))

        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the strength tester server
        client_socket.connect((strength_tester_address, strength_tester_port))

        # Send the password string
        client_socket.send((str(pword)).encode())

        # Receive results strings from the server
        strength_score = client_socket.recv(1024).decode()
        time_to_crack = client_socket.recv(1024).decode()

        # Close the connection
        client_socket.close()

        print("\nPassword: %s" % (pword))
        print("Strength Level: %s" % strength_score)
        print("Time to Crack: %s\n" % time_to_crack)


if __name__ == '__main__':
    test_program()
