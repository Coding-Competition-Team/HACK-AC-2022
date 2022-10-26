flag = "[REDACTED]"

arr = []
for ch in flag:
    tmp = str(ord(ch)) #ASCII value of ch as a string
    tmp = tmp.zfill(3) #Pad with "0"
    tmp = tmp[::-1] #Reverse
    arr.append(tmp)

enc = ""
for chunk in arr:
    a = int(chunk[0]) + 1 #a is an int
    b = chunk[1:] #b is a string
    enc += (a * b + "-")
enc = enc[:-1] #Remove trailing dash

print(enc)
