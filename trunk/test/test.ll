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
br label %and_begin_0
and_begin_0:
%t3 = icmp sgt i32 1 , 0
br i1 %t3 , label %and_second_0 , label %and_end_0
and_second_0:
%t6 = call i1 @fazzo ()
br label %and_end_0
and_end_0:
%t2 = phi i1 [ 0 , %and_begin_0 ] , [ %t6 , %and_second_0 ]
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
br i1 %t0 , label %if_1 , label %else_1
if_1:
%t2 = bitcast [5 x i8]* @const_1 to i8*
call void @printString (i8* %t2)
br label %endif_1
else_1:
%t4 = bitcast [6 x i8]* @const_2 to i8*
call void @printString (i8* %t4)
br label %endif_1
endif_1:
ret void
}
