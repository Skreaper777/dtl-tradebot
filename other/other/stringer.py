import sys
str = sys.stdin.readlines()
str = '\t'.join(str)
# str = input()
str = str.replace("т.д.", "т>д>")
str = str.replace(".\"", "`")
str = str.replace(". ", "~ ")
str = str.replace(".\n", "~\n")

str = str.replace(".", ".\n\t")

str = str.replace("~ ", ". ")
str = str.replace("~\n", ".\n\t")
str = str.replace("т>д>", "т.д.")
str = str.replace("`", ".\"")

str = str.replace("? ", "~ ")
str = str.replace("?\n", "`\n")
str = str.replace("?", "?\n\t")
str = str.replace("~ ", "? ")
str = str.replace("`\n", "?\n")

# str = str.replace(": ", "~ ")
# str = str.replace(":", ":\n\t")
# str = str.replace("~ ", ": ")

str = str.replace("\tHuman", "\n---\nHuman")


str = str.replace("Human:", "Human~")
str = str.replace(":", ":\n\t")
str = str.replace("\n\t ", "\n\t\t")
str = str.replace("Human~", "Human:")

str = str.replace("ChatGPT:\n\t\t", "ChatGPT:\n\t")

# str = str.replace("ChatGPT:", "ChatGPT:\n\t")

print(str)