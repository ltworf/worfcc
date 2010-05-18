declare void @printInt(i32 %x)
declare void @printDouble(double %x)
declare void @printString(i8* %s)
declare i32 @readInt()
declare double @readDouble()
declare noalias i8* @calloc(i32,i32) nounwind
@const_0 = internal constant [3 x i8] c"==\00"
define i32 @main() {
entry:
%v_0 = alloca {i32,[ 0 x double ]}*
%t2 = mul i32 4, 8	;Calculate the size of the memory for the array
%t3 = add i32 8,%t2	;Plus 8 bytes for the length
%t5 = call noalias i8* @calloc(i32 %t3,i32 1) nounwind
%t4 = bitcast i8* %t5 to {i32,[ 0 x double ]}*
%t6 = getelementptr {i32,[ 0 x double ]}* %t4, i32 0, i32 0
store i32 4, i32* %t6	;stores the size of the array
store {i32,[ 0 x double ]}* %t4, {i32,[ 0 x double ]}** %v_0
%v_1 = alloca {i32,[ 0 x {i32,[ 0 x double ]}* ]}*
%t9 = mul i32 3, 8	;Calculate the size of the memory for the array
%t10 = add i32 8,%t9	;Plus 8 bytes for the length
%t12 = call noalias i8* @calloc(i32 %t10,i32 1) nounwind
%t11 = bitcast i8* %t12 to {i32,[ 0 x {i32,[ 0 x double ]}* ]}*
%t13 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t11, i32 0, i32 0
store i32 3, i32* %t13	;stores the size of the array
%v_2 = alloca i32
store i32 0, i32* %v_2
%t20 = mul i32 4, 8	;Calculate the size of the memory for the array
%t21 = add i32 8,%t20	;Plus 8 bytes for the length
br label %ar_loop_expr_1
ar_loop_body_0:
%t14 = load i32* %v_2
%t23 = call noalias i8* @calloc(i32 %t21,i32 1) nounwind
%t22 = bitcast i8* %t23 to {i32,[ 0 x double ]}*
%t24 = getelementptr {i32,[ 0 x double ]}* %t22, i32 0, i32 0
store i32 4, i32* %t24	;stores the size of the array
%t18 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t11, i32 0, i32 1, i32 %t14
store {i32,[ 0 x double ]}* %t22, {i32,[ 0 x double ]}** %t18
%t15 = add i32 1 , %t14
store i32 %t15, i32* %v_2
br label %ar_loop_expr_1
ar_loop_expr_1:
%t16 = load i32* %v_2
%t17 = icmp slt i32 %t16 , 3
br i1 %t17 , label %ar_loop_body_0 , label %ar_loop_exit_2
ar_loop_exit_2:
store {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t11, {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_1
%v_3 = alloca i32
store i32 0, i32* %v_3
br label %expr_3
while_3:
%v_4 = alloca i32
store i32 0, i32* %v_4
br label %expr_4
while_4:
%t29 = load i32* %v_3
%t30 = load {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_1
%t31 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t30, i32 0, i32 1, i32 %t29
%t32 = load i32* %v_4
%t33 = load {i32,[ 0 x double ]}** %t31
%t34 = getelementptr {i32,[ 0 x double ]}* %t33, i32 0, i32 1, i32 %t32
store double 5.0, double* %t34
%t36 = load i32* %v_4
%t35 = add i32 1 , %t36
store i32 %t35, i32* %v_4
br label %expr_4
expr_4:
%t38 = load i32* %v_4
%t42 = load {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_1
%t43 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t42, i32 0, i32 1, i32 0
%t40 = load {i32,[ 0 x double ]}** %t43
%t44 = getelementptr {i32,[ 0 x double ]}* %t40, i32 0, i32 0
%t39 = load i32* %t44
%t37 = icmp slt i32 %t38 , %t39
br i1 %t37 , label %while_4 , label %endwhile_4
endwhile_4:
%t46 = load i32* %v_3
%t45 = add i32 1 , %t46
store i32 %t45, i32* %v_3
br label %expr_3
expr_3:
%t48 = load i32* %v_3
%t50 = load {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_1
%t51 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t50, i32 0, i32 0
%t49 = load i32* %t51
%t47 = icmp slt i32 %t48 , %t49
br i1 %t47 , label %while_3 , label %endwhile_3
endwhile_3:
store i32 0, i32* %v_3
br label %expr_5
while_5:
%t56 = load i32* %v_3
%t57 = load {i32,[ 0 x double ]}** %v_0
%t58 = getelementptr {i32,[ 0 x double ]}* %t57, i32 0, i32 1, i32 %t56
store double 3.0, double* %t58
%t60 = load i32* %v_3
%t59 = add i32 1 , %t60
store i32 %t59, i32* %v_3
br label %expr_5
expr_5:
%t62 = load i32* %v_3
%t65 = load {i32,[ 0 x double ]}** %v_0
%t66 = getelementptr {i32,[ 0 x double ]}* %t65, i32 0, i32 0
%t64 = load i32* %t66
%t63 = sub i32 %t64 , 1
%t61 = icmp slt i32 %t62 , %t63
br i1 %t61 , label %while_5 , label %endwhile_5
endwhile_5:
%t69 = load {i32,[ 0 x double ]}** %v_0
%t71 = load {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_1
%t72 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t71, i32 0, i32 1, i32 0
store {i32,[ 0 x double ]}* %t69, {i32,[ 0 x double ]}** %t72
%v_5 = alloca i32
store i32 0, i32* %v_5
br label %expr_6
while_6:
%t77 = load i32* %v_5
%t78 = load {i32,[ 0 x double ]}** %v_0
%t79 = getelementptr {i32,[ 0 x double ]}* %t78, i32 0, i32 1, i32 %t77
%t76 = load double* %t79
%t75 = fadd double %t76 , 1.0
%t82 = load {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_1
%t83 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t82, i32 0, i32 1, i32 1
%t84 = load i32* %v_5
%t85 = load {i32,[ 0 x double ]}** %t83
%t86 = getelementptr {i32,[ 0 x double ]}* %t85, i32 0, i32 1, i32 %t84
store double %t75, double* %t86
%t88 = load i32* %v_5
%t87 = add i32 1 , %t88
store i32 %t87, i32* %v_5
br label %expr_6
expr_6:
%t90 = load i32* %v_5
%t92 = load {i32,[ 0 x double ]}** %v_0
%t93 = getelementptr {i32,[ 0 x double ]}* %t92, i32 0, i32 0
%t91 = load i32* %t93
%t89 = icmp slt i32 %t90 , %t91
br i1 %t89 , label %while_6 , label %endwhile_6
endwhile_6:
%v_6 = alloca {i32,[ 0 x double ]}*
%v_7 = alloca i32
store i32 0, i32* %v_7
br label %expr_7
while_7:
%t96 = load i32* %v_7
%t97 = load {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_1
%t98 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t97, i32 0, i32 1, i32 %t96
%t95 = load {i32,[ 0 x double ]}** %t98
store {i32,[ 0 x double ]}* %t95, {i32,[ 0 x double ]}** %v_6
%t100 = load i32* %v_7
%t99 = add i32 1 , %t100
store i32 %t99, i32* %v_7
%t102 = bitcast [3 x i8]* @const_0 to i8*
call void @printString (i8* %t102)
%v_8 = alloca double
store double 0.0, double* %v_8
%v_9 = alloca i32
store i32 0, i32* %v_9
br label %expr_8
while_8:
%t105 = load i32* %v_9
%t106 = load {i32,[ 0 x double ]}** %v_6
%t107 = getelementptr {i32,[ 0 x double ]}* %t106, i32 0, i32 1, i32 %t105
%t104 = load double* %t107
store double %t104, double* %v_8
%t109 = load i32* %v_9
%t108 = add i32 1 , %t109
store i32 %t108, i32* %v_9
%t111 = load double* %v_8
call void @printDouble (double %t111)
br label %expr_8
expr_8:
%t113 = load i32* %v_9
%t115 = load {i32,[ 0 x double ]}** %v_6
%t116 = getelementptr {i32,[ 0 x double ]}* %t115, i32 0, i32 0
%t114 = load i32* %t116
%t112 = icmp slt i32 %t113 , %t114
br i1 %t112 , label %while_8 , label %endwhile_8
endwhile_8:
br label %expr_7
expr_7:
%t118 = load i32* %v_7
%t120 = load {i32,[ 0 x {i32,[ 0 x double ]}* ]}** %v_1
%t121 = getelementptr {i32,[ 0 x {i32,[ 0 x double ]}* ]}* %t120, i32 0, i32 0
%t119 = load i32* %t121
%t117 = icmp slt i32 %t118 , %t119
br i1 %t117 , label %while_7 , label %endwhile_7
endwhile_7:
ret i32 0
}
