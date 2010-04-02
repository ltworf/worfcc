int main () {
    int a=readInt();
    if (3==a) printString("Hai scritto 3");
    else {
        printString("Hai scritto");
        printInt(a);
    }
    return 0;   
    
    
}

/*double dfac(double n) {
    return n*2.0;
}*/

/*
double dfac(double n) {
    if (n == 0.0)
      return 1.0;
    else
      return n * dfac(n-1.0);
}*/