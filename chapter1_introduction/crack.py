'''
Changes
    -The book strips word of newline when read from dictionary.txt, but not line from passwords.txt so it won't return as equal
'''
import crypt


def testPass(cryptPass):
    salt = cryptPass[0:2]
    dictFile = open('dictionary.txt', 'r')

    for word in dictFile.readlines():
        word = word.strip('\n')
        cryptWord = crypt.crypt(word, salt)
        if (cryptWord == cryptPass):
            print("[+] Found Password: " + word)
            return

    print("[-] Password Not Found.")

    return


def main():
    passFile = open('passwords.txt')

    for line in passFile.readlines():
        line = line.strip('\n')

        if ":" in line:
            user = line.split(':')[0]
            cryptPass = line.split(':')[1].strip(' ')
            print("[*] Cracking Password For: "+user)
            testPass(cryptPass)


if __name__ == "__main__":
    main()
