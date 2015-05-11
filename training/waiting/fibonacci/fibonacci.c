#include <stdio.h>
#include <stdint.h>

uint64_t fibonacci(int n);
void main()
{
	uint64_t result = 0;
	int n;
	//uint64_t result=0;
	scanf("%d",&n);
	result=fibonacci(n);
	printf("%lu\n",result);
}

uint64_t fibonacci(int n)
{	
	int i=0;
	uint64_t result=0;
	uint64_t pre_result=0;
	uint64_t pree_result = 0;
	if(n==0) result=0;
	else if(n==1) result=1;
	else
	{
		for(i=2;i<=n;i++)
		{
			if(i==2)
			{
				pree_result = 0;
				pre_result = 1;
				result = pree_result + pre_result;
				pree_result = pre_result;
				pre_result = result;
			}
			else
			{
				result = pre_result + pree_result;
				pree_result = pre_result;
				pre_result = result;
			}
		}
	}
	return result;
}
