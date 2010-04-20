declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
@const_0 = internal constant [5 x i8] c"suca\00"
define i32 @main() {
entry:
%t1 = bitcast [5 x i8]* @const_0 to i8*
call void @printString (i8* %t1)
%t3 = call i32 @add (i32 5,i32 10)
call void @printInt (i32 %t3)
ret i32 0
}
define i32 @add(i32 %par_1,i32 %par_0) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%v_1 = alloca i32
store i32 %par_1, i32* %v_1
%t1 = load i32* %v_0
%t2 = load i32* %v_1
%t0 = add i32 %t1 , %t2
ret i32 %t0
}
