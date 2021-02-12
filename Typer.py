from cryptography.fernet import Fernet


def _do(number: str):
	"""
	Prompts and executes the write
	"""
	import pyautogui
	with open("config.txt", "r") as config:
		config.readline()
		i = 0
		for line in config:
			i += 1
			if i == int(number):
				type_text = _decrypt_message(line.strip().encode())
				pyautogui.alert("Click into the field where you want your password to be written \nand press OK")
				pyautogui.write(type_text)
				break
		if i != int(number):
			print("You do not have a password with that index. Please try again!")


def _copy_pw():
	"""
	Asks and executes the write. To be noted that is not a copy paste scenario.
	"""
	number = input("\nWhat password id would you like to copy?\nTo exit, please enter 0\nEnter a number: ")
	if number == "0":
		return
	else:
		_do(number)
		_copy_pw()


def _new_pw():
	"""
	Asks and stores any number of new passwords
	"""
	response = input("Do you want to store a new password? (y/n) ")
	if response == "y":
		password = input("Enter the new password: ")
		with open("config.txt", "a") as config:
			password = _encrypt_message(password)
			config.write(password.decode() + "\n")
		_new_pw()


def _pw_show():
	"""
	Asks and prints out the saved passwords in plain text
	"""
	password_show = input("Do you want to see your passwords? (y/n) ")
	if password_show == "y":
		with open("config.txt", "r") as config:
			config.readline()
			i = 0
			for line in config:
				i += 1
				line = _decrypt_message(line.encode())
				print(f"{i} - {line.strip()}")


def _generate_key():
	"""
	Generates a key and saves it into a file
	"""
	key = Fernet.generate_key()
	with open("security.key", "wb") as key_file:
		key_file.write(key)


def _load_key():
	"""
	Load the previously generated key
	"""
	return open("security.key", "rb").read()


def _encrypt_message(message):
	"""
	Encrypts a message
	"""
	key = _load_key()
	bytes_message = message.encode(encoding='utf-8')
	f = Fernet(key)
	encrypted_message = f.encrypt(bytes_message)
	return encrypted_message


def _decrypt_message(encrypted_message):
	"""
	Decrypts an encrypted message
	"""
	key = _load_key()
	f = Fernet(key)
	decrypted_message = f.decrypt(encrypted_message)
	return decrypted_message.decode()


def _first_time_use():
	"""
	Create the security file and store the encrypted master password on line 1
	"""
	pw1 = "1"
	pw2 = "2"
	while pw1 != pw2:
		pw1 = input("Please set a master password: ")
		pw2 = input("Enter the password again: ")
	_generate_key()
	with open("config.txt", "a") as config:
		en_pw = _encrypt_message(pw1)
		config.write(en_pw.decode() + "\n")
	print(">>>The security and config files have been created. \n>>>Please do not alter them in any way.")
	print(">>>If altered, the saved passwords will be lost forever!")


def _main():
	c_pw = input("Please enter your master password: ")
	with open("config.txt", "r") as config:
		f = config.readline().strip()
		s_pw = _decrypt_message(f.encode())
	if c_pw != str(s_pw):  # If user fails to enter the correct master password
		_main()
	else:
		_new_pw()
		_pw_show()
		_copy_pw()


if __name__ == "__main__":
	print("Welcome to eZKey, your handy password database.")
	import os
	if not os.path.exists("security.key"):
		_first_time_use()
	_main()
	print("Have a safe and eZ day!\nDeveloped by KazzyJr (c) 2021")

