from utils.logging_config import setup_logging

# Logger configuration has to be done before everything else
setup_logging()

import sys
import communication

if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    elif len(sys.argv) == 1:
        host = "localhost"
    else:
        sys.exit("Invalid number of arguments, server address expected")
    communication.start(host)
