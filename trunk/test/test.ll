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
define i1 @not(i1 %par_0) {
entry:
%v_0 = alloca i1
store i1 %par_0, i1* %v_0
%t1 = load i1* %v_0
%t0 = add i1 %t1 , 1
ret i1 %t0
}
