define i32 @main() {
entry:
%v_0 = alloca i32
%t0 = add i32 5 , 10
store i32 %t0, i32* %v_0
%t4 = load i32* %v_0
%t3 = sub i32 %t4 , 9
ret i32 %t3
}

