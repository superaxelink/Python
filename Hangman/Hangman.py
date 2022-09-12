import random
import time

print("\nWelcome to Hangman game\n")
name = input("Enter your name: ")
print("Hello " + name + "! Best of luck!")
time.sleep(2)
print("The game is about to start!\n Let's play Hangman!")
time.sleep(3)

def main(): #main function to initialize arguments
	global count
	global display
	global word
	global already_guessed
	global length
	global play_game
	words_to_guess = ["january","border","image","film","promise","kids","lungs","doll","rhyme","damage","plants","Pneumonoultramicroscopicsilicovolcanoconiosis"]
	word = random.choice(words_to_guess) #we choose on of the words in the words_to_guess list
	length = len(word)
	count = 0
	display = '_'*length #draws a line for us according to the length of the words to guess
	already_guessed = []
	play_game = ""

def play_loop():
	global play_game
	play_game = input("Do you want to play again? y = yes, n=no \n")
	while play_game not in ["y","n","Y","N"]:
		play_game = input("Do you want to play again? y=yes, n=no \n")
	if (play_game == "y" or play_game == "Y"):
		main()
		hangman()
	elif (play_game == "n" or play_game == "N"):
		print("Thanks for playing! We expect you back again!");
		exit()

def hangman():
	global count
	global display
	global word
	global already_guessed
	global play_game
	limit = 5 #maximum guesses
	guess = input("This is the Hangman Word: " + display + " Enter your guess: \n") 
	#takes the user input as guess
	guess = guess.strip()
	#guess.strip removes the letter from the given word
	if len(guess.strip()) == 0 or len(guess.strip()) >= 2 or guess <= "9":
		print("Invalid input, Try a letter\n")
		hangman()
	elif guess in word:
		already_guessed.extend([guess])
		index = word.find(guess)
		word = word[:index] + "_" + word[index + 1:]
		display = display[:index] + guess + display[index + 1:]
		print(display + "\n")

	elif guess in already_guessed:
		print("Try another letter.\n")

	else:
		count += 1
		
		if count == 1:
			time.sleep(1)
			print("  ____\n"
						" |    \n"
						" |    \n"
						" |    \n"
						" |    \n"
						" |    \n"
						" |    \n"
						"_|__\n")
			print("Wrong guess. " + str(limit - count) + " guesses remaining.\n")

		elif count == 2:
			time.sleep(1)
			print("  ____ \n"
						" |    |\n"
						" |    |\n"
						" |     \n"
						" |     \n"
						" |     \n"
						" |     \n"
						"_|__\n")
			print("Wrong guess." + str(limit - count) + " guesses remaining.\n")

		elif count == 3:
			time.sleep(1)
			print("  ____ \n"
						" |    |\n"
						" |    |\n"
						" |    |\n"
						" |     \n"
						" |     \n"
						" |     \n"
						"_|__\n")
			print("Wrong guess." + str(limit - count) + " guesses remaining.\n")

		elif count == 4:
			time.sleep(1)
			print("  ____ \n"
						" |    |\n"
						" |    |\n"
						" |    |\n"
						" |    o\n"
						" |     \n"
						" |     \n"
						"_|__\n")
			print("Wrong guess." + str(limit - count) + " guesses remaining.\n")

		elif count == 5:
			time.sleep(1)
			print("  ____ \n"
						" |    |\n"
						" |    |\n"
						" |    |\n"
						" |    o\n"
						" |   /|\ \n"
						" |   / \ \n"
						"_|__\n")
			print("Wrong guess. You are hanged!!!\n")
			print("The word was:",already_guessed,word)
			play_loop()

	if word == '_'*length:
		print("Congrats! You have guessed the word correctly!")
		play_loop()

	elif count != limit:
		hangman()

main()

hangman()

	



