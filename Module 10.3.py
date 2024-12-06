import threading
from time import sleep
from random import randint

class Bank(threading.Thread):
    def __init__(self, balance):
        threading.Thread.__init__(self)
        self.balance = balance

    lock = threading.Lock()

    def deposit(self):
        for _ in range(100):
            replenishment = randint(50, 500)
            self.balance += replenishment
            if self.lock.locked() and self.balance >= 500:
                self.lock.release()
            print(f'\nПополнение: {replenishment}. Баланс: {self.balance}')
            sleep(0.001)


    def take(self):
        for _ in range(100):
            request_amount = randint(50, 500)
            print(f'\nЗапрос на {request_amount}')
            if request_amount <= self.balance:
                self.balance -= randint(50, 500)
                print(f'\nСнятие: {request_amount}. Баланс: {self.balance}')
                sleep(0.001)
            else:
                print('\nЗапрос отклонён, недостаточно средств')
                self.lock.acquire()
                sleep(0.001)

bk = Bank(50)

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')

