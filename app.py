from status import get_status
from update import get_update, send_error_message
from config import print_n_log
from concurrent.futures import ThreadPoolExecutor
import psutil

def main():
    # Set the maximum amount of memory that can be used to 100 MB
    memory_limit = 1024 * 1024 * 1024
    psutil.Process().rlimit(psutil.RLIMIT_AS, (memory_limit, memory_limit))
    
    with ThreadPoolExecutor() as executor:
        executor.submit(get_status)
        executor.submit(get_update)

if __name__ == "__main__":
    main()