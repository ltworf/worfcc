int main () {
    
    int a=4;
    printInt(a);
    
    {
        int a=12;
        printInt(a);
    }
    printInt(a);
    
    return a;
}