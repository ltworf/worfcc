declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
define i32 @main() {
entry:
%v_0 = alloca i32
store i32 0, i32* %v_0
%v_1 = alloca i32
store i32 0, i32* %v_1
%t3 = load i32* %v_0
call void @printInt (i32 %t3)
%t5 = load i32* %v_1
call void @printInt (i32 %t5)
br label %expr_0
while_0:
%t7 = load i32* %v_1
%t6 = add i32 1 , %t7
store i32 %t6, i32* %v_1
%t9 = load i32* %v_0
%t8 = sub i32 %t9 , 1
store i32 %t8, i32* %v_0
%t11 = load i32* %v_0
call void @printInt (i32 %t11)
%t13 = load i32* %v_1
call void @printInt (i32 %t13)
br label %expr_0
expr_0:
%t15 = load i32* %v_1
%t14 = icmp slt i32 %t15 , 100
br i1 %t14 , label %while_0 , label %endwhile_0
endwhile_0:
ret i32 0
}
