/*lolo*/
int main() {
    boolean a=false;
    
    //printBool(!fazzo());
    printBool(fazzo() && !fazzo() || !fazzo());
    
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
