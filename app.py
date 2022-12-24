from status import get_status
from update import get_update
from config import print_n_log
from concurrent.futures import ThreadPoolExecutor

def main():
    with ThreadPoolExecutor() as executor:
        executor.submit(get_status)
        executor.submit(get_update)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_n_log("Exiting program")
    except Exception as e:
        print_n_log(e, True)