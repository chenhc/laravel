#include<iostream>

using namespace std;

long fib(long);

int main(void)
{
    long a, n;
    while (cin >> n)
        cout << fib(n) << endl;

}

long fib(long n)
{
    if (n == 0 || n == 1) 
        return n;
    else
        return fib(n-1) + fib(n-2);
}
