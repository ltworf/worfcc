target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32"declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
define i32 @main() {
entry:
%v_0 = alloca {i32,[ 0 x i32 ]}*
%t2 = mul i32 10, 4	;Calculate the size of the memory for the array
%t3 = add i32 8,%t2	;Plus 8 bytes for the length
%t5 = call noalias i8* @calloc(i32 %t3,i32 1) nounwind
%t4 = bitcast i8* %t5 to {i32,[ 0 x i32 ]}*
%t6 = getelementptr {i32,[ 0 x i32 ]}* %t4, i32 0, i32 0
store i32 10, i32* %t6	;stores the size of the array
store {i32,[ 0 x i32 ]}* %t4, {i32,[ 0 x i32 ]}** %v_0
%v_1 = alloca i32
store i32 0, i32* %v_1
br label %expr_0
while_0:
%t9 = load i32* %v_1
%t10 = load i32* %v_1
%t11 = load {i32,[ 0 x i32 ]}** %v_0
%t12 = getelementptr {i32,[ 0 x i32 ]}* %t11, i32 0, i32 1, i32 %t10
store i32 %t9, i32* %t12
%t14 = load i32* %v_1
%t13 = add i32 1 , %t14
store i32 %t13, i32* %v_1
br label %expr_0
expr_0:
%t16 = load i32* %v_1
%t18 = load {i32,[ 0 x i32 ]}** %v_0
%t19 = getelementptr {i32,[ 0 x i32 ]}* %t18, i32 0, i32 0
%t17 = load i32* %t19
%t15 = icmp slt i32 %t16 , %t17
br i1 %t15 , label %while_0 , label %endwhile_0
endwhile_0:
%v_2 = alloca i32
store i32 0, i32* %v_2
%v_3 = alloca i32
store i32 0, i32* %v_3
br label %expr_1
while_1:
%t22 = load i32* %v_3
%t23 = load {i32,[ 0 x i32 ]}** %v_0
%t24 = getelementptr {i32,[ 0 x i32 ]}* %t23, i32 0, i32 1, i32 %t22
%t21 = load i32* %t24
store i32 %t21, i32* %v_2
%t26 = load i32* %v_3
%t25 = add i32 1 , %t26
store i32 %t25, i32* %v_3
%t28 = load i32* %v_2
call void @printInt (i32 %t28)
br label %expr_1
expr_1:
%t30 = load i32* %v_3
%t32 = load {i32,[ 0 x i32 ]}** %v_0
%t33 = getelementptr {i32,[ 0 x i32 ]}* %t32, i32 0, i32 0
%t31 = load i32* %t33
%t29 = icmp slt i32 %t30 , %t31
br i1 %t29 , label %while_1 , label %endwhile_1
endwhile_1:
%v_4 = alloca i32
store i32 45, i32* %v_4
%t36 = load i32* %v_4
call void @printInt (i32 %t36)
ret i32 0
}
