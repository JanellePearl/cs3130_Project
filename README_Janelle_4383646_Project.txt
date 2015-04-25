CS3130 Project
Janelle Montgomery
April/24/2015


This project builds off of several lab assignments that we have had in CS3130. The main goal was to combine many components of networking into one program. In this program it makes use of TCP, Sockets, SSL, as well as a database and threading.

This program is intended for a user to login or sign up for Janelle's Messenger. Once they are logged on the user can check to see who is online, private message a user, join the global chatroom, or leave/signout of the program.

The commands that are used are numerical so 1-6.

If a user chooses to enter the global chatroom they will see who is logs in while they are on as well as any conversation that occurs while they are on. I thought it would be handy to have a few key words while in the chat session. This means you must keep in mind that these are key words while in the chat. Of course with a GUI this problem would be remedied. If you type 'checkmessages' this will show you your Inbox in case someone has private messaged you while you were in chat. If you type 'message', then you can message a user whether they are online or not. If you type 'leave' you will be logged out of the program and the chat room will be notified that you have left.

The neat thing about my chat room is you can open up as many terminal windows as you like and become a client(user).

To get the program started you will need to start the server.

To do this you will type:
python3.4 jmsg2.py server localhost

Also start up a client:
python3.4 jmsg2.py client localhost

So in the command line you must provide client/server as well as the address that you wish to use. Localhost is fitting.
NOTE: SSL does not seem to work unless you are specifically using python3.4, so it is important to make sure you are using this to run the program.

Users already in the database that you can message and log in as are:
id:1234 pass:hello <Janelle>
id:1616 pass:hello1 <Brittni>
id:2345 pass:hello2 <Mitch>

Git Url: https://github.com/JanellePearl/cs3130_Project
