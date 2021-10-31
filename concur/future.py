from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def do_something(seconds):
    print(f'sleep {seconds}s')
    time.sleep(seconds)
    return f'sleep task {seconds} done'


def thread_pool_loop(executor, secs):
    results = [executor.submit(do_something, secs[i]) for i in range(len(secs))]
    for f in as_completed(results):
        print(f.result())


# test thread pool
def thread_pool_map(executor: object, secs):
    results = executor.map(do_something, secs)
    for result in results:
        print(result)


if __name__ == "__main__":
    print("File future.py executed when ran directly")
    start_time = time.perf_counter()
    executor = ThreadPoolExecutor()
    secs = [8, 7, 9, 5, 2, 3, 4]

    thread_pool_loop(executor, secs)
    # thread_pool_map(executor, secs)
    end_time = time.perf_counter() - start_time
    print(f'total time {round(end_time, 2)}s')

else:
    print("this File executed when imported")
