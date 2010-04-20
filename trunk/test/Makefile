all: clean assemble link run

clean:
	rm -f *.bc a.out*

assemble:
	llvm-as test.ll 
	llvm-as runtime.ll


link:
	llvm-ld *.bc

run:
	./a.out
