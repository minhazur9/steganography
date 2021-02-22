"""
Created on Fri May  8 18:42:44 2020

"""

from PIL import Image, ImageTk
import random 
import tkinter as tk
from tkinter import Label, Entry
from tkinter.filedialog import askopenfilename, asksaveasfilename


def open_file():
    global img
    img = Image.open(askopenfilename(filetypes=(("Image Files", "*.jpg *.jpeg *.png *.tiff"),)))
    frame.destroy()
    resized = img.resize((400,400))
    canvas.image = ImageTk.PhotoImage(resized)
    canvas.create_image(50,20, image=canvas.image, anchor='nw')

def encode_file():
    if(img):
        global msg, password
        popup = tk.Toplevel()
        popup.title("")
        popup.geometry("300x80")
        popup.resizable(False,False)
        msg_label = Label(popup, text="Secret Message")
        msg = Entry(popup)
        password_label = Label(popup, text="Password")
        password = Entry(popup, show="*")
        confirm_button = tk.Button(popup, text="Confirm", padx=1, pady=1, fg="white", bg="green", command=confirm_secret)
        msg_label.grid(row=0,column=0)
        msg.grid(row=0,column=1)
        password_label.grid(row=1,column=0)
        password.grid(row=1,column=1)
        confirm_button.grid(row=2, column=1)
        popup.mainloop()
        # encode(msg,"Cryptography is awesome")

def confirm_secret():
    encode(msg.get(),password.get())

def decode_file():
    global password, characters
    popup = tk.Toplevel()
    popup.title("")
    popup.geometry("300x80")
    popup.resizable(False,False)
    password_label = Label(popup, text="Password")
    password = Entry(popup, show="*")
    characters_label = Label(popup, text="Message Size")
    characters = Entry(popup)
    confirm_button = tk.Button(popup, text="Confirm", padx=1, pady=1, fg="white", bg="green", command=confirm_decode)
    password_label.grid(row=0,column=0)
    password.grid(row=0,column=1)
    characters_label.grid(row=1,column=0)
    characters.grid(row=1,column=1)
    confirm_button.grid(row=2, column=1)
    popup.mainloop()

def confirm_decode():
    print(password)
    decode(password.get(), int(characters.get()))

def encode(message,phrase):
    random.seed(phrase) # This will generate the seed based on the phrase  
    msgSize = len(message)*8 # This will be the maximum size of the message in bits
    l = list(range(msgSize)) # This will make a list numbered 1 to the size of the message in bits
    random.shuffle(l) #This will shuffle the list randomly based on the seed generated
    x = img.size[0] # The width of the image
    new = img.copy() # Copies the original image
    img.close() #Closes the original image
    px =  new.load()  #Loads up the new image
    charPos = 0 # Tracks the character position of the whole message
    bitPos = 0 # Tracks the bit position within the byte
    byteStr = '' # The binary representation of the current character
    for i in l: 
        if(charPos >= len(message)): # If the character position ends up going past the last character then stop iterating
            break
        if(bitPos >= 8):
            charPos += 1 
            bitPos = 0 
        if(bitPos >= 8 or bitPos == 0): # If its the first bit of a char
            byteStr = bin(ord(message[charPos]))[2:].zfill(8) # Get the binary representation of the current character
        bit = int(byteStr[bitPos])
        randy = (l[i])//x
        randx = (l[i])%x
        randCol = random.randint(0,2)
        p = px[randx,randy]
        r = p[0]
        g = p[1]
        b = p[2]
        if(randCol == 0):
            if(bit == 0):
                px[randx,randy] = (r & ~1,g,b)
            else:
                px[randx,randy] = (r | 1,g,b)  
        elif(randCol == 1):
            if(bit == 0):
                px[randx,randy] = (r,g & ~1,b)         
            else:
                px[randx,randy] = (r,g | 1,b)        
        else:
            if(bit == 0):
                px[randx,randy] = (r,g,b & ~1)    
            else:
                px[randx,randy] = (r,g,b | 1)      
        bitPos+=1
    filepath = asksaveasfilename(filetypes=(("Image Files", "*.png *.tiff" ),))  # To save in the computer
    new.save(filepath)
    global frame
    frame = tk.Frame(canvas,bg="white")
    frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.02)
    
def decode(password,size):
    random.seed(password) # This will generate the seed based on the phrase  
    msgSize = size*8 # This will be the maximum size of the message in bits
    l = list(range(msgSize)) # This will make a list numbered 1 to the size of the message in bits
    random.shuffle(l) #This will shuffle the list randomly based on the seed generated
    x = img.size[0] # The width of the image
    bitPos = 0
    byteStr = ''
    j = 0
    secretMessage = ''
    px = img.load()
    for i in l:
        randy = l[i]//x
        randx = l[i]%x 
        p = px[randx,randy]
        r = p[0]
        g = p[1]
        b = p[2]
        randCol = random.randint(0,2)
        if(randCol == 0):
            byteStr += bin(r)[-1]
        elif(randCol == 1):
            byteStr += bin(g)[-1]
        else:
            byteStr += bin(b)[-1]
        if(len(byteStr) >= 8):
            bitPos = 0
            secretMessage += chr(int(byteStr,2))
            byteStr = ''  
        bitPos += 1
        j+=1
    filepath = asksaveasfilename(filetypes=(("Text Files", "*.txt *.docx" ),)) 
    f = open(filepath, "w")
    f.write(secretMessage)
    f.close()

root = tk.Tk()
img = None
root.title("Steganography")
root.geometry("500x500")
root.resizable(False,False)
canvas = tk.Canvas(root,height=500, width=500)
canvas.pack()
frame = tk.Frame(canvas,bg="white")
frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.02)
open_file_button = tk.Button(canvas, text="Open File", padx=10, pady=5, fg="white", bg="green", command=open_file)
open_file_button.place(x=150,y=450)
encode_file_button = tk.Button(canvas, bg="#117ff5", fg="white", text="Encode File",padx=10,pady=5, command=encode_file)
encode_file_button.place(x=300,y=425)
decode_file_button = tk.Button(canvas, bg="#e81313", fg="white", text="Decode File",padx=10,pady=5, command=decode_file)
decode_file_button.place(x=300,y=463)
popup = None
msg = None
password = None
characters = None
root.mainloop()

# decode(filedialog.askopenfilename(),'cryptography is awesome')