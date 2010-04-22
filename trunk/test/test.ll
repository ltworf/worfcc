declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
define i32 @main() {
entry:
%v_0 = alloca i32
store i32 0, i32* %v_0
%t3 = call i32 @readInt ()
store i32 %t3, i32* %v_0
%t5 = load i32* %v_0
call void @printInt (i32 %t5)
ret i32 0
}
