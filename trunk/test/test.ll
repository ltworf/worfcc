target datalayout = "e-p:32:32:32-i1:8:8-i8:8:8-i16:16:16-i32:32:32-i64:32:64-f32:32:32-f64:32:64-v64:64:64-v128:128:128-a0:0:64-f80:32:32"declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
define i32 @main() {
entry:
br label %expr_0
while_0:
br label %endwhile_0
br label %expr_0
expr_0:
br i1 true , label %while_0 , label %endwhile_0
endwhile_0:
ret i32 0
}
