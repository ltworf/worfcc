declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
define i32 @main() {
entry:
%v_0 = alloca i32*
store i32* %t0, i32** %v_0
%v_1 = alloca {i32,[ 0 x {i32,[ 0 x i32 ]}* ]}*
%t3 = mul i32 15, 8	;Calculate the size of the memory for the array
%t4 = add i32 8,%t3	;Plus 8 bytes for the length
%t6 = call noalias i8* @calloc(i32 %t4,i32 1) nounwind
%t5 = bitcast i8* %t6 to {i32,[ 0 x {i32,[ 0 x i32 ]}* ]}*
%t7 = getelementptr {i32,[ 0 x {i32,[ 0 x i32 ]}* ]}* %t5, i32 0, i32 0
store i32 15, i32* %t7	;stores the size of the array
%v_2 = alloca i32
store i32 0, i32* %v_2
%t14 = mul i32 15, 4	;Calculate the size of the memory for the array
%t15 = add i32 8,%t14	;Plus 8 bytes for the length
br label %ar_loop_expr_1
ar_loop_body_0:
%t8 = load i32* %v_2
%t17 = call noalias i8* @calloc(i32 %t15,i32 1) nounwind
%t16 = bitcast i8* %t17 to {i32,[ 0 x i32 ]}*
%t18 = getelementptr {i32,[ 0 x i32 ]}* %t16, i32 0, i32 0
store i32 15, i32* %t18	;stores the size of the array
%t12 = getelementptr {i32,[ 0 x {i32,[ 0 x i32 ]}* ]}* %t5, i32 0, i32 1, i32 %t8
store {i32,[ 0 x i32 ]}* %t16, {i32,[ 0 x i32 ]}** %t12
%t9 = add i32 1 , %t8
store i32 %t9, i32* %v_2
br label %ar_loop_expr_1
ar_loop_expr_1:
%t10 = load i32* %v_2
%t11 = icmp slt i32 %t10 , 15
br i1 %t11 , label %ar_loop_body_0 , label %ar_loop_exit_2
ar_loop_exit_2:
store {i32,[ 0 x {i32,[ 0 x i32 ]}* ]}* %t5, {i32,[ 0 x {i32,[ 0 x i32 ]}* ]}** %v_1
store i32* %t20, i32** %v_0
%v_3 = alloca i32*
store i32* %t21, i32** %v_3
ret i32 0
}
