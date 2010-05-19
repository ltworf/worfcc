declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
%list = type {i32,%list}*
define i32 @main() {
entry:
%t2 = call %list @fromTo (i32 1,i32 50)
%t1 = call i32 @length (%list %t2)
call void @printInt (i32 %t1)
%t7 = call %list @fromTo (i32 1,i32 100)
%t6 = call i32 @length2 (%list %t7)
call void @printInt (i32 %t6)
ret i32 0
}
define i32 @head(%list %par_0) {
entry:
%v_0 = alloca %list
store %list %par_0, %list* %v_0
%t2 = load %list* %v_0
%t1 = getelementptr %list %t2, i32 0, i32 0
%t0 = load i32* %t1
ret i32 %t0
}
define %list @cons(i32 %par_0,%list %par_1) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%v_1 = alloca %list
store %list %par_1, %list* %v_1
%v_2 = alloca %list
%t0 = inttoptr i8 0 to %list
store %list %t0, %list* %v_2
%t3 = call noalias i8* @calloc(i32 16,i32 1) nounwind
%t2 = bitcast i8* %t3 to %list
store %list %t2, %list* %v_2
%t5 = load i32* %v_0
%t7 = load %list* %v_2
%t6 = getelementptr %list %t7, i32 0, i32 0
store i32 %t5, i32* %t6
%t9 = load %list* %v_1
%t11 = load %list* %v_2
%t10 = getelementptr %list %t11, i32 0, i32 1
store %list %t9, %list* %t10
%t12 = load %list* %v_2
ret %list %t12
}
define i32 @length(%list %par_0) {
entry:
%v_0 = alloca %list
store %list %par_0, %list* %v_0
%t1 = load %list* %v_0
%t2 = inttoptr i8 0 to %list
%t3 = ptrtoint %list %t1 to i64
%t4 = ptrtoint %list %t2 to i64
%t0 = icmp eq i64 %t3 , %t4
br i1 %t0 , label %if_0 , label %else_0
if_0:
ret i32 0
br label %endif_0
else_0:
%t11 = load %list* %v_0
%t10 = getelementptr %list %t11, i32 0, i32 1
%t9 = load %list* %t10
%t8 = call i32 @length (%list %t9)
%t6 = add i32 1 , %t8
ret i32 %t6
br label %endif_0
endif_0:
unreachable
}
define %list @fromTo(i32 %par_0,i32 %par_1) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%v_1 = alloca i32
store i32 %par_1, i32* %v_1
%t1 = load i32* %v_0
%t2 = load i32* %v_1
%t0 = icmp sgt i32 %t1 , %t2
br i1 %t0 , label %if_1 , label %else_1
if_1:
%t3 = inttoptr i8 0 to %list
ret %list %t3
br label %endif_1
else_1:
%t5 = load i32* %v_0
%t8 = load i32* %v_0
%t7 = add i32 %t8 , 1
%t10 = load i32* %v_1
%t6 = call %list @fromTo (i32 %t7,i32 %t10)
%t4 = call %list @cons (i32 %t5,%list %t6)
ret %list %t4
br label %endif_1
endif_1:
unreachable
}
define i32 @length2(%list %par_0) {
entry:
%v_0 = alloca %list
store %list %par_0, %list* %v_0
%v_1 = alloca i32
store i32 0, i32* %v_1
br label %expr_2
while_2:
%t2 = load i32* %v_1
%t1 = add i32 1 , %t2
store i32 %t1, i32* %v_1
%t6 = load %list* %v_0
%t5 = getelementptr %list %t6, i32 0, i32 1
%t4 = load %list* %t5
store %list %t4, %list* %v_0
br label %expr_2
expr_2:
%t8 = load %list* %v_0
%t9 = inttoptr i8 0 to %list
%t10 = ptrtoint %list %t8 to i64
%t11 = ptrtoint %list %t9 to i64
%t7 = icmp ne i64 %t10 , %t11
br i1 %t7 , label %while_2 , label %endwhile_2
endwhile_2:
%t12 = load i32* %v_1
ret i32 %t12
}
