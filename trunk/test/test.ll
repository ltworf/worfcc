declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
define i32 @main() {
entry:
%v_0 = alloca {i32,[ 0 x {i32,[ 0 x double ]}* ]}*
%t2 = mul i32 100, 8	;Calculate the size of the memory for the array
%t3 = add i32 8,%t2	;Plus 8 bytes for the length
%t5 = call noalias i8* @calloc(i32 %t3,i32 1) nounwind
%t4 = bitcast i8* %t5 to {i32,[ 0 x {i32,[ 0 x double ]}* ]}*
%t6 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t4, i32 0, i32 0
store i32 100, i32* %t6	;stores the size of the array
%v_1 = alloca i32
store i32 0, i32* %v_1
%t13 = mul i32 100, 8	;Calculate the size of the memory for the array
%t14 = add i32 8,%t13	;Plus 8 bytes for the length
br label %ar_loop_expr_1
ar_loop_body_0:
%t7 = load i32* %v_1
%t16 = call noalias i8* @calloc(i32 %t14,i32 1) nounwind
%t15 = bitcast i8* %t16 to {i32,[ 0 x double ]}*
%t17 = getelementptr {i32,[ 0 x double ]}* %t15, i32 0, i32 0
store i32 100, i32* %t17	;stores the size of the array
%t11 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t4, i32 0, i32 1, i32 %t7
store {i32,[ 0 x double ]}* %t15, {i32,[ 0 x double ]}** %t11
%t8 = add i32 1 , %t7
store i32 %t8, i32* %v_1
br label %ar_loop_expr_1
ar_loop_expr_1:
%t9 = load i32* %v_1
%t10 = icmp slt i32 %t9 , 100
br i1 %t10 , label %ar_loop_body_0 , label %ar_loop_exit_2
ar_loop_exit_2:
store {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t4, {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_0
%t21 = load {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_0
%t22 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t21, i32 0, i32 1, i32 0
%t24 = load {i32,[ 0 x double ]}** %t22
%t25 = getelementptr {i32,[ 0 x double ]}* %t24, i32 0, i32 1, i32 0
store double 4.0, double* %t25
ret i32 0
}
