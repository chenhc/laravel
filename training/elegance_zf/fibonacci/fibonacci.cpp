#include <iostream>
using namespace std;
long f(long n)
{
	if(n==1) return 0;
	else
	{
		if(n==2) return 1;
		else
		{
			return f(n-1)+f(n-2);
		}
	}
}
int main ()
{
	int i;
	cout << "'0' stop" <<endl;
	cin >> i;
	while (i)
	{
		cout << i << ":" << f(i) <<endl;
	}
	return 0;
}
