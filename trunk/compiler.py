#!/usr/bin/env jython
# -*- coding: utf-8 -*-

# Copyright (C) 2010  Salvo "LtWorf" Tomaselli
# 
# worfcc
# worfcc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

import typechecker
import sys
import cpp
import context
import inferred


class labeler:
    '''This class provides a simple global counter used tor labels'''
    def __init__(self):
        self.label=0
    def getlbl(self):
        self.label+=1
        return self.label

variables=context.var_env()
lbl=labeler()

def ijvm_compile(filename):
    '''Compiles the program into JVM assembly'''
    prog,contx,inf=typechecker.checkfile(filename)
    print inf
    compile_block(prog.listdeclaration_[0].liststatement_)

def compile_block(statements):
    for i in statements:
        if isinstance(i,cpp.Absyn.Expression):    #Expression
            compile_expr(i.expr_)
            print "pop"     #An expression returns a value, so we pop it now to free the stack
        elif isinstance(i,cpp.Absyn.LocalVars):   #Var declaration (multiple vars)
            for j in i.listcident_:
                variables.put(j)
                '''elif isinstance(i,cpp.Absyn.LocalVarInit):   #Var declaration and initialization
                variables.put(i.cident_)    #Putting the var
                compile_expr(i.expr_)       #Resolving the assignment
                print "istore %d" % variables.get(i.cident_) '''
        elif isinstance(i,cpp.Absyn.Block): #New context
            variables.push()
            compile_block(i.liststatement_)
            variables.pop()
        elif isinstance(i,cpp.Absyn.IfElse):
            compile_expr(i.expr_) #Pushing the result of the condition
            
            lab1=lbl.getlbl()
            
            print "ifeq else%d" % lab1    #If expr is false
            compile_block((i.statement_1,))  #True branch
            print "goto endif%d" %lab1
            print "else%d:" % lab1
            compile_block((i.statement_2,))  #False branch
            print "endif%d:" %lab1
        elif isinstance(i,cpp.Absyn.While):
            lab1=lbl.getlbl()
            
            print "while%d:" % lab1
            compile_expr(i.expr_)
            print "ifeq endwhile%d" % lab1  #If condition is false, exits
            compile_block((i.statement_,))  #While body
            print "goto while%d" % lab1
            print "endwhile%d:" % lab1

def emit(instr,s):
    print instr

def compile_expr(e):
    '''
Edbl.       Expr16          ::= Double;
Ebool.      Expr16          ::= Bool;
Estrng.     Expr16          ::= String;
Eitm.       Expr16          ::= CIdent; 
Efun.       Expr15          ::= CIdent "(" [Expr] ")";
Eainc.      Expr14          ::= Expr15 "++";
Eadec.      Expr14          ::= Expr15 "--";
Epinc.      Expr13          ::= "++" Expr14;
Epdec.      Expr13          ::= "--" Expr14;

ENeg.       Expr12 ::= "-" Expr13 ;
ENot.       Expr12 ::= "!" Expr13 ;


Emod.       Expr11          ::= Expr11 "%" Expr12;  --TODO

Eand.       Expr4           ::= Expr4 "&&" Expr5;
Eor.        Expr3           ::= Expr3 "||" Expr4;
Eass.       Expr2           ::= Expr3 "=" Expr2;        --I think this was wrong in lab1

Edbl.       Expr16          ::= Double;
Estrng.     Expr16          ::= String;
Eitm.       Expr16          ::= CIdent; 
Efun.       Expr15          ::= CIdent "(" [Expr] ")";
Eainc.      Expr14          ::= Expr15 "++";
Eadec.      Expr14          ::= Expr15 "--";
Epinc.      Expr13          ::= "++" Expr14;
Epdec.      Expr13          ::= "--" Expr14;

ENeg.       Expr12 ::= "-" Expr13 ;
ENot.       Expr12 ::= "!" Expr13 ;


Emul.       Expr11          ::= Expr11 "*" Expr12;
Ediv.       Expr11          ::= Expr11 "/" Expr12;
Emod.       Expr11          ::= Expr11 "%" Expr12;  --TODO
Eadd.       Expr10          ::= Expr10 "+" Expr11;
Esub.       Expr10          ::= Expr10 "-" Expr11;

Elt.        Expr9           ::= Expr9 "<" Expr10;
Egt.        Expr9           ::= Expr9 ">" Expr10;
Eelt.       Expr9           ::= Expr9 "<=" Expr10;
Eegt.       Expr9           ::= Expr9 ">=" Expr10;
Eeql.       Expr8           ::= Expr8 "==" Expr9;
Edif.       Expr8           ::= Expr8 "!=" Expr9;


Eand.       Expr4           ::= Expr4 "&&" Expr5;
Eor.        Expr3           ::= Expr3 "||" Expr4;
Eass.       Expr2           ::= Expr3 "=" Expr2;        --I think this was wrong in lab1

    '''
    
    dic= {
    cpp.Absyn.Eadd: "iadd",
    cpp.Absyn.Emul: "imul",
    cpp.Absyn.Esub: "isub",
    cpp.Absyn.Ediv: "idiv"
    }
    
    comp_dic= {
        cpp.Absyn.Egt: "if_icmpgt",
        cpp.Absyn.Elt: "if_icmplt",
        cpp.Absyn.Eelt: "if_icmple",
        cpp.Absyn.Eegt: "if_icmpge",
        cpp.Absyn.Eeql: "if_icmpeq",
        cpp.Absyn.Edif: "if_icmpne"
    }
    
    if isinstance(e,cpp.Absyn.Eint): #Integer value
        if e.integer_ == -1:    #Constants
            emit("iconst_m1",1)
        elif e.integer_ in range(-1,6):
            emit("iconst_%d" % e.integer_,1)
        elif e.integer_ in range(-129,128):   #Push byte
            emit ("bipush %d"%e.integer_,1)
        elif e.integer_ in range(-32769,32768): #Push short
            emit("sipush %d" % e.integer_ ,1)
        else:                                   #Push integer
            emit("ldc %d" % e.integer_,1)
    elif isinstance(e,cpp.Absyn.Ebool): #Boolean value
        if isinstance(e.bool_,cpp.Absyn.TrueLit):
            emit("iconst_1",1)
        else:
            emit("iconst_0",1)
            
            
            
            
    elif isinstance(e,cpp.Absyn.Eitm): #Variable
        print "iload %d" % variables.get(e.cident_)
    elif isinstance(e,cpp.Absyn.Eass): #Assignment
        compile_expr(e.expr_2)
        print "dup" #Needed becaus assignment returns a value as well
        print "istore %d" % variables.get(e.expr_1.cident_)
    elif isinstance(e,cpp.Absyn.Eainc): #var++
        print "iload %d" % variables.get(e.expr_.cident_) #Load var on stack
        print "iinc %d 1" % variables.get(e.expr_.cident_) #increment variable
    elif isinstance(e,cpp.Absyn.Epinc): #++var
        print "iinc %d 1" % variables.get(e.expr_.cident_) #increment variable
        print "iload %d" % variables.get(e.expr_.cident_) #Load var on stack
    elif isinstance(e,cpp.Absyn.Efun): #Function call (print)
        compile_expr(e.listexpr_[0])    #Only has one param
        print "invokestatic runtime/iprint(I)V"
        print "bipush 1"    #Return value of iprint
    elif isinstance(e,cpp.Absyn.Eand):  #Short-circuit and operator
        lab1=lbl.getlbl()
        compile_expr(e.expr_1)  #Evaluating 1st operand
        print "ifeq andfalse%d" % lab1  #If 1st operand is false
        compile_expr(e.expr_2)  #Evaluating 2nd operand, that will give the value to the expression
        print "goto endand%d" % lab1
        print "andfalse%d:" % lab1
        print "bipush 0"    #push false
        print "endand%d:" % lab1
    elif isinstance(e,cpp.Absyn.Eor):  #Short-circuit or operator
        lab1=lbl.getlbl()
        compile_expr(e.expr_1)  #Evaluating 1st operand
        print "ifne  ortrue%d" % lab1  #expr1 true,
        compile_expr(e.expr_2)  #2nd operand
        print "goto endor%d" % lab1
        print "ortrue%d:" % lab1
        print "bipush 1" #pushing the true value
        print "endor%d:" %lab1
    elif e.__class__ in comp_dic:   #Comparison
        compile_expr(e.expr_1) #Pushing operands
        compile_expr(e.expr_2)
        
        lab1=lbl.getlbl()   #Getting label
        
        print "%s trueexpr%d" % (comp_dic[e.__class__],lab1)
        print "bipush 0"    #False
        print "goto endexpr%d" % lab1
        print "trueexpr%d:" % lab1
        print "bipush 1"    #True
        print "endexpr%d:" %lab1
    elif e.__class__ in dic: #Aritmetic operations
        compile_expr(e.expr_1)
        compile_expr(e.expr_2)
        print dic[e.__class__]

if __name__=="__main__":
    for f in range(1,len(sys.argv)):
        ijvm_compile(sys.argv[f])