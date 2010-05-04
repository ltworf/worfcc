declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
define i32 @main() {
entry:
%v_0 = alloca 128
store 128 0, 128* %v_0
ret i32 0
}
