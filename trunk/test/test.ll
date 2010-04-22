declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
define i32 @main() {
entry:
%v_0 = alloca i32
store i32 10, i32* %v_0
%t2 = load i32* %v_0
call void @printInt (i32 %t2)
%v_1 = alloca i32
%t4 = load i32* %v_0
%t3 = add i32 %t4 , 1
store i32 %t3, i32* %v_1
%t7 = load i32* %v_1
call void @printInt (i32 %t7)
store i32 15, i32* %v_1
%t11 = load i32* %v_1
call void @printInt (i32 %t11)
%t13 = load i32* %v_0
call void @printInt (i32 %t13)
ret i32 0
}
