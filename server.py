import socketserver
import logging
from lib import parsers, api, calendar

logger = logging.getLogger(__name__)


event_calendar = calendar.Calendar

class TCPHandler(socketserver.BaseRequestHandler):
    """

    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        logger.log(logging.INFO, f"Received [{self.client_address[0]}]: {self.data}")
        command, *parameters = parsers.parse_message(self.data)
        operation = getattr(api, command)
        response = operation(*parameters, calendar=event_calendar)
        logger.log(logging.INFO, f"[{self.client_address[0]}] Executed: {operation}({", ".join(parameters)})")
        if response is not None:
            self.request.sendall(response)
            logger.log(logging.INFO, f"Sent [{self.client_address[0]}]: {response}")

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()