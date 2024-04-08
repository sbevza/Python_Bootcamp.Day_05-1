import threading
import time
import random


class Screwdriver:
    def __init__(self):
        self.owner = None
        self.lock = threading.Lock()


class Doctor(threading.Thread):
    def __init__(self, number, left_screwdriver, right_screwdriver):
        super().__init__()
        self.number = number
        self.left_screwdriver = left_screwdriver
        self.right_screwdriver = right_screwdriver

    def run(self):
        if self.number == 9:
            first, second = self.right_screwdriver, self.left_screwdriver
        else:
            first, second = self.left_screwdriver, self.right_screwdriver

        with first.lock:
            first.owner = self
            time.sleep(random.uniform(0.1, 0.5))
            with second.lock:
                second.owner = self
                self.blast()

    def blast(self):
        print(f"Doctor {self.number}: BLAST!")


if __name__ == "__main__":
    num_doctors = 5
    screwdrivers = [Screwdriver() for i in range(num_doctors)]

    doctors = [
        Doctor(i + 9, screwdrivers[i], screwdrivers[(i + 1) % num_doctors])
        for i in range(num_doctors)
    ]

    for doctor in doctors:
        doctor.start()

    for doctor in doctors:
        doctor.join()
