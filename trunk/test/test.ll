declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
@const_1 = internal constant [6 x i8] c"false\00"
@const_0 = internal constant [5 x i8] c"true\00"
define i32 @main() {
entry:
call void @printBool (i1 true)
ret i32 0
}
define void @printBool(i1 %par_0) {
entry:
%v_0 = alloca i1
store i1 %par_0, i1* %v_0
%t0 = load i1* %v_0
br i1 %t0 , label %if_0 , label %else_0
if_0:
%t2 = bitcast [5 x i8]* @const_0 to i8*
call void @printString (i8* %t2)
br label %endif_0
else_0:
%t4 = bitcast [6 x i8]* @const_1 to i8*
call void @printString (i8* %t4)
br label %endif_0
endif_0:
ret void
}
