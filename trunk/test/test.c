struct Node {
  tree left;
  int val;
  tree right;
};

typedef struct Node *tree;

int main () {
    tree n= new Node;
    
    n->val++;
    printInt(n->val);
    
    return 0;
}
    

    