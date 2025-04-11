from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Default to index.html if no path is specified
        if self.path == '/':
            self.path = '/index.html'
        
        # Remove query parameters for file serving
        self.path = self.path.split('?')[0]
        
        try:
            # Try to serve the requested file
            return SimpleHTTPRequestHandler.do_GET(self)
        except:
            # If file not found, serve index.html
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

def run(port=8000):
    print(f"Starting server on port {port}...")
    # Create server object
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    
    # Print serving directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Serving files from: {current_dir}")
    print(f"Server running at: http://localhost:{port}/")
    
    # Start server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == '__main__':
    run()
