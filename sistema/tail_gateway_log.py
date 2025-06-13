#!/usr/bin/env python3
import os
import sys
import time
from datetime import datetime

def follow(path):
    with open(path, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line

def main():
    # permite passar o arquivo de log como argumento
    if len(sys.argv) >= 2:
        logfile = sys.argv[1]
    else:
        logfile = os.getenv('GATEWAY_LOG_FILE', 'logs/api_gateway.log')

    # Espera o arquivo existir
    while not os.path.exists(logfile):
        print(f"{datetime.now().isoformat()} waiting for {logfile}…")
        time.sleep(1)

    print(f"{datetime.now().isoformat()} monitoring {logfile}")
    for line in follow(logfile):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{ts}  {line}", end='')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped monitoring.")
