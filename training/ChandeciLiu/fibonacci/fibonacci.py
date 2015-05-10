#!/usr/bin/env python
# -*- encoding=utf8 -*-


# author liudongqiang 

def fibonacci(n):
    a, b = 1, 0
    for i in range(n):
        a, b = b, a + b
    return b

if __name__ == '__main__':
    while True:
        try:
            n = raw_input()
        except EOFError:
            break
        print fibonacci(int(n))
