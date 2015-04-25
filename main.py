#cs3130 Main Project
#Janelle Montgomery
#April/25/2015

#The purpose of this project is to build off of the messenger program that I have
#put together in a previous lab. It will be a fully functional messenger accessible
#from the command line. Any amount of users may us this messenger.
#It will be encrypted and require a log in to sign in. The protocols and other data
#will be defined in the readme file attached with code.

#The main program will set up the screen for the server and client to communicate


#This displays the menu to the user
def display():
    print("--")
    print("Welcome to Janelle's Messenger")
    print("--\n")
    print('The following commands are supported:\n')
    print('1) signin')
    print('2) users')
    print('3) join chat')
    print('4) message a user')
    print('5) signout')
    print('6) exit\n')
    
def start():
    display()
    print("--\n")
