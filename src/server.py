from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from cowpy import cow
import json
import io


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        parsed_qs = parse_qs(parsed_path.query)

        # GET / - returns a valid HTML formatted response with a project \
        # description and an anchor tag which references a link to /cow.
        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()

            self.wfile.write(b'''
            <!DOCTYPE html>
            <html>
            <head>
            <title> cowsay </title>
            </head>
            <body>
            <header>
            <nav>
            <ul>
            <li><a href="/cowsay">cowsay</a></li>
            </ul>
            </nav>
            <header>
            <main>
            <!-- project description -->
            </main>
            </body>
            </html>
            ''')
            return
        # GET /cowsay - returns a generic cowpy response which displays a \
        # helpful message to the client about how they can further interact \
        # with the API.
        elif parsed_path.path == '/cowsay':
            cheese = cow.Moose()
            msg = cheese.milk('yo im a moose')
            print(msg)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(msg.encode('utf8'))
            return

        # GET /cow?msg=text - returns a cowpy response which \
        # correctly displays a default cow object including \
        # the text from your query string.
        elif parsed_path.path == '/cow':
            try:
                message = json.loads(parsed_qs['msg'][0])
                cheese = cow.Moose()
                msg = cheese.milk(message)
                print(msg)
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

    # POST /cow msg=text - returns a cowpy response with a JSON body \
    # {"content": "<cowsay cow>"}
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = io.BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

        # self.send_response(200)
        # self.end_headers()
        # self.send_response_only()


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
