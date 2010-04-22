declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
@const_0 = internal constant [6 x i8] c"false\00"
@const_1 = internal constant [14 x i8] c"maggiore di 3\00"
@const_2 = internal constant [12 x i8] c"minore di 3\00"
define i32 @main() {
entry:
%t1 = bitcast [6 x i8]* @const_0 to i8*
call void @printString (i8* %t1)
%t3 = call double @readDouble ()
%t2 = fcmp ogt double %t3 , 3.0
br i1 %t2 , label %if_0 , label %else_0
if_0:
%t6 = bitcast [14 x i8]* @const_1 to i8*
call void @printString (i8* %t6)
br label %endif_0
else_0:
%t8 = bitcast [12 x i8]* @const_2 to i8*
call void @printString (i8* %t8)
br label %endif_0
endif_0:
ret i32 0
}
