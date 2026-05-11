import random


word_bank=['rizz','ohio','couch','tiktok', 'skidmarks']

word=random.choice(word_bank)
guessedWord=['_']*len(word)
attempts=10
guessed_letters=set()


while attempts > 0 :
    print('\nCurrent word:' + ' '.join(guessedWord))
    guess=input('Guess a letter: ').lower()
    if len(guess)!=1 or not guess.isalpha():
        print('Please enter a single letter')
    if guess in guessed_letters:
        print('You\'ve already guessed this letter!')
    if guess in word:
        for i in range(len(word)):
            if word[i]==guess:
                guessedWord[i]=guess
        print('Great guess!')
    else:
        attempts-=1
        print('Wrong guess! Attempts left: '+ str(attempts))
    
    if '_' not in guessedWord:
        print('\nCongratulations!!You guessed the word ' + word)
        break

    if attempts==0 and '_' in guessedWord:
        print('\nYou\'ve run out of attempts!! The word was ' + word)

