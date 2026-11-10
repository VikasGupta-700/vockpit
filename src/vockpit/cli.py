import argparse
import sys
from vockpit import __version__


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="vockpit",
        description="Vockpit: the Vibe Coding Cockpit. You steer. AI builds.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"vockpit {__version__}",
    )
    args = parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
