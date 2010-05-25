target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32"declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
define i32 @main() {
entry:
%v_0 = alloca i32
store i32 8, i32* %v_0
br label %expr_0
while_0:
%t4 = load i32* %v_0
%t2 = add i32 5 , %t4
call void @printInt (i32 %t2)
%t6 = load i32* %v_0
%t5 = add i32 1 , %t6
store i32 %t5, i32* %v_0
br label %expr_0
expr_0:
%t8 = load i32* %v_0
%t7 = icmp slt i32 %t8 , 20
br i1 %t7 , label %while_0 , label %endwhile_0
endwhile_0:
ret i32 0
}
