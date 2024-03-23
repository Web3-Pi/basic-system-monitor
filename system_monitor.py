from config.conf import APP_DESCRIPTION, MONITOR_PORT
from services.httpserver import MonitoringHTTPServer

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description=APP_DESCRIPTION)
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=MONITOR_PORT,
        help=f"HTTP server listen port (default: {MONITOR_PORT})"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    MonitoringHTTPServer.run_forever(args.port)


if __name__ == '__main__':
    main()
