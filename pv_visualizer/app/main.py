from pathlib import Path
from trame.app import get_server

SERVER = None

def main(server=None, data=None, plugins=None, **kwargs):
    from . import engine, ui

    global SERVER
    if server is None:
        server = get_server()

    # Adding CLI parameters
    
    # Will get deprecated for Certscan (not longer supported) 
    if data is None:
        server.cli.add_argument(
            "--data", help="Path to browse", dest="data", default=str(Path.home())
        )

    if plugins is None:
        server.cli.add_argument(
            "--plugins", help="List of distributed plugins to load", dest="plugins"
        )
        args, _ = server.cli.parse_known_args()
        plugins = args.plugins.split(",") if args.plugins else []

    # Init application
    server.client_type = "vue2"
    SERVER = server

    engine.initialize(server, plugins)# ./engine/__init__.py
    ui.initialize(server) # ./ui/__init__.py

    # Start server
    return server.start(**kwargs)


if __name__ == "__main__":
    server = get_server()
    main(server)
