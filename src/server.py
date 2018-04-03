from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import sys


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        # import pdb; pdb.set_trace()

        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()

            self.wfile.write(b'You did a thing!')
            return

        elif parsed_path.path == '/test':
            try:
                cat = json.loads(parsed_qs['category'][0])
            except KeyError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'You did a bad thing')
                return

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'we did the thing with the qs')
            return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.send_response_only()


def create_server():
    return HTTPServer(('127.0.0.1', 3000), SimpleHTTPRequestHandler)


def run_forever():
    server = create_server()

    try:
        print('Starting server on port 3000')
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()
        # sys.exit()


if __name__ == '__main__':
    run_forever()