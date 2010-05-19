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
%t0 = inttoptr i8 0 to %list
store %list %t0, %list* %v_0
ret i32 0
}
