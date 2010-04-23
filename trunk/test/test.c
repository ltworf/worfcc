/*lolo*/
int main() {
    int a=5;
    double b=9.1;
    int c;
    double d;
    //printBool(!fazzo());
    printInt(-a);
    printDouble(-b);
    printInt(-c);
    printDouble(-d);
    
    return 0;
    
}

boolean fazzo() {
    printString("lala");
    return false;
}

void printBool(boolean a) {
    if (a) printString("true");
    else printString("false");
    //return;
}
