declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
@const_2 = internal constant [5 x i8] c"lolo\00"
@const_1 = internal constant [8 x i8] c"sucuni2\00"
@const_0 = internal constant [7 x i8] c"sucuni\00"
@const_4 = internal constant [6 x i8] c"false\00"
@const_3 = internal constant [5 x i8] c"true\00"
define i32 @main() {
entry:
%v_0 = alloca i1
%t1 = icmp slt i32 1 , 3
br label %or_begin_0
or_begin_0:
br i1 %t1 , label %or_end_0 , label %or_second_0
or_second_0:
%t4 = icmp sgt i32 4 , 5
br label %or_third_0
or_third_0:
br label %or_end_0
or_end_0:
%t0 = phi i1 [ 1 , %or_begin_0 ] , [ %t4 , %or_third_0 ]
store i1 %t0, i1* %v_0
%t8 = load i1* %v_0
call void @printBool (i1 %t8)
%t10 = load i1* %v_0
%t9 = add i1 %t10 , 1
br i1 %t9 , label %if_1 , label %else_1
if_1:
%t12 = bitcast [7 x i8]* @const_0 to i8*
call void @printString (i8* %t12)
br label %endif_1
else_1:
br label %endif_1
endif_1:
%v_1 = alloca i1
%t14 = load i1* %v_0
%t13 = add i1 %t14 , 1
store i1 %t13, i1* %v_1
%t16 = load i1* %v_1
%t15 = add i1 %t16 , 1
br i1 %t15 , label %if_2 , label %else_2
if_2:
%t18 = bitcast [8 x i8]* @const_1 to i8*
call void @printString (i8* %t18)
br label %endif_2
else_2:
%t20 = bitcast [5 x i8]* @const_2 to i8*
call void @printString (i8* %t20)
br label %endif_2
endif_2:
ret i32 0
}
define void @printBool(i1 %par_0) {
entry:
%v_0 = alloca i1
store i1 %par_0, i1* %v_0
%t0 = load i1* %v_0
br i1 %t0 , label %if_3 , label %else_3
if_3:
%t2 = bitcast [5 x i8]* @const_3 to i8*
call void @printString (i8* %t2)
br label %endif_3
else_3:
%t4 = bitcast [6 x i8]* @const_4 to i8*
call void @printString (i8* %t4)
br label %endif_3
endif_3:
ret void
}
define i1 @not(i1 %par_0) {
entry:
%v_0 = alloca i1
store i1 %par_0, i1* %v_0
%t0 = load i1* %v_0
br i1 %t0 , label %if_4 , label %else_4
if_4:
ret i1 false
br label %endif_4
else_4:
br label %endif_4
endif_4:
ret i1 true
}
