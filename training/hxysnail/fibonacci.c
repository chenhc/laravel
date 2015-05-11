#include <stdio.h>

long long int fibonacci(int n){
	long long int f1 = 0;
	long long int f2 = 1;

	if(n==0) return f1;
	while(n>=1 && n){
		long long int temp = f2;
		f2 = f1 + f2;
		f1 = temp;
		n--;
	}
	return f1;
}

int main(){
	int n;
	while(~scanf("%d",&n)){
		long long int result;
		result = fibonacci(n);
		printf("%lld\n",result);
	}
}
