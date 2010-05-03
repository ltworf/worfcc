declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
define i32 @main() {
entry:
%v_0 = alloca i32
store i32 0, i32* %v_0
br label %expr_0
while_0:
%t2 = load i32* %v_0
call void @printInt (i32 %t2)
br label %expr_1
while_1:
%t4 = call i32 @readInt ()
%t3 = icmp eq i32 %t4 , 0
br i1 %t3 , label %if_2 , label %else_2
if_2:
br label %endwhile_1
br label %endif_2
else_2:
br label %endif_2
endif_2:
br label %expr_1
expr_1:
%t7 = load i32* %v_0
%t6 = icmp slt i32 %t7 , 50
br i1 %t6 , label %while_1 , label %endwhile_1
endwhile_1:
br label %expr_0
expr_0:
%t11 = load i32* %v_0
%t10 = add i32 1 , %t11
store i32 %t10, i32* %v_0
%t9 = icmp slt i32 %t11 , 40
br i1 %t9 , label %while_0 , label %endwhile_0
endwhile_0:
ret i32 0
}
