int main () {
    double r;
    r=readDouble();
    
    r=dd(r);
    printDouble(r);
    return 0;
}

double dd(double n) {
    return n;
}

/*
double dfac(double n) {
    if (n == 0.0)
      return 1.0;
    else
      return n * dfac(n-1.0);
}*/