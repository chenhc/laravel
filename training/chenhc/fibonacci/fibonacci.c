#include<stdio.h>
#include <stdint.h> 

uint64_t fibonacci(int n);

int main()
{
    int n;
    while (scanf("%d",&n) != EOF)
        printf("%lu\n", fibonacci(n));

    return 0;
}

uint64_t fibonacci(int n)
{
    if (n == 0)
        return 0;

    if (n == 1)
        return 1;

    uint64_t a=0;
    uint64_t b=1;
    uint64_t c;

    while (--n > 0)
    {
        c = a + b;
        a = b;
        b = c;
    }

    return c;
}
