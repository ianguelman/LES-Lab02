import sys


def main():
    print ("Hello, from script, received: ")
    for arg in sys.argv:
        print(arg)
    
main()