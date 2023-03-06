import compiler

while True:
	text = input('> ')
	result, error = compiler.run('<stdin>', text)

	if error: print(error.as_string())
	elif result: print(result)
    

