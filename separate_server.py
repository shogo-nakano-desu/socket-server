import os
import socketserver


class ForkingEchoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
     # Echo the back to the client
        data = self.request.recv(1024)
        cur_pid = os.getpid()
        response = '%s: %s' % (cur_pid, data)
        self.request.send(bytes(response, 'utf-8'))
        return


class ForkingEchoServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    import socket
    import threading
    address = ('localhost', 0)  # let the kernel give us a port
    server = ForkingEchoServer(address, ForkingEchoRequestHandler)
    ip, port = server.server_address  # find out what port we were given
    t = threading.Thread(target=server.serve_forever)
    t.daemon
    t.start()
    print('Server loop running in process:', os.getpid())
    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    # Send the data
    message = 'Hello, world'
    print('Sending : "%s"' % message)
    len_sent = s.send(bytes(message, 'utf-8'))
    # Receive a response
    response = s.recv(1024)
    print('Received: "%s"' % response)
    # Clean up
    s.close()
    server.socket.close()
