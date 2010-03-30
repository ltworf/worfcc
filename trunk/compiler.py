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
import improve
import os.path


prefix= {
        cpp.Absyn.Typeint:("i",1),
        cpp.Absyn.Typebool:("i",1),
        cpp.Absyn.Typedouble:("d",2),
        cpp.Absyn.Typevoid:("v",0),
        cpp.Absyn.Typestrng:("Ljava/lang/String;",2)
        }

class labeler:
    '''This class provides a simple global counter used tor labels'''
    def __init__(self):
        self.label=0
    def getlbl(self):
        self.label+=1
        return self.label

def ijvm_compile(filename):
    '''Compiles the program into JVM assembly'''
    prog,contx,inf=typechecker.checkfile(filename)
    
    #Gets the name of the class
    cname='.'.join(os.path.basename(filename).split('.')[:-1])
    
    dname='%s/%s.j' % (os.path.dirname(filename),cname)
    
    f=file(dname,"w")
    
    f.write( class_header(cname))
    for i in prog.listdeclaration_:
        c=cfunction(i,inf,contx,cname)
        f.write(c.fcompile())
    f.close()
    return dname

def class_header(classname):
    '''Prints the header of the jasmin file'''
    r=''
    r+=".class public %s\n" % classname
    r+=".super java/lang/Object\n"
    r+="\n"
    r+=".method public <init>()V\n"
    r+="\taload_0\n"
    r+="\tinvokespecial java/lang/Object/<init>()V\n"
    r+="\treturn\n"
    r+=".end method\n"
    r+="\n"
    r+=".method public static main([Ljava/lang/String;)V\n"
    r+=".limit locals 1\n"
    r+="\tinvokestatic %s/main()I\n" % classname
    r+="\tpop\n"
    r+="\treturn\n"
    r+=".end method\n"
    return r

def get_signature(f):
    '''Returns the signature of a function'''
    asignature=[]
    for i in f.listargument_:
        p=prefix[i.type_.__class__]
        if len(prefix[i.type_.__class__][0])==1:
            t=prefix[i.type_.__class__][0].upper()
        else:
            t=prefix[i.type_.__class__][0]
        asignature.append(t)
        
    return '%s(%s)%s' % (f.cident_, ''.join(asignature) , prefix[f.type_.__class__][0].upper())
    
class cfunction():
    '''Purpose of this class is to compile a function'''
    def __init__(self,f,inf,contx,classname):
        '''f:   Fnct object to compile
        inf: inferred class to access the type of the expressions
        contx is the context that contains the other functions
        classname is the name of the class itself'''
        self.contx=contx #Context, contains the declarations of the other functions
        
        self.classname=classname
        
        self.lbl=labeler()  #Unique label sequence for the function
        self.variables=context.var_env()    #Variables
        
        self.inf=inf
        
        #Inserting variables of the declaration in the context
        for i in f.listargument_:
            p=prefix[i.type_.__class__]
            self.variables.put(i.cident_,p[1])
        
        self.f=f; #Function is retrievable
        
        
        #Used to know the max operand stack size
        self.opstack=0;
        self.maxopstack=0;
        self.opcodes=[]
        
        self.code=None
        
    def fcompile(self):
        '''Returns the jasmin assembly for the function
        This function compiles only the 1st time it is invoked.
        The other times it will only return the same string'''
        
        if self.code!=None:
            return self.code
        
        self.compile_block(self.f.liststatement_)
        
        self.opcodes=improve.improve(self.opcodes)
        
        r='\n'
        r+= ".method public static %s\n" % get_signature(self.f)
        r+= ".limit locals %d\n" % self.variables.getmax()
        r+= ".limit stack %d\n" % self.maxopstack
        
        for i in self.opcodes:
            r+="\t%s\n" % i
        r+= ".end method\n"
        
        self.code=r
        return r
        
    def emit(self,instr,s):
        '''Emits an instruction and calculates the stack operand size'''
        self.opstack+=s
        if self.opstack>self.maxopstack:
            self.maxopstack=self.opstack
        self.opcodes.append(instr)
        
    def compile_block(self,statements):
        '''This function compiles a block, or the main block of a function'''
        if len(statements)==0:
            self.emit("nop",0)
            
        for i in statements:
            if isinstance(i,cpp.Absyn.Expression):    #Expression
                self.compile_expr(i.expr_)
                qq=self.inf.getinfer(i.expr_)
                
                if isinstance(qq,cpp.Absyn.Typedouble): #If double, remove two words
                    self.emit("pop2",-2)
                elif not isinstance(qq,cpp.Absyn.Typevoid): #If not void, we remove the return value
                    self.emit ("pop",-1)     #An expression returns a value, so we pop it now to free the stack
                    
            elif isinstance(i,cpp.Absyn.LocalVars):   #Var declaration (multiple vars)
                for j in i.listvitem_:
                    p=prefix[i.type_.__class__]
                    self.variables.put(j.cident_,p[1])
                
                    if isinstance(j,cpp.Absyn.VarNA): #Declaration without assignment
                        self.emit("%sconst_0"%p[0],p[1])
                    else:
                        self.compile_expr(j.expr_)
                    self.emit("%sstore %d" % (p[0],self.variables.get(j.cident_)),-1)
            elif isinstance(i,cpp.Absyn.Block): #New context
                self.variables.push()
                self.compile_block(i.liststatement_)
                self.variables.pop()
            elif isinstance(i,cpp.Absyn.If) or isinstance(i,cpp.Absyn.IfElse): #//TODO if
                
                if self.inf.getinfer(i.expr_)==True:
                    self.compile_block((i.statement_1,))  #True branch
                    continue
                elif self.inf.getinfer(i.expr_)==False:
                    self.compile_block((i.statement_2,))  #True branch
                    continue
                    
                self.compile_expr(i.expr_) #Pushing the result of the condition
                lab1=self.lbl.getlbl()
                self.emit( "ifeq else%d" % lab1,-1)    #If expr is false
                self.compile_block((i.statement_1,))  #True branch
                self.emit( "goto endif%d" %lab1,0)
                self.emit( "else%d:" % lab1,0)
                
                if isinstance(i,cpp.Absyn.IfElse):
                    self.compile_block((i.statement_2,))  #False branch
                    
                self.emit( "endif%d:" %lab1,0)
            elif isinstance(i,cpp.Absyn.While):
                lab1=self.lbl.getlbl()
                
                if self.inf.getinfer(i.expr_)==True:
                    self.emit ( "while%d:" % lab1,0)
                    self.compile_block((i.statement_,))  #While body
                    self.emit ( "goto while%d" % lab1,0)
                    continue
                elif self.inf.getinfer(i.expr_)==False:
                    self.emit("nop",0)
                    continue
                
                self.emit ( "while%d:" % lab1,0)
                self.compile_expr(i.expr_)
                self.emit ("ifeq endwhile%d" % lab1,-1)  #If condition is false, exits
                self.compile_block((i.statement_,))  #While body
                self.emit ( "goto while%d" % lab1,0)
                self.emit ( "endwhile%d:" % lab1,0)
            elif isinstance(i,cpp.Absyn.VoidReturn):
                self.emit("return",0)
            elif isinstance(i,cpp.Absyn.Return):
                self.compile_expr(i.expr_)
                
                p=prefix[self.f.type_.__class__]
                self.emit("%sreturn" % p[0],-1)


    def compile_expr(self,e):
        '''
        Eand.       Expr4           ::= Expr4 "&&" Expr5;
        Eor.        Expr3           ::= Expr3 "||" Expr4;
        '''
    
        dic= {
            cpp.Absyn.Eadd: "add",
            cpp.Absyn.Emul: "mul",
            cpp.Absyn.Esub: "sub",
            cpp.Absyn.Ediv: "div",
            cpp.Absyn.Emod: "rem"
        }
    
        comp_dic= {
            cpp.Absyn.Egt: "if_icmpgt",
            cpp.Absyn.Elt: "if_icmplt",
            cpp.Absyn.Eelt: "if_icmple",
            cpp.Absyn.Eegt: "if_icmpge",
            cpp.Absyn.Eeql: "if_icmpeq",
            cpp.Absyn.Edif: "if_icmpne"
        }
        
        dcomp_dic = {
                cpp.Absyn.Egt: "ifgt",
                cpp.Absyn.Elt: "iflt",
                cpp.Absyn.Eelt: "ifle",
                cpp.Absyn.Eegt: "ifge",
                cpp.Absyn.Eeql: "ifeq",
                cpp.Absyn.Edif: "ifne"
        }
    
        if isinstance(e,cpp.Absyn.Eint): #Integer value
            self.emit("ldc %d" % e.integer_,1)
        elif isinstance(e,cpp.Absyn.Ebool): #Boolean value
            if isinstance(e.bool_,cpp.Absyn.TrueLit):
                self.emit("iconst_1",1) #True
            else:
                self.emit("iconst_0",1) #False
        elif isinstance(e,cpp.Absyn.Estrng): #String constant value
            self.emit("ldc \"%s\""% e.string_,2) #//TODO I have no clue how big is pushing a string constant on the stack
        elif isinstance(e,cpp.Absyn.Edbl): #Double value
            self.emit("ldc2_w %lf"%e.double_,2)
        elif isinstance(e,cpp.Absyn.Eitm): #Loads Variable
            r=prefix[self.inf.getinfer(e).__class__]
            self.emit ("%sload %d" % (r[0],self.variables.get(e.cident_)),r[1])
        elif isinstance(e,cpp.Absyn.Eass): #Assignment
            self.compile_expr(e.expr_2)
            qq=self.inf.getinfer(e)
            p=prefix[qq.__class__]
            
            if isinstance(qq,cpp.Absyn.Typedouble):
                self.emit("dup2",2) #Needed becaus assignment returns a value as well
            else:
                self.emit("dup",1) #Needed becaus assignment returns a value as well
            
            self.emit("%sstore %d" % (p[0],self.variables.get(e.expr_1.cident_)),p[1]*-1)
        elif isinstance(e,cpp.Absyn.Eainc): #var++
            self.emit ("iload %d" % self.variables.get(e.expr_.cident_),1) #Load var on stack
            self.emit ("iinc %d 1" % self.variables.get(e.expr_.cident_),0) #increment variable
        elif isinstance(e,cpp.Absyn.Epinc): #++var
            self.emit("iinc %d 1" % self.variables.get(e.expr_.cident_),0) #increment variable
            self.emit("iload %d" % self.variables.get(e.expr_.cident_),1) #Load var on stack
        elif isinstance(e,cpp.Absyn.Eadec): #var--
            self.emit ("iload %d" % self.variables.get(e.expr_.cident_),1) #Load var on stack
            self.emit ("iinc %d -1" % self.variables.get(e.expr_.cident_),0) #increment variable
        elif isinstance(e,cpp.Absyn.Epdec): #--var
            self.emit("iinc %d -1" % self.variables.get(e.expr_.cident_),0) #increment variable
            self.emit("iload %d" % self.variables.get(e.expr_.cident_),1) #Load var on stack    
        elif isinstance(e,cpp.Absyn.Efun): #Function call
            #Emits code for the params
            before=self.opstack
            for q in e.listexpr_:
                self.compile_expr(q)
            after=self.opstack
            
            f=self.contx.get(e.cident_)
            
            p=prefix[f.type_.__class__]
            
            #Distinguishes between builtin functions and normal ones. I am not proud of this code.
            if e.cident_ in typechecker.builtins:
                cname="runtime"
            else:
                cname=self.classname
            
            self.emit("invokestatic %s/%s" % (cname,get_signature(f)),before-after+p[1])
            
        elif isinstance(e,cpp.Absyn.ENot):
            self.compile_expr(e.expr_)
            l=self.lbl.getlbl()
            
            l1="negation_t%d" %l 
            l2="negation_f%d" %l
            self.emit("ifne %s"%l2,-1)
            self.emit("iconst_1",1)
            self.emit("goto %s" % l1,0)
            self.emit("%s:" % l2,0)
            self.emit("iconst_0",1)
            
            #The -1 there is because otherwise the stack will grow, considering that both expr_2 and iconst_0 will be executed, which is not possible
            self.emit("%s:"%l1,-1)
            
        elif isinstance(e,cpp.Absyn.ENeg):
            self.compile_expr(e.expr_)
            p=prefix[self.inf.getinfer(e).__class__]
            self.emit("%sneg"%p[0],0)
    
        elif isinstance(e,cpp.Absyn.Eand):  #Short-circuit and operator
            lab1=self.lbl.getlbl()
            self.compile_expr(e.expr_1)  #Evaluating 1st operand
            self.emit( "ifeq andfalse%d" % lab1,-1)  #If 1st operand is false
            self.compile_expr(e.expr_2)  #Evaluating 2nd operand, that will give the value to the expression
            self.emit("goto endand%d" % lab1,0)
            self.emit("andfalse%d:" % lab1,0)
            self.emit("iconst_0",1)    #push false
            
            #The -1 there is because otherwise the stack will grow, considering that both expr_2 and iconst_0 will be executed, which is not possible
            self.emit("endand%d:" % lab1,-1)   
            
        elif isinstance(e,cpp.Absyn.Eor):  #Short-circuit or operator
            lab1=self.lbl.getlbl()
            self.compile_expr(e.expr_1)  #Evaluating 1st operand
            self.emit("ifne  ortrue%d" % lab1,-1)  #expr1 true,
            self.compile_expr(e.expr_2)  #2nd operand
            self.emit("goto endor%d" % lab1,0)
            self.emit("ortrue%d:" % lab1,0)
            
            self.emit("iconst_1",1) #pushing the true value
            
            #The -1 there is because otherwise the stack will grow, considering that both expr_2 and iconst_0 will be executed, which is not possible
            self.emit("endor%d:" %lab1,-1)
        elif e.__class__ in comp_dic and self.inf.getinfer(e.expr_1).__class__ in (cpp.Absyn.Typebool, cpp.Absyn.Typeint):   #Comparison int, boolean
            self.compile_expr(e.expr_1) #Pushing operands
            self.compile_expr(e.expr_2)
        
            lab1=self.lbl.getlbl()   #Getting label
        
            self.emit ("%s trueexpr%d" % (comp_dic[e.__class__],lab1),-2)
            self.emit("iconst_0",1)    #False
            self.emit("goto endexpr%d" % lab1,0)
            self.emit("trueexpr%d:" % lab1,0)
            self.emit("iconst_1",1)    #True
            
            #The -1 there is because otherwise the stack will grow, considering that both expr_2 and iconst_0 will be executed, which is not possible
            self.emit("endexpr%d:" %lab1,-1)
        elif e.__class__ in dcomp_dic and isinstance(self.inf.getinfer(e.expr_1),cpp.Absyn.Typedouble): #Dobule comparison
            self.compile_expr(e.expr_1) #Pushing operands
            self.compile_expr(e.expr_2)
            self.emit("dcmpg",-3)
            
            l=self.lbl.getlbl()
            l1="doublecomp%d" % l
            l2="enddoublecomp%d" % l
            
            self.emit("%s %s" % (dcomp_dic[e.__class__],l1),-1)
            self.emit("iconst_0",1)    #False
            self.emit("goto %s"%l2,0)
            self.emit("%s:"%l1,0)
            self.emit("iconst_1",1)    #True
            
            #The -1 there is because otherwise the stack will grow, considering that both expr_2 and iconst_0 will be executed, which is not possible
            self.emit("%s:"%l2,-1)
        elif e.__class__ in dic: #Aritmetic operations
            self.compile_expr(e.expr_1)
            self.compile_expr(e.expr_2)
            
            p=prefix[self.inf.getinfer(e).__class__]
                        
            
            self.emit("%s%s" % (p[0],dic[e.__class__]),-1)

if __name__=="__main__":
    for f in range(1,len(sys.argv)):
        ijvm_compile(sys.argv[f])