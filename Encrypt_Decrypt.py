key=5
def Encryption(picture_name,file_name):
    with open(picture_name, "rb") as p:
        with open (file_name,"w")as f:
            while (byte := p.read(1)):
                byte=byte[0]
                byte=format(byte, '08b')

                f.write( ( bin ( int ( byte,2 )^key ) ) [2:] .zfill(8) ) # turning binary string to binary int, then we XOR, then turning it back to binary and removing '0b'

def Decryption (enc_file,dec_file):
    with open(enc_file, "r") as enc:
        encrypted_data = enc.read()  #a variable containnig  the whole binary text file

    with open(dec_file, "w") as dec:  
        for i in range(0, len(encrypted_data), 8): #loop for each byte
           
            binary_string = encrypted_data[i:i+8] # taking the 8 next bits

            encrypted_byte = int(binary_string, 2)
            
            decrypted_byte = encrypted_byte ^ key
            
            dec.write (( bin ( decrypted_byte ) ) [2:] .zfill(8))#turning int to binary then removing '0b'

            

Encryption(r"c:\Users\USER\Downloads\download (1).jpeg",r"c:\Users\USER\Downloads\bits_e.txt")

Decryption(r"c:\Users\USER\Downloads\bits_e.txt",r"c:\Users\USER\Downloads\bits_d.txt")