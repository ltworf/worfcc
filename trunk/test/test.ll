define i32 @main() {                                                                                                                               
entry:                                                                                                                                             
%v_0 = alloca i32
store i32 0, i32* %v_0
%v_1 = alloca i32
store i32 0, i32* %v_1
%t2 = add i32 5 , 10
store i32 %t2, i32* %v_1
store i32 %t2, i32* %v_0
%t6 = load i32* %v_1
%t7 = load i32* %v_0
%t5 = add i32 %t6 , %t7
ret i32 %t5
}

