declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
define {i32,[ 0 x i32 ]}* @doubleArray({i32,[ 0 x i32 ]}* %par_0) {
entry:
%v_0 = alloca {i32,[ 0 x i32 ]}*
store {i32,[ 0 x i32 ]}* %par_0, {i32,[ 0 x i32 ]}** %v_0
%v_1 = alloca {i32,[ 0 x i32 ]}*
%t2 = load {i32,[ 0 x i32 ]}** %v_0
%t3 = getelementptr {i32,[ 0 x i32 ]}* %t2, i32 0, i32 0
%t1 = load i32* %t3
%t4 = mul i32 %t1, 4	;Calculate the size of the memory for the array
%t5 = add i32 4,%t4	;Plus 4 bytes for the length
%t7 = call noalias i8* @calloc(i32 %t5,i32 1) nounwind
%t6 = bitcast i8* %t7 to {i32,[ 0 x i32 ]}*
%t8 = getelementptr {i32,[ 0 x i32 ]}* %t6, i32 0, i32 0
store i32 %t1, i32* %t8	;stores the size of the array
store {i32,[ 0 x i32 ]}* %t6, {i32,[ 0 x i32 ]}** %v_1
%v_2 = alloca i32
store i32 0, i32* %v_2
%t10 = load {i32,[ 0 x i32 ]}** %v_1
ret {i32,[ 0 x i32 ]}* %t10
}
define void @shiftLeft({i32,[ 0 x i32 ]}* %par_0) {
entry:
%v_0 = alloca {i32,[ 0 x i32 ]}*
store {i32,[ 0 x i32 ]}* %par_0, {i32,[ 0 x i32 ]}** %v_0
%v_1 = alloca i32
%t2 = load {i32,[ 0 x i32 ]}** %v_0
%t3 = getelementptr {i32,[ 0 x i32 ]}* %t2, i32 0, i32 1, i32 0
%t0 = load i32* %t3
store i32 %t0, i32* %v_1
%v_2 = alloca i32
store i32 0, i32* %v_2
br label %expr_0
while_0:
%t8 = load i32* %v_2
%t7 = add i32 %t8 , 1
%t10 = load {i32,[ 0 x i32 ]}** %v_0
%t11 = getelementptr {i32,[ 0 x i32 ]}* %t10, i32 0, i32 1, i32 %t7
%t6 = load i32* %t11
%t12 = load i32* %v_2
%t13 = load {i32,[ 0 x i32 ]}** %v_0
%t14 = getelementptr {i32,[ 0 x i32 ]}* %t13, i32 0, i32 1, i32 %t12
store i32 %t6, i32* %t14
%t16 = load i32* %v_2
%t15 = add i32 1 , %t16
store i32 %t15, i32* %v_2
br label %expr_0
expr_0:
%t18 = load i32* %v_2
%t21 = load {i32,[ 0 x i32 ]}** %v_0
%t22 = getelementptr {i32,[ 0 x i32 ]}* %t21, i32 0, i32 0
%t20 = load i32* %t22
%t19 = sub i32 %t20 , 1
%t17 = icmp slt i32 %t18 , %t19
br i1 %t17 , label %while_0 , label %endwhile_0
endwhile_0:
%t25 = load i32* %v_1
%t28 = load {i32,[ 0 x i32 ]}** %v_0
%t29 = getelementptr {i32,[ 0 x i32 ]}* %t28, i32 0, i32 0
%t27 = load i32* %t29
%t26 = sub i32 %t27 , 1
%t31 = load {i32,[ 0 x i32 ]}** %v_0
%t32 = getelementptr {i32,[ 0 x i32 ]}* %t31, i32 0, i32 1, i32 %t26
store i32 %t25, i32* %t32
ret void
ret void
}
define i32 @scalProd({i32,[ 0 x i32 ]}* %par_1,{i32,[ 0 x i32 ]}* %par_0) {
entry:
%v_0 = alloca {i32,[ 0 x i32 ]}*
store {i32,[ 0 x i32 ]}* %par_0, {i32,[ 0 x i32 ]}** %v_0
%v_1 = alloca {i32,[ 0 x i32 ]}*
store {i32,[ 0 x i32 ]}* %par_1, {i32,[ 0 x i32 ]}** %v_1
%v_2 = alloca i32
store i32 0, i32* %v_2
%v_3 = alloca i32
store i32 0, i32* %v_3
br label %expr_1
while_1:
%t4 = load i32* %v_2
%t7 = load i32* %v_3
%t8 = load {i32,[ 0 x i32 ]}** %v_0
%t9 = getelementptr {i32,[ 0 x i32 ]}* %t8, i32 0, i32 1, i32 %t7
%t6 = load i32* %t9
%t11 = load i32* %v_3
%t12 = load {i32,[ 0 x i32 ]}** %v_1
%t13 = getelementptr {i32,[ 0 x i32 ]}* %t12, i32 0, i32 1, i32 %t11
%t10 = load i32* %t13
%t5 = mul i32 %t6 , %t10
%t3 = add i32 %t4 , %t5
store i32 %t3, i32* %v_2
%t15 = load i32* %v_3
%t14 = add i32 1 , %t15
store i32 %t14, i32* %v_3
br label %expr_1
expr_1:
%t17 = load i32* %v_3
%t19 = load {i32,[ 0 x i32 ]}** %v_0
%t20 = getelementptr {i32,[ 0 x i32 ]}* %t19, i32 0, i32 0
%t18 = load i32* %t20
%t16 = icmp slt i32 %t17 , %t18
br i1 %t16 , label %while_1 , label %endwhile_1
endwhile_1:
%t21 = load i32* %v_2
ret i32 %t21
}
define i32 @main() {
entry:
%v_0 = alloca {i32,[ 0 x i32 ]}*
%t2 = mul i32 5, 4	;Calculate the size of the memory for the array
%t3 = add i32 4,%t2	;Plus 4 bytes for the length
%t5 = call noalias i8* @calloc(i32 %t3,i32 1) nounwind
%t4 = bitcast i8* %t5 to {i32,[ 0 x i32 ]}*
%t6 = getelementptr {i32,[ 0 x i32 ]}* %t4, i32 0, i32 0
store i32 5, i32* %t6	;stores the size of the array
store {i32,[ 0 x i32 ]}* %t4, {i32,[ 0 x i32 ]}** %v_0
%v_1 = alloca i32
store i32 0, i32* %v_1
br label %expr_2
while_2:
%t9 = load i32* %v_1
%t10 = load i32* %v_1
%t11 = load {i32,[ 0 x i32 ]}** %v_0
%t12 = getelementptr {i32,[ 0 x i32 ]}* %t11, i32 0, i32 1, i32 %t10
store i32 %t9, i32* %t12
%t14 = load i32* %v_1
%t13 = add i32 1 , %t14
store i32 %t13, i32* %v_1
br label %expr_2
expr_2:
%t16 = load i32* %v_1
%t18 = load {i32,[ 0 x i32 ]}** %v_0
%t19 = getelementptr {i32,[ 0 x i32 ]}* %t18, i32 0, i32 0
%t17 = load i32* %t19
%t15 = icmp slt i32 %t16 , %t17
br i1 %t15 , label %while_2 , label %endwhile_2
endwhile_2:
%t21 = load {i32,[ 0 x i32 ]}** %v_0
call void @shiftLeft ({i32,[ 0 x i32 ]}* %t21)
%v_2 = alloca {i32,[ 0 x i32 ]}*
%t23 = load {i32,[ 0 x i32 ]}** %v_0
%t22 = call {i32,[ 0 x i32 ]}* @doubleArray ({i32,[ 0 x i32 ]}* %t23)
store {i32,[ 0 x i32 ]}* %t22, {i32,[ 0 x i32 ]}** %v_2
%t26 = load {i32,[ 0 x i32 ]}** %v_0
%t27 = load {i32,[ 0 x i32 ]}** %v_2
%t25 = call i32 @scalProd ({i32,[ 0 x i32 ]}* %t27,{i32,[ 0 x i32 ]}* %t26)
call void @printInt (i32 %t25)
ret i32 0
}
