declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
%list = type {i32,%list}*
define i32 @main() {
entry:
call void @p2 (i32 2,double 2.0)
ret i32 0
}
define void @p2(i32 %par_0,double %par_1) {
entry:
%v_0 = alloca i32
store i32 %par_0, i32* %v_0
%v_1 = alloca double
store double %par_1, double* %v_1
%t1 = load i32* %v_0
call void @printInt (i32 %t1)
%t3 = load double* %v_1
call void @printDouble (double %t3)
ret void
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
