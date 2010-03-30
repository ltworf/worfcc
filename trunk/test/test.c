int main () {
    
    int a;
    while ((a=readInt())<100) {
        printString("ancora no");
    }
    
    if (a%2==0) {
    
        printString("pari");
        return 0;
    } else {
        printString("dispari");
        return 0;
    }
    
    
       
}