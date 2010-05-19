declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
%tree = type {%tree,i32,%tree}*
define i32 @main() {
entry:
%v_0 = alloca %tree
%t1 = call noalias i8* @calloc(i32 24,i32 1) nounwind
%t0 = bitcast i8* %t1 to %tree
store %tree %t0, %tree* %v_0
%t5 = load %tree* %v_0
%t4 = getelementptr %tree %t5, i32 0, i32 1
%t3 = load i32* %t4
%t2 = add i32 1 , %t3
store i32 %t2, i32* %t4
%t9 = load %tree* %v_0
%t8 = getelementptr %tree %t9, i32 0, i32 1
%t7 = load i32* %t8
call void @printInt (i32 %t7)
ret i32 0
}
