t@git.coding.net:fasionchan/ilive.git
import java.util.Scanner
public class count{
   public static long num(int n){
         if(n<0)
                 return -1;
         else  if(n==0)
              ic   return 0;
         else  if(n==1)
                 return 1;
         else
                 return num(n-1)+num(n-2);
}
   public static void main (String[] args){
         System.out.println("Please enter a number:")
         Scanner scanner=new Scanner(System.in);
         int n= scanner.nextInt();
         System.out.println(num(n));
}
}
