/*lolo*/
int main() {
    boolean a=false;
    
    printBool(1<0 || fazzo());
    
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
