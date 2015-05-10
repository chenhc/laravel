#include<stdio.h>
#include <stdint.h> 
uint64_t fibonacci(int n);

int main()
{
	int n;
	while(scanf("%d",&n))
		printf("%lu\n", fibonacci(n));
	return 1;
}

uint64_t  fibonacci(int n)
{
	if(n==0)
		return 0;
	if(n==1)
		return 1;
	uint64_t a=0;
	uint64_t b=1;
	uint64_t c;
	n=n-2;
	while(n>=0)
	{
		c=a+b;
		a=b;
		b=c;
		n--;
	}
	return c;
	
}
