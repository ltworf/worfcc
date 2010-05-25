/* */
int main() {

for(int i = 0; i < 5; i++) {
    if(i == 3)
        continue;
    printInt(i);
}
  
  int i=0;
  while (i<5) {
    if (i==3) continue;
    printInt(i);
    i++;
  }
  
  return 0;
}