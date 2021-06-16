# I used the following ressource to base my code on. I have modified the program to fit the needs of the assignment.
# https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2
import numpy as np
from PIL import Image
import os

#this will serve as the encoder function
def Encoder(file, message, destination):
    picture = Image.open(file, 'r')
    width = picture.width
    height = picture.height
    array = np.array(list(picture.getdata()))
#Account for RGBA
    if picture.mode == 'RGB':
        n = 3
    elif picture.mode == 'RGBA':
        n = 4

    pixels_ttl = array.size//n
#this code will tell us when we have reached the end of the message
    code = "3r9"
    message += code
#updating the message to binary and calculate the # of pixels needed
    bin_message = ''.join([format(ord(i), "08b") for i in message])
#print(bin_message)
    req_pixels = len(bin_message)
#check that number of pixels is good.
    if req_pixels > pixels_ttl :
        print("ERROR: The message is too large for this image, please shorten your message or provide a larger picture")
    else :
        #modify the least significant bit one by one
        index = 0
        for i in range(pixels_ttl) :
            #print("outter i", i, "\n")
            for j in range(0,n-1) :
                if index < req_pixels :
                    #print("inner i", i, "\n")
                    #print("j value", j, "\n")
                    array [i][j] = int(bin(array[i][j]) [2:9] +
                    bin_message[index], 2)
                    index += 1

        array = array.reshape(height, width, n)
        encoded_pict = Image.fromarray(array.astype('uint8'), picture.mode)
#saves the encoded image
        encoded_pict.save(destination)
#Function for decoding
def Decoder(file) :
#open the image
    picture = Image.open(file, 'r')
    array = np.array(list(picture.getdata()))
#see if it is RGB or RGBA
    if picture.mode == 'RGB':
        n = 3
    elif picture.mode == 'RGBA' :
        n = 4

    pixels_ttl = array.size//n
    hid_bits = ""
    for i in range(pixels_ttl) :
        for j in range(0, n-1) :
#this was used to test an error that I had hit
            #if i == pixels_ttl - 2000 :
                #print ("test")
                #print ("i ", i)
                #print("j ", j)
                #break
            hid_bits += (bin(array[i][j]) [2:][-1])

    hid_bits = [hid_bits[k:k+8] for k in range(0,len(hid_bits), 8)]

    message = ""
    for i in range(len(hid_bits)):
        if message [-3:] == "3r9":
            break
        else :
            message += chr(int(hid_bits[i], 2))
    if "3r9" in message:
        print("Message: ", message[:-3])
    else :
        print("Unable to find any hidden messages.")
#main function to run the program - calls the encoder and decoder depending on user inputs
def Stegonography():
    print("Please select an option:")
    print("Type 1 to Encode")
    print("Type 2 to Decode")
    print("Type 3 to Exit\n")
#Encoder gets called
    option = input()
    if option == '1' :
        print("Enter the path to the Image")
        file = input()
        if os.path.exists(file) != True :
            print('No such file found, closing the program.')
            exit()
        if not file.lower().endswith('.png') :
            print("Invalid file type. File must be a .png file. Closing program now.")
            exit()
        print("Type the message you would like to hide")
        message = input()
        print("Enter the destination path for the file")
        destination = input()
        if not destination.lower().endswith('.png') :
            print("Invalid file type. File must be a .png file. Encoding cancelled, please try again.")
            exit()
        Encoder(file, message, destination)
#Decoder is selected
    elif option == '2' :
        print("Enter the path to the Image")
        file = input()
        if os.path.exists(file) != True :
            print('No such file found, closing the program.')
            exit()
        if not file.lower().endswith('.png') :
            print("Invalid file type. File must be a .png file. Closing program now.")
            exit()
        Decoder(file)
#exit is selected
    elif option == "3" :
        exit()
#Invalid selection of options
    else :
        print("Invalid option, closing program")

if __name__ == "__main__":
    Stegonography()
