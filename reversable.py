# reversable.py

user_input = input("Enter a word or phrase: ")

# Normalize the input: lowercase and remove non-letter characters
cleaned = ""
for char in user_input:
    if char.isalnum():
        cleaned += char.lower()

# Reverse the cleaned string
reversed_word = cleaned[::-1]

# Check if it's a palindrome
if cleaned == reversed_word:
    print("This is a palindrome!")
else:
    print("This is not a palindrome.")
