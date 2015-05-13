import java.util.Scanner;
public class fibonacci {
    
	public static void main(String[] args) {
	Scanner input=new Scanner(System.in);
	System.out.println("Enter n(n>=2)");
	int n=input.nextInt();
	int[] List=new int[n];
	List[0]=0;
	List[1]=1;
	for(int i=2;i<n;i++){
	List[i]=List[i-1]+List[i-2];
	
	}System.out.println(List[n-1]);
	}
}

