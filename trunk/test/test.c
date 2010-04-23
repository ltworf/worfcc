/*lolo*/
int main() {
    boolean a= 1<3 || 4>5;
    
    
    printBool(a);
    
    if (!a) {
        printString("sucuni");
    }
    boolean b=!a;
    if (!b) {
        printString("sucuni2");
    } else {printString("lolo");}
    
    return 0;
    
}

void printBool(boolean a) {
    if (a) printString("true");
    else printString("false");
    //return;
}

boolean not(boolean a) {
    if (a)
        return false;
    return true;
}
