import interpreter

print("INPUT CODE: ")
while True:
    text = input("> ")
    
    result, error = interpreter.run('<stdin>',text)

    if error: print(error.as_string())
    else: print(result)
    

