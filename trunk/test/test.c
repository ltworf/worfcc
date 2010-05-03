/* allow comparing booleans. */

int main() {
    int i=0;
    while (i++<40) {
        
        printInt(i);
        while (i<50) {
            if (readInt()==0) break;
        }
        
    }
    return 0;
    
}