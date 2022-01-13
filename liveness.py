from http.server import BaseHTTPRequestHandler, HTTPServer
import random, os, signal, time

hostName = "0.0.0.0"
PORT = os.getenv("PORT")  # None if not set
serverPort = 80 if PORT is None else int(PORT)

# MyHttpServer implements the HTTP request handler
class MyHttpServer(BaseHTTPRequestHandler):
    # we only have a simple GET handler
    # this handler calls another function that should implement some smart logic to determine the liveness state
    # we return 500 when our application is not in a good state, else we return 200 status
    def do_GET(self):
        message = ""
        if self.some_liveness_logic():
            self.send_response(200)
            message = "all is good!"
        else:
            self.send_response(500)
            message = "things are not looking good!"
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>LIVENESS</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(
            bytes("<p>This is an example liveness check: %s</p>" % message, "utf-8")
        )
        self.wfile.write(bytes("</body></html>", "utf-8"))

    # just some placeholder for a liveness logic function
    def some_liveness_logic(self):
        return random.randint(0, 9) % 2 == 0

def receiveSignal(signalNumber, frame):
    print('Received a SIGTERM signal:', signalNumber)
    print('Terminating in 3 seconds...')
    time.sleep(3)
    raise SystemExit('Exiting gracefully')


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, receiveSignal)
    webServer = HTTPServer(
        server_address=(hostName, serverPort), RequestHandlerClass=MyHttpServer
    )
    print("HTTP server started serving at: http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("HTTP server has stopped!")
