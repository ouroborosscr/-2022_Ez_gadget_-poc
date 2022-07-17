from urllib import parse

while 1:
    key=input("#")
    print(parse.quote(chr(ord(key[0]) - 1) + chr(ord(key[1]) + 31) + key[2::]))