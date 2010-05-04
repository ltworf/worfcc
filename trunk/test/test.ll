declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
define i32 @main() {
entry:
%v_0 = alloca i32
store i32 3, i32* %v_0
%v_1 = alloca i1
store i1 false, i1* %v_1
%v_2 = alloca 128
store 128 %t2, 128* %v_2
%t4 = call 128 @f ()
store 128 %t4, 128* %v_2
call void @printInt (i32 %t6)
call void @printInt (i32 %t8)
%t10 = load i32* %v_0
call void @printInt (i32 %t10)
ret i32 0
}
define 128 @f() {
entry:
%v_0 = alloca 128
store 128 0, 128* %v_0
%t0 = load 128* %v_0
ret 128 %t0
}
