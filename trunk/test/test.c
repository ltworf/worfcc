int main () {
    
    double a,b;
    
    if (a==b) a=b+1.0;
    else b=a+1.0;
    
    printDouble(dfac(10.0));
    return 3;
}

double dfac(double n) {
    if (n == 0.0)
      return 1.0;
    else
      return n * dfac(n-1.0);
}