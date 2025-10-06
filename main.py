KEY = 3
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print(letters[(letters.find("Z")+3) % len(letters)] )
inp = input()
output = ""
for i in range(0, len(inp)):
    output += letters[(letters.find(inp[i])+3 ) % len(letters) ]
print(output)


