import socket
from threading import Thread
import random

server =  socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ip_address = '127.0.0.2'
port = 8001

server.bind((ip_address,port))
server.listen()

list_of_clients = []
nicknames =[]

print("Server has started....")

questions = [
    "What is the Italian word for PIE? /n a.Mozareela/n b.Pasty/n c.Patty/n d.Pizza",
    "Water boils at 212 Units at which scale? /n a.Fahrenheit/n b.Celsius/n c.Rankine/n d.Kelvin",
    "Which sea creature has three hearts? /n a.Dolphin/n b.Octopus/n c.Walrus/n d,Seal",
    "How many bones does an adult human have? /n a.206/n .b208/n .c201/n d.196",
    "What is the capital of France? /n a.Berlin/n b.Madrid/n c.Paris/n d.Rome",
    " What is the chemical symbol for water? /n a.CO2/n b.O2/n c.H2O/n d.H2O2"
]

answers = ['d','a','b','a','c','c']








def clientthread(conn,nickname):
    score = 0
    conn.send("Welcome to this chatroom!".encode('utf-8'))
    conn.send("You will recieve a question. The answer to that question should be one of a,b,c,d".encode('utf-8'))
    conn.send("Good Luck!/n/n".encode('utf-8'))
    index,question,answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answers:
                    score+=1
                    conn.send(f"Bravo! Your score is {score}/n/n".encode('utf-8'))
                else:  
                    conn.send("Incorrect answer! Better luck next time!/n/n".encode('utf-8'))
                remove_question(index)
                index,question,answer = get_random_question_answer(conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue    
            


def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions)-1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index,random_question,random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def broadcast(message,connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                remove(clients)

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)



while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined!".format(nickname)
    print(message)
    broadcast(message,conn)  
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()





