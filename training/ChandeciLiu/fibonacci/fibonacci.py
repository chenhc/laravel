#!/usr/bin/env python
# -*- encoding=utf8 -*-


# author liudongqiang 

def fibonacci(n):
    a,b = 0,1
    for i in range(n):
        a,b = b,a + b
    print b
if __name__ == '__main__':
    
    while True:
        n = raw_input()
        fibonacci(int(n))

