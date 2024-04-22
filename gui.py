from rsa_encryption import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import sys
import base64

def str_to_base64(input_str):
    input_str_bytes = input_str.encode('latin1')
    base64_bytes = base64.b64encode(input_str_bytes)
    base64_str = base64_bytes.decode('latin1')
    return base64_str

def on_input_type_change(widgetHide,widgetShow):
    hideWidget(widgetHide)
    showWidget(widgetShow)

def hideWidget(widget):
    widget.grid_remove()

def showWidget(widget):
    widget.grid(row=6, column=1, pady=15, ipadx = 40)

def reset_label(window):
    fileLabel = tk.Label(window, text='                                                                                              ')
    fileLabel.grid(row=7, column=1, pady=15, ipadx = 40)

def start_encrypting(target64, inputType, input, key, encodingUsed):
    cyphertext = "ERROR"
    fileContent = cyphertext
    fileContentIsBinary = False

    if (len(input) == 0 or len(key) == 0):
        return fileContent, fileContentIsBinary
    
    if inputType == 'Text': 
            fileContent = rsa_string_encrypt(input, key, 1)
            fileContentIsBinary = False
    else:
        if os.path.splitext(input)[1] == ".txt": #Berarti  -> enkripsi isinya, jangan filenya
            
            with open(input,"r", encoding=encodingUsed) as inputFile:
                plainTextInput = inputFile.read()
            
            fileContent = rsa_string_encrypt(plainTextInput, key, 1)
            fileContentIsBinary = False

        else: 
            with open(input,"rb") as inputFile:
                binaryInput = inputFile.read()
            fileContentIsBinary = True
            plainTextInput = binaryInput.decode(encodingUsed)
            fileContent = rsa_string_encrypt(plainTextInput, key, 1)
    
    cyphertext = str_to_base64(fileContent)

    # DIMUNCULIN DI TEXTBOX

    target64.config(state='normal')
    target64.delete(1.0, tk.END) 
    target64.insert(tk.END, cyphertext)

    # BIAR GAK DIGANTI USER
    target64.config(state=tk.DISABLED)

    return fileContent, fileContentIsBinary

def start_decrypting(target, inputType, input, key, encodingUsed):
    plaintext = "ERROR"
    fileContent = plaintext
    fileContentIsBinary = False

    if (len(input) == 0 or len(key) == 0):
        return fileContent, fileContentIsBinary
    
    if inputType == 'Text': 
        fileContent = rsa_string_decrypt(input, key, 1)
        fileContentIsBinary = False
    else:
        if os.path.splitext(input)[1] == ".txt": #Berarti  -> enkripsi isinya, jangan filenya
            
            with open(input,"r", encoding=encodingUsed) as inputFile:
                plainTextInput = inputFile.read()
            
            fileContent = rsa_string_decrypt(plainTextInput, key, 1)
            fileContentIsBinary = False

        else: 
            with open(input,"rb") as inputFile:
                binaryInput = inputFile.read()
            fileContentIsBinary = True
            plainTextInput = binaryInput.decode(encodingUsed)
            fileContent = rsa_string_decrypt(plainTextInput, key, 1)

    # DIMUNCULIN DI TEXTBOX
    target.config(state='normal')
    target.delete(1.0, tk.END) 
    target.insert(tk.END, fileContent)

    # BIAR GAK DIGANTI USER
    target.config(state=tk.DISABLED)

    return fileContent, fileContentIsBinary

    
def main():    
    # Main Window
    window = tk.Tk()
    window.title("RSA CHAT GUI")
    defaultEncoding = "latin1"

    window_width = 1400
    window_height = 800
    
    window.minsize(window_width, window_height)
    window.maxsize(window_width, window_height)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    private_user1 = ''
    public_user1 = ''
    private_user2 = ''
    public_user2 = ''
    user1_know = False
    user2_know = False

    def keyGen(user):
        nonlocal private_user1
        nonlocal public_user1
        nonlocal private_user2
        nonlocal public_user2
        nonlocal user1_know
        nonlocal user2_know

        if user == 1:
            public_user1, private_user1 = generate_key(10, 10000000)
            user2_know =False

        elif user == 2:
            public_user2, private_user2 = generate_key(10, 10000000)
            user1_know = False

    def sendKey(user):
        nonlocal user1_know
        nonlocal user2_know

        if user == 1:
            user2_know = True

        elif user == 2:
            user1_know = True

    def save_public(user):
        nonlocal public_user1
        nonlocal public_user2

        outputFile = filedialog.asksaveasfile(mode="w",defaultextension=".txt",filetypes=[("Text files","*.*")])

        if user == 1:
            outputFile.write(public_user1)
        else:
            outputFile.write(public_user2)

    def save_private(user):
        nonlocal private_user1
        nonlocal private_user2

        outputFile = filedialog.asksaveasfile(mode="w",defaultextension=".txt",filetypes=[("Text files","*.*")])

        if user == 1:
            outputFile.write(private_user1)
        else:
            outputFile.write(private_user2)


    fileLabel = tk.Label(window, text='')
    fileLabel.grid(row=7, column=5, pady=15, ipadx = 40)

    fileLabe2 = tk.Label(window, text='')
    fileLabe2.grid(row=7, column=5, pady=15, ipadx = 40)

    # USER 1
    keyLabel = tk.Label(window, text="User 1")
    keyLabel.grid(row=0, column=1, pady=10)

    keyLabel = tk.Label(window, text="User 1 Key : ")
    keyLabel.grid(row=1, column=0, pady=10)
    
    keyButton = ttk.Button(window, text="Generate Key", command=lambda: keyGen(1))
    keyButton.grid(row=1, column=1, padx = 5, pady=11)
    sendKeyButton = ttk.Button(window, text="Send Key", command=lambda: sendKey(1))
    sendKeyButton.grid(row=1, column=2, padx = 5, pady=11)
    savePubButton = ttk.Button(window, text="Save Public Key", command=lambda: save_public(1))
    savePubButton.grid(row=2, column=1, padx = 5, pady=12)
    savePriButton = ttk.Button(window, text="Save Public Key", command=lambda: save_private(1))
    savePriButton.grid(row=2, column=2, padx = 5, pady=12)
    
    # USER 2
    keyLabel = tk.Label(window, text="User 2")
    keyLabel.grid(row=0, column=5, pady=10)

    keyLabel = tk.Label(window, text="User 2 Key : ")
    keyLabel.grid(row=1, column=4, pady=10)
    
    keyButton = ttk.Button(window, text="Generate Key", command=lambda: keyGen(2))
    keyButton.grid(row=1, column=5, padx = 5, pady=11)
    sendKeyButton = ttk.Button(window, text="Send Key", command=lambda: sendKey(2))
    sendKeyButton.grid(row=1, column=6, padx = 5, pady=11)
    savePubButton = ttk.Button(window, text="Save Public Key", command=lambda: save_public(2))
    savePubButton.grid(row=2, column=5, padx = 5, pady=12)
    savePriButton = ttk.Button(window, text="Save Public Key", command=lambda: save_private(2))
    savePriButton.grid(row=2, column=6, padx = 5, pady=12)

    

    # Nested Functions (We're bad at programming)
    currentFile1 = "Error"
    currentFile2 = "Error"
    encryptedUser1 = "Error"
    encryptedUser2 = "Error"
    decryptedUser1 = "Error"
    decryptedUser2 = "Error"
    isResultBinary1 = False
    isResultBinary2 = False

    def uploadFile(user): 
        nonlocal currentFile1
        nonlocal currentFile2
        nonlocal window


        filename = filedialog.askopenfilename()

        if user == 1:
            fileLabel1 = tk.Label(window, text=filename)
            fileLabel1.grid(row=7, column=1, pady=15, ipadx = 40)
            currentFile1 = filename
        else:
            fileLabel2 = tk.Label(window, text=filename)
            fileLabel2.grid(row=7, column=5, pady=15, ipadx = 40)
            currentFile2 = filename

    def handle_input(inputType, user):
        nonlocal currentFile1
        nonlocal currentFile2
        if inputType == 'Text':
            if user == 1:
                return inputText1.get()
            else:
                return inputText2.get()
        else:
            if user == 2:
                return currentFile1
            else:
                return currentFile2
            
    def handle_encrypt(target64, inputType, input, key, user):
        print(target64, inputType, input, key, user)
        nonlocal encryptedUser1
        nonlocal encryptedUser2
        nonlocal isResultBinary1
        nonlocal isResultBinary2
        nonlocal defaultEncoding

        if user == 1:
            encryptedUser1, isResultBinary1 = start_encrypting(target64, inputType, input, key, defaultEncoding)
        else:
            encryptedUser2, isResultBinary2 = start_encrypting(target64, inputType, input, key, defaultEncoding)

    def handle_decrypt(target, inputType, input, key, user):
        nonlocal decryptedUser1
        nonlocal decryptedUser2
        nonlocal isResultBinary1
        nonlocal isResultBinary2
        nonlocal defaultEncoding
        
        if user == 1:
            decryptedUser1, isResultBinary1 = start_decrypting(target, inputType, input, key, defaultEncoding)
        else:
            decryptedUser2, isResultBinary2 = start_decrypting(target, inputType, input, key, defaultEncoding)

        
    def on_save_button(user, fileContent):
        nonlocal encryptedUser1
        nonlocal encryptedUser2
        nonlocal decryptedUser1
        nonlocal decryptedUser2
        nonlocal isResultBinary1
        nonlocal isResultBinary2
        print(1, encryptedUser1, encryptedUser2)
        print(2, decryptedUser1, decryptedUser2)

        if fileContent == 'encrypt':
            if user == 1:
                if (isResultBinary1):
                    outputFile = filedialog.asksaveasfile(mode="wb",filetypes=[("All files","*.*")])
                else :
                    outputFile = filedialog.asksaveasfile(mode="wb",defaultextension=".txt",filetypes=[("Text files","*.txt*")])

                if type(encryptedUser1) == str:
                    outputFile.write(encryptedUser1.encode('latin1'))
                else:
                    outputFile.write(encryptedUser1)
            else:
                if (isResultBinary2):
                    outputFile = filedialog.asksaveasfile(mode="wb",filetypes=[("All files","*.*")])
                else :
                    outputFile = filedialog.asksaveasfile(mode="wb",defaultextension=".txt",filetypes=[("Text files","*.txt*")])

                if type(encryptedUser2) == str:
                    outputFile.write(encryptedUser2.encode('latin1'))
                else:
                    outputFile.write(encryptedUser2)
        elif fileContent == 'decrypt':
            if user == 1:
                if (isResultBinary1):
                    outputFile = filedialog.asksaveasfile(mode="wb",filetypes=[("All files","*.*")])
                else :
                    outputFile = filedialog.asksaveasfile(mode="wb",defaultextension=".txt",filetypes=[("Text files","*.txt*")])

                if type(decryptedUser1) == str:
                    outputFile.write(decryptedUser1.encode('latin1'))
                else:
                    outputFile.write(decryptedUser1)
            else:
                if (isResultBinary2):
                    outputFile = filedialog.asksaveasfile(mode="wb",filetypes=[("All files","*.*")])
                else :
                    outputFile = filedialog.asksaveasfile(mode="wb",defaultextension=".txt",filetypes=[("Text files","*.txt*")])

                if type(decryptedUser2) == str:
                    outputFile.write(decryptedUser2.encode('latin1'))
                else:
                    outputFile.write(decryptedUser2)


        
    # Input Text 1 & 2
    inputText1 = tk.StringVar()
    inputTextField1 = ttk.Entry(window, textvariable=inputText1)
    inputText2 = tk.StringVar()
    inputTextField2 = ttk.Entry(window, textvariable=inputText2)

    # Input File 1 & 2
    inputUploadButton1 = ttk.Button(window,text= "Upload", command=lambda:uploadFile())
    inputUploadButton2 = ttk.Button(window,text= "Upload", command=lambda:uploadFile())

    # Input Selection 1
    inputLabelType1 = tk.Label(window, text="Input Type User 1:")
    inputLabelType1.grid(row=4, column=0, pady=10)
    inputSelected1 = tk.StringVar()
    inputList = ["Text", "File" ]
    inputSelection1_1 = ttk.Radiobutton(window, text=inputList[0], variable= inputSelected1, value=inputList[0], command=lambda: (on_input_type_change(inputUploadButton1,inputTextField1), inputTextField1.grid(row=6, column=1, pady=15, ipadx = 40), reset_label(window)))
    inputSelection1_1.grid(row=4, column=1, pady=10)
    inputSelection2_1 = ttk.Radiobutton(window, text=inputList[1], variable= inputSelected1, value=inputList[1], command=lambda: (on_input_type_change(inputTextField1,inputUploadButton1), inputUploadButton1.grid(row=6, column=1, pady=15, ipadx = 40)))
    inputSelection2_1.grid(row=5, column=1, pady=15)

    inputLabelInput1 = tk.Label(window, text="Input User 1:")
    inputLabelInput1.grid(row=6, column=0, pady=5, ipadx = 40)

    # Input Selection 2
    inputLabelType1 = tk.Label(window, text="Input Type User 2:")
    inputLabelType1.grid(row=4, column=4, pady=10)
    inputSelected2 = tk.StringVar()
    inputList = ["Text", "File" ]
    inputSelection1_2 = ttk.Radiobutton(window, text=inputList[0], variable= inputSelected2, value=inputList[0], command=lambda: (on_input_type_change(inputUploadButton2,inputTextField2), inputTextField2.grid(row=6, column=5, pady=15, ipadx = 40), reset_label(window)))
    inputSelection1_2.grid(row=4, column=5, pady=10)
    inputSelection2_2 = ttk.Radiobutton(window, text=inputList[1], variable= inputSelected2, value=inputList[1], command=lambda: (on_input_type_change(inputTextField2,inputUploadButton2), inputUploadButton2.grid(row=6, column=5, pady=15, ipadx = 40)))
    inputSelection2_2.grid(row=5, column=5, pady=15)

    inputLabelInput2 = tk.Label(window, text="Input User 2:")
    inputLabelInput2.grid(row=6, column=4, pady=5, ipadx = 40)

    # Encrypt Button
    encryptButton1 = ttk.Button(window, text="Encrypt and Send", command=lambda: handle_encrypt(textBox641, inputSelected1.get(), handle_input(inputSelected1.get(), 1), public_user2, 1))
    encryptButton1.grid(row=8, column=1, pady=3)

    encryptButton2 = ttk.Button(window, text="Encrypt and Send", command=lambda: handle_encrypt(textBox642, inputSelected1.get(), handle_input(inputSelected2.get(), 2), public_user1, 2))
    encryptButton2.grid(row=8, column=5, pady=3)

    # Decrypt Button
    DecryptButton1 = ttk.Button(window, text="Decrypt", command=lambda: handle_decrypt(textBox1, inputSelected1.get(), handle_input(inputSelected1.get(), 1), private_user1, 1))
    DecryptButton1.grid(row=10, column=1, pady=3)

    DecryptButton2 = ttk.Button(window, text="Decrypt", command=lambda: handle_decrypt(textBox2, inputSelected2.get(), handle_input(inputSelected2.get(), 2), private_user2, 2))
    DecryptButton2.grid(row=10, column=5, pady=3)


    # USER 1
    # Result (Base64)
    textLabel = tk.Label(window, text="User 1 Encrypted Text (Base64):")
    textLabel.grid(row=9, column=4, pady=5, ipadx = 40)

    textBox641 = tk.Text(window, state=tk.DISABLED, height=10, width=20)
    textBox641.grid(row=9, column=5, columnspan=2, pady=5, ipadx=40)

    # Result User1 Decrypted
    textLabel = tk.Label(window, text="User 1 Decrypted Text:")
    textLabel.grid(row=11, column=4, pady=5, ipadx = 40)

    textBox1 = tk.Text(window, state=tk.DISABLED, height=10, width=20)
    textBox1.grid(row=11, column=5, columnspan=2, pady=5, ipadx=40)


    # USER 2
    # # Result
    # textLabel = tk.Label(window, text="User 2 Encrypted/Decrypted Text:")
    # textLabel.grid(row=10, column=0, pady=5, ipadx = 40)

    # textBox2 = tk.Text(window, state=tk.DISABLED, height=10, width=20)
    # textBox2.grid(row=10, column=1, columnspan=2, pady=5, ipadx=40)

    # Result (Base64)
    textLabel = tk.Label(window, text="User 2 Encrypted (Base64):")
    textLabel.grid(row=9, column=0, pady=5, ipadx = 40)

    textBox642 = tk.Text(window, state=tk.DISABLED, height=10, width=20)
    textBox642.grid(row=9, column=1, columnspan=2, pady=5, ipadx=40)

    # Result User2 Decrypted
    textLabel = tk.Label(window, text="User 1 Decrypted Text:")
    textLabel.grid(row=11, column=0, pady=5, ipadx = 40)

    textBox2 = tk.Text(window, state=tk.DISABLED, height=10, width=20)
    textBox2.grid(row=11, column=1, columnspan=2, pady=5, ipadx=40)


    

    # Save Button
    saveButtonMsg1 = ttk.Button(window, text="Save User 1 Encrypted Message", command=lambda: on_save_button(1, 'encrypt'))
    saveButtonMsg1.grid(row=12, column=5, pady=10)
    saveButtonMsg2 = ttk.Button(window, text="Save User 2 Encrypted Message", command=lambda: on_save_button(2, 'encrypt'))
    saveButtonMsg2.grid(row=12, column=1, pady=10)

    
    saveButtonDec1 = ttk.Button(window, text="Save User 1 Decrypted Message", command=lambda: on_save_button(1, 'decrypt'))
    saveButtonDec1.grid(row=12, column=6, pady=10)
    saveButtonDec2 = ttk.Button(window, text="Save User 2 Decrypted Message", command=lambda: on_save_button(2, 'decrypt'))
    saveButtonDec2.grid(row=12, column=2, pady=10)

    #RUN 
    window.mainloop()

if __name__ == '__main__':
    main()