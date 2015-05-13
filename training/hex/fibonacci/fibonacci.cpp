#include <iostream>

using namespace std;

class BigInterge {
public:
	BigInterge() { length = 0; }
	void set(int Interge);
	BigInterge Add (BigInterge bigInterge);
	void out();
protected:
	int num[50];
	int length;
};


void BigInterge::set(int Interge) {
	length = 0;
	if (Interge == 0) {
		num[0] = 0;
		length++;
	}
	else {
		while (Interge > 0) {
			num[length++] = Interge%10;
			Interge /= 10;
		}
	}

}

void BigInterge::out() {
	for (int i = this->length-1; i >= 0; --i) {
		cout << this->num[i];
	}
}

BigInterge BigInterge::Add(BigInterge bigInterge) {
		BigInterge result;
		int a_length = this->length;
		int b_length = bigInterge.length;
		int carry = 0;
		int cur = 0;
		int temp_result;
		while (a_length > 0 && b_length > 0) {
			temp_result = (this->num[cur] + bigInterge.num[cur] + carry);
			result.num[cur++] = temp_result % 10;
			carry = temp_result / 10;
			a_length--;
			b_length--;
		}
		while (a_length > 0) {
			temp_result = (this->num[cur] + carry);
			result.num[cur++] = temp_result % 10;
			carry = temp_result / 10;
			a_length--;
		}
		while (b_length > 0) {
			temp_result = (bigInterge.num[cur] + carry);
			result.num[cur++] = temp_result % 10;
			carry = temp_result / 10;
			b_length--;
		}
		if (carry == 1) {
			result.num[cur++] = 1;
		}
		result.length = cur;
		return result;			
}

BigInterge fib[100];
int main()
{
	fib[0].set(0);
	fib[1].set(1);
	for (int i = 2; i < 100; ++i)
	{
		fib[i] = fib[i-1].Add(fib[i-2]);
	}
	int T;
	while (cin >> T) {
		fib[T].out();
		cout << endl;
	}
	return 0;
}
