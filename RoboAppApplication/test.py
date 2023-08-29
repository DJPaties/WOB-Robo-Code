import time
from concurrent.futures import ThreadPoolExecutor



message = ""

def whileLoop():
    while True:
        print(message)
        time.sleep(4)

def setMessage():
    while True:
        x = input("Enter message:")
        global message
        message = x

def main():
    excuter = ThreadPoolExecutor()
    future = excuter.submit(whileLoop)
    future2 = excuter.submit(setMessage)
    return future,future2


if __name__ == "__main__":
    main()



