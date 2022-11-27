#!/usr/ibn/env python3
class demo():
    def add(a,b,c):
        b = b*c
        print(b)
    def sub(a,b,c,d):
        b = b-c
        print(b)
    def __init__(self,b,c):
        self.b=b
        self.c=c
        print(f"{self.b + self.c}")
    def addition(b):
        print(f"{b.b + b.c}")

print("enter the choice: ")
ch = int(input(" "))
if ch ==1:
    b=int(input())
    c= int(input())
    obj = demo(b,c)
    obj.add(b,c)
elif ch == 2:
    b=int(input())
    c= int(input())
    d =int(input())
    obj = demo(b,c)
    obj.sub(b,c,d)