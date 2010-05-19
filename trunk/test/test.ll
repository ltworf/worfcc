target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32"declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
%list = type {i32,%list}*
define i32 @main() {
entry:
%t4 = inttoptr i8 0 to %list
%t2 = call %list @cons (i32 7,%list %t4)
%t1 = getelementptr %list %t2, i32 0, i32 0
%t0 = load i32* %t1
ret i32 0
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
