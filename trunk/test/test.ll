declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
@const_0 = internal constant [5 x i8] c"lala\00"
@const_2 = internal constant [6 x i8] c"false\00"
@const_1 = internal constant [5 x i8] c"true\00"
define i32 @main() {
entry:
%v_0 = alloca i32
store i32 5, i32* %v_0
%v_1 = alloca double
store double 9.1, double* %v_1
%v_2 = alloca i32
store i32 0, i32* %v_2
%v_3 = alloca double
store double 0.0, double* %v_3
%t4 = load i32* %v_0
%t3 = mul i32 %t4 , -1
call void @printInt (i32 %t3)
%t7 = load double* %v_1
%t6 = fmul double %t7 , -1.0
call void @printDouble (double %t6)
%t10 = load i32* %v_2
%t9 = mul i32 %t10 , -1
call void @printInt (i32 %t9)
%t13 = load double* %v_3
%t12 = fmul double %t13 , -1.0
call void @printDouble (double %t12)
ret i32 0
}
define i1 @fazzo() {
entry:
%t1 = bitcast [5 x i8]* @const_0 to i8*
call void @printString (i8* %t1)
ret i1 false
}
define void @printBool(i1 %par_0) {
entry:
%v_0 = alloca i1
store i1 %par_0, i1* %v_0
%t0 = load i1* %v_0
br i1 %t0 , label %if_0 , label %else_0
if_0:
%t2 = bitcast [5 x i8]* @const_1 to i8*
call void @printString (i8* %t2)
br label %endif_0
else_0:
%t4 = bitcast [6 x i8]* @const_2 to i8*
call void @printString (i8* %t4)
br label %endif_0
endif_0:
ret void
}
