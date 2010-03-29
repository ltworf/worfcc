int main () {
    printString("Insert n to factorize");
    int a=readInt();
    printInt(fact(a));
       
       
    return a;
}

int fact(int n) {
    bool c=n<3;
    printBool(c);
    if (c) return n;
    else {
        printString("no");
        //return n*fact(n-1);
    }
    return 0;
}