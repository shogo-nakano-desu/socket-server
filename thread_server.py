import threading
import socketserver


class ThreadedEchoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
     # Echo the back to the client
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = '%s: %s' % (cur_thread.name, data)
        self.request.send(bytes(response, 'utf-8'))
        return


class ThreadedEchoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == '__main__':
    import socket
    import threading
    address = ('localhost', 0)  # let the kernel give us a port
    server = ThreadedEchoServer(address, ThreadedEchoRequestHandler)
    ip, port = server.server_address  # find out what port we were given
    t = threading.Thread(target=server.serve_forever)
    t.daemon
    t.start()
    print('Server loop running in thread:', t.name)
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
