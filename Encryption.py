class EncryptionProgram:
    def __init__(self):
        self.key = None

    def def_pass(self, key):
        self.key = key.upper()

    def _vigenere(self, text, decrypt=False):
        if self.key is None:
            return "Error"

        listRes = []
        key = self.key
        key_len = len(key)

        for i, char in enumerate(text.upper()):
            if not char.isalpha():
                continue
            txt = ord(char) - ord('A')
            key2 = ord(key[i % key_len]) - ord('A')
            if decrypt:
                newVig = (txt - key2 + 26) % 26
            else:
                newVig = (txt + key2) % 26
            listRes.append(chr(newVig + ord('A')))

        return "Set " + ''.join(listRes)

    def encrypt(self, text):
        return self._vigenere(text, decrypt=False)

    def decrypt(self, text):
        return self._vigenere(text, decrypt=True)


def main():
    program = EncryptionProgram()

    while True:
        try:
            msg_input = input()
            if not msg_input.strip():
                continue
            parts = msg_input.strip().split(' ', 1)
            command = parts[0].upper()
            argument = parts[1] if len(parts) > 1 else ""

            if command == "PASSW":
                program.def_pass(argument)
                print("RESULT")
            elif command == "ENCRYPT":
                print(program.encrypt(argument))
            elif command == "DECRYPT":
                print(program.decrypt(argument))
            elif command == "QUIT":
                break
            else:
                print("Error")
        except Exception as e:
            print("Error")

if __name__ == "__main__":
    main()
