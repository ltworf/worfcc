declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
%list = type {i32,%list}*
define i32 @main() {
entry:
%v_0 = alloca %list
%t1 = call noalias i8* @calloc(i32 16,i32 1) nounwind
%t0 = bitcast i8* %t1 to %list
store %list %t0, %list* %v_0
ret i32 0
}
define i32 @head(%list %par_0) {
entry:
%v_0 = alloca %list
store %list %par_0, %list* %v_0
ret i32 %t0
}
