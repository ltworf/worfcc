int main () {
    
    if (!(1<3)) printString("<");
        if (!(1>3)) printString(">");
        if (!(1==3)) printString("==");
    if (!(1!=3)) printString("!=");
    if (!(1<=3)) printString("<=");
        if (!(1>=3)) printString(">=");
        
    if (!(3<=3)) printString("<=");
    if (!(3>=3)) printString(">=");
    
    return 3;
}