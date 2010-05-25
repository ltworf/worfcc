target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32"declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
define i32 @main() {
entry:
%v_0 = alloca i32
store i32 0, i32* %v_0
br label %expr_0
while_0:
%t2 = load i32* %v_0
%t1 = icmp eq i32 %t2 , 3
br i1 %t1 , label %if_1 , label %else_1
if_1:
br label %continue_0
br label %endif_1
else_1:
br label %endif_1
endif_1:
%t5 = load i32* %v_0
call void @printInt (i32 %t5)
br label %continue_0
continue_0:
%t7 = load i32* %v_0
%t6 = add i32 1 , %t7
store i32 %t6, i32* %v_0
br label %expr_0
expr_0:
%t9 = load i32* %v_0
%t8 = icmp slt i32 %t9 , 5
br i1 %t8 , label %while_0 , label %endwhile_0
endwhile_0:
%v_1 = alloca i32
store i32 0, i32* %v_1
br label %expr_2
while_2:
%t13 = load i32* %v_1
%t12 = icmp eq i32 %t13 , 3
br i1 %t12 , label %if_3 , label %else_3
if_3:
br label %expr_2
br label %endif_3
else_3:
br label %endif_3
endif_3:
%t16 = load i32* %v_1
call void @printInt (i32 %t16)
%t18 = load i32* %v_1
%t17 = add i32 1 , %t18
store i32 %t17, i32* %v_1
br label %expr_2
expr_2:
%t20 = load i32* %v_1
%t19 = icmp slt i32 %t20 , 5
br i1 %t19 , label %while_2 , label %endwhile_2
endwhile_2:
ret i32 0
}
