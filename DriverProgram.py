import subprocess

class DriverProgram:
    def __init__(self, log_file):
        self.log_file = log_file
        self.history = []
        self.current_password = ""

        # Start logger subprocess
        self.logger_process = subprocess.Popen(
            ["python", "logger.py", self.log_file],
            stdin=subprocess.PIPE,
            text=True
        )

        # Start encryption subprocess
        self.encryption_process = subprocess.Popen(
            ["python", "Encryption.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        self.sendLog("Start Logging")

    def run(self):
        while True:
            command = input("Enter command (password-encrypt-decrypt-history or quit): ").strip().lower()

            if command == "quit":
                self.sendLog("QUIT command.")
                self.sendECryp("QUIT")
                self.sendLog("STOP Driver.")
                self.finishProj()
                break

            self.sendLog(f"COMMAND {command}")

            if command == "password":
                self.vault()

            elif command == "encrypt":
                self.callEnc()

            elif command == "decrypt":
                self.callDec()

            elif command == "history":
                self.dispHist()
                self.sendLog("History Result.")

            else:
                print("Invalid command.")
                self.sendLog("Error")

    def vault(self):
        option = input("Use a string from history (y/n)? ").strip().lower()

        if option == "n":
            password = input("Enter a new password: ").strip()
            if not password.isalpha():
                print("Error: Letters only")
                self.sendLog("Error")
                return
            self.current_password = password
            self.sendECryp(f"PASSW {self.current_password}")
            print("Password set.")
            self.sendLog("Password set.")

        elif option == "y":
            self.dispHist()
            try:
                index = int(input("Enter index from history: "))
                if 0 <= index < len(self.history):
                    self.current_password = self.history[index]
                    self.sendECryp(f"PASSW {self.current_password}")
                    print("Password set from history.")
                    self.sendLog("RESULT Password Set.")
                else:
                    print("Invalid index.")
                    self.sendLog("ERROR Invalid history")
            except ValueError:
                print("Invalid input.")
                self.sendLog("Error Incorrect input")

    def callEnc(self):
        text = self.onlyHistoryILikeIsCoolWars("encrypt")
        if text is None:
            return

        self.sendECryp(f"Encrypt {text}")
        response = self.readEnc()
        print(response)
        self.sendLog(f"Result {response}")
        if response.startswith("Result "):
            encrypted = response.split(" ", 1)[1]
            self.history.append(encrypted)

    def callDec(self):
        text = self.onlyHistoryILikeIsCoolWars("decrypt")
        if text is None:
            return

        self.sendECryp(f"Decrypt {text}")
        response = self.readEnc()
        print(response)
        self.sendLog(f"Result {response}")
        if response.startswith("Result "):
            decrypted = response.split(" ", 1)[1]
            self.history.append(decrypted)

    def onlyHistoryILikeIsCoolWars(self, action):
        option = input("Use a string from history (y/n)? ").strip().lower()

        if option == "n":
            text = input(f"new string {action}: ").strip()
            if not text.isalpha():
                print("Letters only")
                self.sendLog("Error Letters only")
                return None
            self.history.append(text)
            return text

        elif option == "y":
            self.dispHist()
            try:
                index = int(input("Enter index from history: "))
                if 0 <= index < len(self.history):
                    return self.history[index]
                else:
                    print("Error")
                    self.sendLog("ERROR Invalid history")
            except ValueError:
                print("Error invalid input.")
                self.sendLog("Error invalid Input")
        else:
            print("Invalid option.")
            self.sendLog("ERROR Invalid history")
        return None

    def dispHist(self):
        print("\n History ")
        for i, item in enumerate(self.history):
            print(f"{i}: {item}")

    def sendLog(self, message):
        self.logger_process.stdin.write(message + "\n")
        self.logger_process.stdin.flush()

    def sendECryp(self, command):
        self.encryption_process.stdin.write(command + "\n")
        self.encryption_process.stdin.flush()

    def readEnc(self):
        return self.encryption_process.stdout.readline().strip()

    def finishProj(self):
        self.logger_process.stdin.close()
        self.encryption_process.stdin.close()
        self.encryption_process.stdout.close()
        print("Exiting")

# --- Entry Point ---
if __name__ == "__main__":
    log_file_name = "log.txt"
    driver = DriverProgram(log_file_name)
    driver.run()
