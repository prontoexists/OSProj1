import sys
import datetime

def log(file, action, message):
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    entry = f"{time} [{action}] {message}\n"
    file.write(entry)

def main():
    if len(sys.argv) != 2:
        print("logger.py")
        return

    log_filename = sys.argv[1]
    with open(log_filename, 'a') as logf:
        log(logf, 'START', 'Logging')
        while True:
            try:
                msg = input()
                if msg == 'QUIT':
                    log(logf, 'STOP', 'FINISHED')
                    break

                action, message = msg.split(' ', 1)
                log(logf, action, message)
            except ValueError:
                print("Invalid input")

if __name__ == "__main__":
    main()
