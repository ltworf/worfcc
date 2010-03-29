int main () {
    printString("Insert a ");
    int a=readInt();
      
    printInt(-fact(a));
           
    return a;
}

int fact(int n) {
    
    bool c=n<3;
    //printBool(c);
    
    if (n<3) {
        //printInt(n);
        return n;
    }
    else {
        ;
        //printInt(n);
        //n=n*fact(n-1);
        //printInt(n);
        //printString("no");
        //
        //return n;
    }
    return n*fact(n-1);
    
}