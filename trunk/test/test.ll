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
%v_0 = alloca i1
store i1 false, i1* %v_0
%t4 = call i1 @fazzo ()
br label %and_begin_1
and_begin_1:
br i1 %t4 , label %and_second_1 , label %and_end_1
and_second_1:
%t6 = call i1 @fazzo ()
br label %or_begin_2
or_begin_2:
br i1 %t6 , label %or_end_2 , label %or_second_2
or_second_2:
br label %or_end_2
or_end_2:
%t5 = phi i1 [ 0 , %or_begin_2 ] , [ 1 , %or_second_2 ]
br label %and_third_1
and_third_1:
br label %and_end_1
and_end_1:
%t3 = phi i1 [ 0 , %and_begin_1 ] , [ %t5 , %and_third_1 ]
br label %or_begin_0
or_begin_0:
br i1 %t3 , label %or_end_0 , label %or_second_0
or_second_0:
%t8 = call i1 @fazzo ()
br label %or_begin_3
or_begin_3:
br i1 %t8 , label %or_end_3 , label %or_second_3
or_second_3:
br label %or_end_3
or_end_3:
%t7 = phi i1 [ 0 , %or_begin_3 ] , [ 1 , %or_second_3 ]
br label %or_third_0
or_third_0:
br label %or_end_0
or_end_0:
%t2 = phi i1 [ 1 , %or_begin_0 ] , [ %t7 , %or_third_0 ]
call void @printBool (i1 %t2)
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
br i1 %t0 , label %if_4 , label %else_4
if_4:
%t2 = bitcast [5 x i8]* @const_1 to i8*
call void @printString (i8* %t2)
br label %endif_4
else_4:
%t4 = bitcast [6 x i8]* @const_2 to i8*
call void @printString (i8* %t4)
br label %endif_4
endif_4:
ret void
}
