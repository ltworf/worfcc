declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
define i32 @main() {
entry:
%t0 = icmp eq i1 true , true
br i1 %t0 , label %if_0 , label %else_0
if_0:
call void @printInt (i32 42)
br label %endif_0
else_0:
br label %endif_0
endif_0:
ret i32 0
}
