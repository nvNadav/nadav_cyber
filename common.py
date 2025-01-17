import sys
def common(file_name,N):
    dic = {}
    try:
        # Open the file in read mode
        with open(file_name, "r") as file:
            # Read the contents of the file, remove trailing newlines, and split by spaces
            words = file.read().strip("\n").split()

            # Count the occurrences of each word in the file
            for word in words:
                if word in dic:
                    dic[word] += 1  
                else:
                    dic[word] = 1
    
        # Sort the dictionary by word frequency in descending order
        sorted_dic = (sorted(dic.items(), key=lambda x: x[1], reverse=True))

        key_only =[x[0] for x in sorted_dic]

        print (key_only[:N])

    except Exception as error:
        print (error)
