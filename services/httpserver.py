import json
import socketserver
from http.server import BaseHTTPRequestHandler

from config.conf import MONITOR_PORT, MONITORING_ENDPOINT
from services.systemmonitor import SystemMonitor


class MonitoringServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        if self.path == MONITORING_ENDPOINT:
            assert isinstance(self.server, MonitoringHTTPServer)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.server.monitor.get_last_sample().to_dict()).encode("UTF-8"))
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            response = '<!DOCTYPE html><html><head><title>Unauthorized</title></head><body><h1>You are not authorized '\
                       'to access this page</h1></body></html>'

            self.wfile.write(response.encode("UTF-8"))

    # Added to suppress log messages on the console
    def log_request(self, code: int | str = ..., size: int | str = ...) -> None:
        pass


class MonitoringHTTPServer(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.monitor = SystemMonitor()

    @classmethod
    def run_forever(cls, port: int = MONITOR_PORT):
        addr = ('', port)
        httpd = MonitoringHTTPServer(addr, MonitoringServerRequestHandler)

        print(f"Starting HTTP server, listening on port {addr[1]}, data available via endpoint {MONITORING_ENDPOINT}")
        httpd.monitor.start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Keyboard interrupt - stopping server and monitor")
            print("Shutting down HTTP server")
            httpd.server_close()

            print("Shutting down system monitor service")
            httpd.monitor.stop()
