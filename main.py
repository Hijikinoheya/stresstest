import os
import time
import math
import psutil
import logging
import requests
import multiprocessing
from datetime import datetime

# ログ設定
logging.basicConfig(filename='stress_test.log', level=logging.DEBUG, format='%(asctime)s - %(message)s')

def log_message(message):
    logging.info(message)
    print(message)

def get_cpu_clock_speed():
    try:
        clock_speed = psutil.cpu_freq().current
        log_message(f"CPU Clock Speed: {clock_speed} MHz")
    except Exception as e:
        log_message(f"Error getting CPU clock speed: {e}")

def cpu_stress(duration):
    log_message("Starting CPU stress test...")
    start_time = time.time()
    processes = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=cpu_worker, args=(duration, start_time))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    log_message("CPU stress test completed.")

def cpu_worker(duration, start_time):
    while time.time() - start_time < duration:
        math.sqrt(64 * 64 * 64 * 64 * 64)

def memory_stress(duration, size_mb):
    log_message(f"Starting memory stress test for {size_mb} MB...")
    start_time = time.time()
    memory = []
    while time.time() - start_time < duration:
        memory.append(' ' * (1024 * 1024))  # 1MB
    log_message("Memory stress test completed.")

def network_stress(duration, url):
    log_message(f"Starting network stress test to {url}...")
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            response = requests.get(url)
            log_message(f"Request to {url} status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            log_message(f"Network error: {e}")
    log_message("Network stress test completed.")

def disk_benchmark(duration, drive, file_size_mb):
    log_message(f"Starting disk benchmark on {drive} with {file_size_mb}MB file...")
    start_time = time.time()
    test_file = os.path.join(drive, 'test_file.tmp')
    with open(test_file, 'wb') as f:
        f.write(os.urandom(file_size_mb * 1024 * 1024))  # ランダムなデータを書き込む
    elapsed_time = time.time() - start_time
    log_message(f"Disk write completed in {elapsed_time:.2f} seconds.")
    
    # ファイル読み込みテスト
    start_time = time.time()
    with open(test_file, 'rb') as f:
        f.read()
    elapsed_time = time.time() - start_time
    log_message(f"Disk read completed in {elapsed_time:.2f} seconds.")
    
    # テストファイルの削除
    os.remove(test_file)
    log_message("Disk benchmark completed.")

def main():
    log_message("Starting stress test...")

    # ユーザー入力
    choice = input("Choose a test: \n1. CPU Test\n2. Memory Test\n3. Network Test\n4. Disk Benchmark\nEnter choice: ")

    if choice == '1':
        duration = int(input("Enter CPU test duration in seconds: "))
        get_cpu_clock_speed()
        cpu_stress(duration)

    elif choice == '2':
        duration = int(input("Enter memory test duration in seconds: "))
        size_mb = int(input("Enter memory size in MB: "))
        memory_stress(duration, size_mb)

    elif choice == '3':
        duration = int(input("Enter network test duration in seconds: "))
        url = input("Enter URL (e.g., google.com or custom URL): ")
        if not url.startswith("https://"):
            url = "https://" + url
        network_stress(duration, url)

    elif choice == '4':
        duration = int(input("Enter disk benchmark duration in seconds: "))
        drive = input("Enter the drive (e.g., C: or /mnt): ")
        file_size_mb = int(input("Enter file size for disk benchmark in MB: "))
        disk_benchmark(duration, drive, file_size_mb)

    else:
        log_message("Invalid choice. Exiting.")
        print("Invalid choice. Exiting.")
        return

    log_message("All tests completed.")

if __name__ == "__main__":
    main()
