import time, os, sys
sys.path.append(os.getcwd())
from src.core.config import CONFIG

if __name__ == "__main__":
    print("??  SOVEREIGN BOARDROOM ONLINE")
    print(f"   DATA_DIR: {CONFIG.DATA_DIR}")
    while True:
        time.sleep(30)
