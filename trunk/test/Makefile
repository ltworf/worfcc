all: clean assemble link run

clean:
	rm -f test.bc a.out*

assemble:
	llvm-as test.ll 


link:
	llvm-ld *.bc

run:
	./a.out
