declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
@const_0 = internal constant [9 x i8] c"hello */\00"
@const_1 = internal constant [9 x i8] c"/* world\00"
define i32 @main() {
entry:
%t1 = call i32 @fac (i32 10)
call void @printInt (i32 %t1)
%t4 = call i32 @rfac (i32 10)
call void @printInt (i32 %t4)
%t7 = call i32 @mfac (i32 10)
call void @printInt (i32 %t7)
%t10 = call i32 @ifac (i32 10)
call void @printInt (i32 %t10)
%v_0 = alloca double
store double 0.0, double* %v_0
%v_1 = alloca i32
store i32 10, i32* %v_1
%v_2 = alloca i32
store i32 1, i32* %v_2
br label %expr_0
while_0:
%t16 = load i32* %v_2
%t17 = load i32* %v_1
%t15 = mul i32 %t16 , %t17
store i32 %t15, i32* %v_2
%t19 = load i32* %v_1
%t18 = sub i32 %t19 , 1
store i32 %t18, i32* %v_1
br label %expr_0
expr_0:
%t21 = load i32* %v_1
%t20 = icmp sgt i32 %t21 , 0
br i1 %t20 , label %while_0 , label %endwhile_0
endwhile_0:
%t24 = load i32* %v_2
call void @printInt (i32 %t24)
%t26 = call double @dfac (double 10.0)
call void @printDouble (double %t26)
%t29 = bitcast [9 x i8]* @const_0 to i8*
call void @printString (i8* %t29)
%t31 = bitcast [9 x i8]* @const_1 to i8*
call void @printString (i8* %t31)
ret i32 0
}
define i32 @fac(i32 %par_0) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%v_1 = alloca i32
store i32 0, i32* %v_1
%v_2 = alloca i32
store i32 0, i32* %v_2
store i32 1, i32* %v_1
%t3 = load i32* %v_0
store i32 %t3, i32* %v_2
br label %expr_1
while_1:
%t6 = load i32* %v_1
%t7 = load i32* %v_2
%t5 = mul i32 %t6 , %t7
store i32 %t5, i32* %v_1
%t10 = load i32* %v_2
%t9 = sub i32 %t10 , 1
store i32 %t9, i32* %v_2
br label %expr_1
expr_1:
%t13 = load i32* %v_2
%t12 = icmp sgt i32 %t13 , 0
br i1 %t12 , label %while_1 , label %endwhile_1
endwhile_1:
%t15 = load i32* %v_1
ret i32 %t15
}
define i32 @rfac(i32 %par_0) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%t1 = load i32* %v_0
%t0 = icmp eq i32 %t1 , 0
br i1 %t0 , label %if_2 , label %else_2
if_2:
ret i32 1
br label %endif_2
else_2:
%t5 = load i32* %v_0
%t8 = load i32* %v_0
%t7 = sub i32 %t8 , 1
%t6 = call i32 @rfac (i32 %t7)
%t4 = mul i32 %t5 , %t6
ret i32 %t4
br label %endif_2
endif_2:
unreachable
}
define i32 @mfac(i32 %par_0) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%t1 = load i32* %v_0
%t0 = icmp eq i32 %t1 , 0
br i1 %t0 , label %if_3 , label %else_3
if_3:
ret i32 1
br label %endif_3
else_3:
%t5 = load i32* %v_0
%t8 = load i32* %v_0
%t7 = sub i32 %t8 , 1
%t6 = call i32 @nfac (i32 %t7)
%t4 = mul i32 %t5 , %t6
ret i32 %t4
br label %endif_3
endif_3:
unreachable
}
define i32 @nfac(i32 %par_0) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%t1 = load i32* %v_0
%t0 = icmp ne i32 %t1 , 0
br i1 %t0 , label %if_4 , label %else_4
if_4:
%t6 = load i32* %v_0
%t5 = sub i32 %t6 , 1
%t4 = call i32 @mfac (i32 %t5)
%t8 = load i32* %v_0
%t3 = mul i32 %t4 , %t8
ret i32 %t3
br label %endif_4
else_4:
ret i32 1
br label %endif_4
endif_4:
unreachable
}
define double @dfac(double %par_0) {
entry:
%v_0 = alloca double
store double %par_0, double* %v_0
%t1 = load double* %v_0
%t0 = fcmp oeq double %t1 , 0.0
br i1 %t0 , label %if_5 , label %else_5
if_5:
ret double 1.0
br label %endif_5
else_5:
%t5 = load double* %v_0
%t8 = load double* %v_0
%t7 = fsub double %t8 , 1.0
%t6 = call double @dfac (double %t7)
%t4 = fmul double %t5 , %t6
ret double %t4
br label %endif_5
endif_5:
unreachable
}
define i32 @ifac(i32 %par_0) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%t2 = load i32* %v_0
%t0 = call i32 @ifac2f (i32 %t2,i32 1)
ret i32 %t0
}
define i32 @ifac2f(i32 %par_1,i32 %par_0) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%v_1 = alloca i32
store i32 %par_1, i32* %v_1
%t1 = load i32* %v_0
%t2 = load i32* %v_1
%t0 = icmp eq i32 %t1 , %t2
br i1 %t0 , label %if_6 , label %else_6
if_6:
%t3 = load i32* %v_0
ret i32 %t3
br label %endif_6
else_6:
br label %endif_6
endif_6:
%t5 = load i32* %v_0
%t6 = load i32* %v_1
%t4 = icmp sgt i32 %t5 , %t6
br i1 %t4 , label %if_7 , label %else_7
if_7:
ret i32 1
br label %endif_7
else_7:
br label %endif_7
endif_7:
%v_2 = alloca i32
store i32 0, i32* %v_2
%t11 = load i32* %v_0
%t12 = load i32* %v_1
%t10 = add i32 %t11 , %t12
%t9 = sdiv i32 %t10 , 2
store i32 %t9, i32* %v_2
%t16 = load i32* %v_0
%t17 = load i32* %v_2
%t15 = call i32 @ifac2f (i32 %t17,i32 %t16)
%t20 = load i32* %v_2
%t19 = add i32 %t20 , 1
%t22 = load i32* %v_1
%t18 = call i32 @ifac2f (i32 %t22,i32 %t19)
%t14 = mul i32 %t15 , %t18
ret i32 %t14
}
