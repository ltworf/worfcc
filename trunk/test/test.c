/* */
typedef struct Node *list;

struct Node {
  int elem;
  list next;
};


int main() {
  cons(1+1+1+1+1+1+1,(list)null)->elem;
  return 0;
}

list cons (int x, list xs) {
  list n;
  n = new Node;
  n->elem = x;
  n->next = xs;
  return n;
}
