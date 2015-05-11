#include<iostream>
using namespace std;
long fib(long);
int main(void)
{long a,n;
cout<<"Input an integer:";
a=fib(n);
cout<<"fibonacci("<<n<<")="<<a<<endl;
}
long fib(long n)
{if(n==0||n==1) 
return n;
else return fib(n-1)+fib(n-2);
}
