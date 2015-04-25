#cs3130 Main Project
#Janelle Montgomery
#April/25/2015

#The purpose of this project is to build off of the messenger program that I have
#put together in a previous lab. It will be a fully functional messenger accessible
#from the command line. Any amount of users may us this messenger.
#It will be encrypted and require a log in to sign in. The protocols and other data
#will be defined in the readme file attached with code.

#This is the bulk of the program including client and server

import sys, argparse, string, ssl,socket
import threading
import main
from random import randint

#global client id so the server knows who is talking
CLIENT_ID = 0
CLIENT_NAME = 0
host = '127.0.0.1'
#what the server uses to check if all the information has been sent <term>
term = '.'
#certification stuff
cafile = 'ca.crt'
certfile = 'localhost.pem'
#used for the thread to connect the client and server
lock = threading.Lock()


def client(host,port):
   #show the client the display commands
    p = port
    h= host
    main.start()
    print("-----******-----")
    print("To begin please sign in or sign up :)")
    begin()
    print("Enter a selection from 1-6")
    correct = False
    while not correct:
        #accept user selection
        selection = input()
        print("-----******-----")
        #carry out command
        if selection == ('1'):
            signin()
        elif selection == ('2'):
            listusers()
        elif selection == ('3'):
            message(h,p)
        elif selection == ('4'):
            sendMsg()
        elif selection == ('5'):
            signout()
        elif selection == ('6'):
            leave()
        else:
            print('Your selection is not valid please try again.')


    
#this will handle the TCP connection side of the client
def message(host,port):
    d=users()
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    
    #connect to the host
    try:
        raw_sock.connect((host, port))
    except:
        print('Unable to connect')
        leave()

    #connection has been started    
    print('Connected to remote host. Chat started.')
    ssl_sock = context.wrap_socket(raw_sock, server_hostname=host)
    lock.acquire()
    cont = True
    #options while in chat
    while cont == True:
        print('Send: ')
        send = input()
        if not send:
            break
        elif send=='leave':
            user = CLIENT_NAME
            #i use a m` as it is a random combo of characters that is likely not to be used.
            send = user +'m`'+ 'User has left the chatroom' + term
            ecmsg=send.encode('ascii')
            ssl_sock.sendall(ecmsg)
            lock.release()
            break
            
        elif send=='message':
            sendMsg()
        elif send=='checkmessages':
            print("-----******-----")
            print('Inbox: ')
            inbox()
            print("-----******-----")
        else:
            user = CLIENT_NAME
            send = user +'m`'+ send + term
            ecmsg=send.encode('ascii')
            ssl_sock.sendall(ecmsg)
            reply = recv_all(ssl_sock)
            reply = reply.replace('.','')
            if not send:
                break
            else:
                print (str(reply))
           
    ssl_sock.close()
    leave() 
    
#displays the messages that users send in the message.txt file
def inbox():
    d = users()
    m = messages()
    for k in m.keys():
        sentto = m[k][0]
        sentfrom = m[k][1]
        msg = m[k][2]
        if sentto == CLIENT_ID:
            sendname = d[sentfrom][0]
            print(sendname + ' said: ' + msg +'\n')


#this handles new connections via threading
def handler(clientsocket, clientaddr):
    print('New user has entered the room: {}'.format(clientaddr))
    print('In chat commands: message,checkmessages,leave')
    while 1:
        data = recv_all(clientsocket)
        data = data.replace('.','')
        if not data:
            break
        else:
            user,message = data.split('m`')
            print(user+' says: ')
            print(message)
            msg = 'Message Sent'
            msg = msg + term
            ecmsg=msg.encode('ascii')
            clientsocket.sendall(ecmsg)
    clientsocket.close()
    
#the server waits for a message from the client
def server(host,port):
    purpose = ssl.Purpose.CLIENT_AUTH
    context = ssl.create_default_context(purpose, cafile=cafile)
    context.load_cert_chain(certfile)
    
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((host,port))
    listener.listen(1)
     
    while 1:
        print('Server is listening for connections\n')
        raw_sock, address = listener.accept()
        ssl_sock = context.wrap_socket(raw_sock, server_side=True)
        new_thread = threading.Thread(target=handler,args=(ssl_sock,address))
        new_thread.start()
        #thread.start_new_thread(handler,(ssl_sock, address))
    serversocket.close() 
        
        
    



#used to handle the data being sent from the server to the client
def recv_all(ssl_sock):
    commsg = ''
    message = ''
    while term not in message:
        commsg = ssl_sock.recv(4096)
        commsg = commsg.decode('ascii')
        message += commsg
    return message

#this will allow a new user to register
def begin():
    d = users()
    p = passwords()
    user = []
    puser = []
    print('Would you like to 1)Sign In or 2)Sign Up?')
    choice = input()
    if choice == '1':
        signin()
    elif choice == '2':
        print('Enter a user ID number: ')
        user_id = input()
        if user_id in d.keys():
            print('This user id already exists try again.')
            begin()
        else:
            print('Enter a user name: ')
            user_name = input()
            user.append(user_name)
            status = 'Offline'
            user.append(status)
            d[user_id] = user
            with open('database.txt','w+')as f:
                for k,v in d.items():
                    f.write(k + ':' + ':'.join(v) + '\n')
            print('Enter your password: ')
            user_pwd = input()
            puser.append(user_pwd)
            p[user_id] = puser
            with open('passwords.txt','w+') as j:
                for k,v in p.items():
                    j.write(k +':'+':'.join(v) + '\n')
            print('User successfully created, please sign in.')
            signin()
        
    else:
        print('Whoops try again!')
        begin()
        
    
                    
#check if the user is authorized, ie. in the database. Change their status to online
def signin():
    d = users()
    p = passwords()
    user = []
    print("Please enter your unique User ID number: ")
    user_id = input()
    global CLIENT_ID
    CLIENT_ID = user_id
    print("Please enter your password: ")
    user_pwd = input()
    if not user_id in d.keys():
        print("This user is not authorized to use Janelle Messenger!.")
        print("\n")
        signin()
    elif p[user_id][0] != user_pwd:
        print("This is an incorrect password")
        print("\n")
        signin()
        
    #change user status to online
    else:
        user_name = d[user_id][0]
        global CLIENT_NAME
        CLIENT_NAME = user_name
        user.append(user_name)
        status = 'Online'
        user.append(status)
        d[user_id] = user
        print('\n')
        print('Welcome!')
        print('\n')
        print('User Id: ' + user_id + ' Username:'+user_name+' Status:'
        + status)
        with open("database.txt", "w+")as f:
            for k,v in d.items():
                f.write(k + ":" + ":".join(v) + "\n")
        #this checks for messages
        #goes through message database and prints off messages for client
        #if user has no messages no message will appear
        print("-----******-----")
        print('Inbox: ')
        inbox()
        print("-----******-----")
                
        
        print("\nWaiting for next command: ")


#list users and their status
def listusers():
    d = users()
    for k in d.keys():
        print('ID:' + k + ' Username:' + d[k][0] + ' Status:'+d[k][1])
        
    print("\nWaiting for next command: ")

#this will send a user a message if they are online or offline
#user will get message when they sign on and if the use checkmessages while in chat
#logic here is only to be used when the user is offline
def sendMsg():
    d = users()
    print('Please enter the ID of the user you would like to message.')
    chat_id = input()
    print('Your message: ')
    text = input()
    if not chat_id in d.keys():
        print("This user is not authorized to use Janelle Messenger!.")
        print("\n")
        print('Do you want to try again? Y or N')
        selection =  input()
        if selection in['y','Y']:
            sendMsg()
        else:
            print('Continue..')
    else:
        #creates a random int from 1-100 for message id
        msgid = randint(1,100)
        f = open('messages.txt','a')
        #message is saved to message database
        f.write("{}:".format(msgid) + chat_id + ":" + CLIENT_ID + ":" + text + "\n")
        print("Your message has been sent.")
        print('Continue...')
        
        
        


#Allow user to signout, set status to offline
def signout():
    d = users()
    user = []
    print('Signed out: ')
    user_id = CLIENT_ID
    user_name=d[user_id][0]
    user.append(user_name)
    status = 'Offline'
    user.append(status)
    d[user_id] = user
    with open("database.txt", "w+")as f:
        for k,v in d.items():
            f.write(k+ ":" + ":".join(v) + "\n")
    print('User Id: ' + user_id + ' Username:'+user_name+' Status:'
            + status)
    #i enforce a sign in so users can't access data when not signed in
    print('\nPlease sign in to continue using messenger :)\n')
    signin()
        
#exit the program
def leave():
    #it is a nice practice to set the user to be offline when they close the program :)
    d = users()
    user = []
    print('Signed out: ')
    user_id = CLIENT_ID
    user_name=d[user_id][0]
    user.append(user_name)
    status = 'Offline'
    user.append(status)
    d[user_id] = user
    with open("database.txt", "w+")as f:
        for k,v in d.items():
            f.write(k+ ":" + ":".join(v) + "\n")
    print('User Id: ' + user_id + ' Username:'+user_name+' Status:'
            + status)
    exit(0)


#opens and reads from the user data base (userid:username:status)
def users():
    d = {}
    f=open("database.txt","r")
    for user in f:
        user=user.strip()
        ID,name = user.split(":",1)
        d[ID]=name.split(":",2)
    return d
           
#opens and reads from the message database (msgid:sentto:sentfrom:msg)
def messages():
    m = {}
    f=open("messages.txt","r")
    for user in f:
        user=user.strip()
        ID,name = user.split(":",1)
        m[ID]=name.split(":",3)
    return m

def passwords():
    p = {}
    f=open("passwords.txt","r")
    for user in f:
        user=user.strip()
        ID,name = user.split(":",1)
        p[ID]=name.split(":",1)
    return p

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=2015,
    help='TCP port (default 2015)')
    parser.add_argument('host', help='hostname or IP address')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

