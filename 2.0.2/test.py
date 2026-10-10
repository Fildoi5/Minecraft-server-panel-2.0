log = "ahoj"

logs_str = "a\nb\nc\n"

list = logs_str.split("\n")

logs_str = ""
list.pop(0)
for log in list:
    logs_str += log + "\n"

print(logs_str)
