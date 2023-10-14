import socket


BUF_SIZE = 1024
new_message = True
full_message = ""


#HTTP using a raw TCP socket
#We will obtain a simple html file which is available at http://example.com/
#You can check the content by accessing this page in your web browser.


def make_the_connection(port = 80,address = 'example.com'):
    # create a socket object(connection)
    con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    con.connect((address, port))
    return con


def get_message_length(decaded_data:str) -> int:
    #get the length of the message from the HTTP header and add rest of the message to the full message
    global full_message
    head_items_dictionary = dict() 
    head , body = decaded_data.split("\n\r\n",1)
    head_items = [i for i in head.split("\r\n")]
    
    full_message += body
    
    for i in  head_items[1:]:
        items = i.split(":")
        head_items_dictionary[items[0]]=items[1]     
    return int(head_items_dictionary['Content-Length']) , head
        
#HTTP GET request is specific:
#1. One space between GET and path, and another one space between path and version
#2. \n newline at the end of first line.
#3. Additional headers in subsequent lines.
#4. The end of message must be marked with two newline characters 
#Additional headers can be included. (You can find some options using your browsers Network Monitor tool)
message = "GET / HTTP/1.1\nHost:example.com\nConnection:close\n\n"

con = make_the_connection()
con.send(bytes(message,"utf-8"))
print("msg sent")

while True:
    data = con.recv(BUF_SIZE)
    decaded_data = data.decode("utf-8")
    if new_message:
        message_length , head = get_message_length(decaded_data)
        new_message = False

    else:
        full_message += decaded_data
    
    if message_length <= len(full_message):
        print(head)
        con.close()
        break

print("-"*100)
print(full_message)

#Here, we do not retreive the entire file.
#We are happy with only first part of the file. 

#Task 1:
#It is an exercise for you to retreive entire file as chunks.
#If needed, you can just observe the Content-Length in the Response header, 
#Then retreive the entier file as suited. (Either expand BUF_SIZE or receive and print as chunks)

#Expected output: HTTP/1.1 200 OK with additional headers, 
#Followed by \n\n (Two new lines to mark the end of the header, and then the content)
#Content is an html file which begin with "<!doctype html>"

#Task 2:
#Verify / is the same path as /index.html by changing the path

#Task 3: 
#Try receiving non existant file. like /obviously-nonexistant instead of /
#You should receive HTTP/1.1 404 Not Found

#Task 4: 
#Try changing the HTTP version to 2 instead of 1.1
#You might receive HTTP/1.0 505 HTTP Version Not Supported
#This means server is old-style. More modern servers support version 2 which has lot of additional features.
