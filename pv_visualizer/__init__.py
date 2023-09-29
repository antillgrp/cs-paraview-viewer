import os
from trame_client.utils.version import get_version

# Disable warning -->  !!! You are currently using trame@3 which may break your application !!! ...
os.environ["TRAME_DISABLE_V3_WARNING"] = "1"
# print(os.environ)

__version__ = get_version("pv-visualizer")
# print("__version__", __version__)

__all__ = [
    "__version__",
]
