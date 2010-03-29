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
import os.path


prefix= {
        cpp.Absyn.Typeint:("i",1),
        cpp.Absyn.Typebool:("i",1),
        cpp.Absyn.Typedouble:("d",2),
        cpp.Absyn.Typevoid:("v",0)
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
    
    
    print class_header(cname)
    for i in prog.listdeclaration_:
        c=cfunction(i,inf,contx,cname)
        print c.fcompile()

def class_header(classname):
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
    r+="\tinvokestatic %s/main()I\n"
    r+="\tpop\n"
    r+="\treturn\n"
    r+=".end method\n"
    return r
def get_signature(f):
    asignature=[]
    for i in f.listargument_:
        p=prefix[i.type_.__class__]
        asignature.append(prefix[i.type_.__class__][0].upper())
        
    return '%s(%s)%s' % (f.cident_, ','.join(asignature) , prefix[f.type_.__class__][0].upper())
    
class cfunction():
    '''Purpose of this class is to compile a function'''
    def __init__(self,f,inf,contx,classname):
        '''f:   Fnct object to compile
        inf: inferred class to access the type of the expressions'''
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
        
        
        #TODO optimize
        
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
        for i in statements:
            if isinstance(i,cpp.Absyn.Expression):    #Expression
                self.compile_expr(i.expr_)
            
                if not isinstance(self.inf.getinfer(i.expr_),cpp.Absyn.Typevoid): #If not void, we remove the return value
                    self.emit ("pop",-1)     #An expression returns a value, so we pop it now to free the stack
            elif isinstance(i,cpp.Absyn.LocalVars):   #Var declaration (multiple vars)
                for j in i.listvitem_:
                    p=prefix[i.type_.__class__]
                    self.variables.put(j.cident_,p[1])
                
                    if isinstance(j,cpp.Absyn.VarNA): #Declaration without assignment
                        self.emit("iconst_0",1)
                    else:
                        self.compile_expr(j.expr_)
                    self.emit("%sstore %d" % (p[0],self.variables.get(j.cident_)),-1)
            elif isinstance(i,cpp.Absyn.Block): #New context
                self.variables.push()
                self.compile_block(i.liststatement_)
                self.variables.pop()
            elif isinstance(i,cpp.Absyn.IfElse): #//TODO if
                self.compile_expr(i.expr_) #Pushing the result of the condition
            
                lab1=self.lbl.getlbl()
            
                self.emit( "ifeq else%d" % lab1,-1)    #If expr is false
                self.compile_block((i.statement_1,))  #True branch
                self.emit( "goto endif%d" %lab1,0)
                self.emit( "else%d:" % lab1,0)
                self.compile_block((i.statement_2,))  #False branch
                self.emit( "endif%d:" %lab1,0)
            elif isinstance(i,cpp.Absyn.While):
                lab1=self.lbl.getlbl()
            
                self.emit ( "while%d:" % lab1,0)
                self.compile_expr(i.expr_)
                self.emit ("ifeq endwhile%d" % lab1,-1)  #If condition is false, exits
                self.compile_block((i.statement_,))  #While body
                self.emit ( "goto while%d" % lab1,0)
                self.emit ( "endwhile%d:" % lab1,0)
            elif isinstance(i,cpp.Absyn.Return):
                self.compile_expr(i.expr_)
                
                p=prefix[self.f.type_.__class__]
                self.emit("%sreturn" % p[0],-1) #//TODO return the correct type 


    def compile_expr(self,e):
        '''
        Edbl.       Expr16          ::= Double;
        Ebool.      Expr16          ::= Bool;
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
        Eass    .       Expr2           ::= Expr3 "=" Expr2;        --I think this was wrong in lab1
    
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
                self.emit("iconst_m1",1)
            elif e.integer_ in range(-1,6):
                self.emit("iconst_%d" % e.integer_,1)
            elif e.integer_ in range(-129,128):   #Push byte
                self.emit ("bipush %d"%e.integer_,1)
            elif e.integer_ in range(-32769,32768): #Push short
                self.emit("sipush %d" % e.integer_ ,1)
            else:                                   #Push integer
                self.emit("ldc %d" % e.integer_,1)
        elif isinstance(e,cpp.Absyn.Ebool): #Boolean value
            if isinstance(e.bool_,cpp.Absyn.TrueLit):
                self.emit("iconst_1",1) #True
            else:
                self.emit("iconst_0",1) #False
        elif isinstance(e,cpp.Absyn.Estrng): #String constant value
            self.emit("ldc \"%s\""% e.string_,4) #//TODO I have no clue how big is pushing a string constant on the stack
        elif isinstance(e,cpp.Absyn.Edbl): #Double value
            self.emit("ldc_w %lf"%e.double_,2)
        elif isinstance(e,cpp.Absyn.Eitm): #Loads Variable
            r=prefix[self.inf.getinfer(e).__class__]
            self.emit ("%sload %d" % (r[0],self.variables.get(e.cident_)),r[1])
        elif isinstance(e,cpp.Absyn.Eass): #Assignment
            self.compile_expr(e.expr_2)
            self.emit("dup",1) #Needed becaus assignment returns a value as well
            p=prefix[self.inf.getinfer(e).__class__]
            self.emit("%sstore %d" % (p[0],self.variables.get(e.expr_1.cident_)),-1)
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
            
            self.emit("invokestatic %s/%s" % (self.classname,get_signature(f)),before-after+p[1])
            
            
            
            
            
            
            
            
            
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
        elif e.__class__ in comp_dic:   #Comparison
            self.compile_expr(e.expr_1) #Pushing operands
            self.compile_expr(e.expr_2)
        
            lab1=self.lbl.getlbl()   #Getting label
        
            print "%s trueexpr%d" % (comp_dic[e.__class__],lab1)
            print "bipush 0"    #False
            print "goto endexpr%d" % lab1
            print "trueexpr%d:" % lab1
            print "bipush 1"    #True
            print "endexpr%d:" %lab1
        elif e.__class__ in dic: #Aritmetic operations
            self.compile_expr(e.expr_1)
            self.compile_expr(e.expr_2)
            self.emit(dic[e.__class__],-1)

if __name__=="__main__":
    for f in range(1,len(sys.argv)):
        ijvm_compile(sys.argv[f])