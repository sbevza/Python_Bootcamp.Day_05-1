import threading
import time
import random


class Screwdriver:
    def __init__(self, owner):
        self.owner = owner
        self.lock = threading.Lock()


class Doctor(threading.Thread):
    def __init__(self, number, left_screwdriver, right_screwdriver):
        super().__init__()
        self.number = number
        self.left_screwdriver = left_screwdriver
        self.right_screwdriver = right_screwdriver

    def run(self):
        time.sleep(random.uniform(0.1, 0.5))
        with self.left_screwdriver.lock:
            time.sleep(random.uniform(0.1, 0.5))
            with self.right_screwdriver.lock:
                self.blast()

    def blast(self):
        print(f"Doctor {self.number}: BLAST!")


if __name__ == "__main__":
    num_doctors = 50
    screwdrivers = [Screwdriver(i) for i in range(num_doctors)]

    doctors = [
        Doctor(i, screwdrivers[i], screwdrivers[(i + 1) % num_doctors])
        for i in range(num_doctors)
    ]

    for doctor in doctors:
        doctor.start()

    for doctor in doctors:
        doctor.join()
