#include <iostream>

using namespace std;

long f(long n)
{
    if (n == 0)
    {
        return 0;
    }
	else if(n==1)
    {
        return 1;
    }
    else if (n >= 2)
	{
        return f(n-1) + f(n-2);
	}
}

int main ()
{
	int i;
	while (cin>>i)
	{
		cout << f(i) <<endl;
	}

	return 0;
}
