/*lolo*/
int main() {
    int a=10;
    printInt(a);
    
    {
        int a=a+1;
        
        printInt(a);
        a=15;
        printInt(a);
    }
    
    printInt(a);
    
    return 0;
    
}