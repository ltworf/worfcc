int main () {
    double a=0.0, b=1.0;
    
    if (a==b) printString("true");
    else printString("false");
    
    if (a!=b) printString("true");
    else printString("false");
    
    if (a>b) printString("true");
    else printString("false");
    
    if (a>=b) printString("true");
    else printString("false");
    
    if (a<b) printString("true");
    else printString("false");
    
    if (a<=b) printString("true");
    else printString("false");
    
    
    b=0.0;
    
    if (a==b) printString("true");
    else printString("false");
    
    if (a!=b) printString("true");
    else printString("false");
    
    if (a>b) printString("true");
    else printString("false");
    
    if (a>=b) printString("true");
    else printString("false");
    
    if (a<b) printString("true");
    else printString("false");
    
    if (a<=b) printString("true");
    else printString("false");
    
    return 1;
}

int fact(int n) {
    
    bool c=n<3;
   
    if (n<3) {
        //printInt(n);
        return n;
    }
    else {
        ;
    }
    return n*fact(n-1);
    
}

int test() {
    if (true)
        return 1;
    else;
        return 0; 
}