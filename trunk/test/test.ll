declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
define i32 @main() {
entry:
%v_0 = alloca i32*
store i32* 0, i32** %v_0
store i32* %t1, i32** %v_0
%v_1 = alloca i32*
store i32* %t2, i32** %v_1
ret i32 0
}
