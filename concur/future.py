from concurrent.futures import ThreadPoolExecutor
import time

def do_something(seconds):
    print(f'sleep {seconds}s')
    time.sleep(seconds)
    return 'sleep done'


# test thread pool
def thread_pool_map():
    start_time = time.perf_counter()

    executor = ThreadPoolExecutor()
    secs = [8, 7, 9, 5, 2, 3, 4]
    results = executor.map(do_something, secs)
    for result in results:
        print(result)

    end_time = time.perf_counter() - start_time
    print(f'total time {round(end_time, 2)}s')

if __name__ == "__main__":
   print("File future.py executed when ran directly")
   thread_pool_map()
else:
   print("this File executed when imported")