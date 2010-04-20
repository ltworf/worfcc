define i32 @main() {
entry:
%v_0 = alloca i32
store i32 10, i32* %v_0
%v_1 = alloca i32
store i32 0, i32* %v_1
%t4 = load i32* %v_0
%t3 = add i32 1 , %t4
store i32 %t3, i32* %v_0
%t2 = mul i32 %t3 , 3
store i32 %t2, i32* %v_1
%t6 = load i32* %v_1
ret i32 %t6
}
