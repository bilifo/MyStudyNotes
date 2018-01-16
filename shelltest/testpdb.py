import pdb
import os
import io
def add(num1=0, num2=0):
    return int(num1) + int(num2)
def sub(num1=0, num2=0):
    return int(num1) - int(num2)
def main():
    #Assuming our inputs are valid numbers
	a=input("a:")
	print(""+a)
	pdb.set_trace() # <-- Break point added here
	b=input("b:")
	a_b=add(a+b)
	print(a_b)
	subtraction = sub(a, b)
	pdb.set_trace() # <-- Break point added here
	print(subtraction)
if __name__ == '__main__':
    main()