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

'''
-- Grammar for Javalette    Salvo 'LtWorf' Tomaselli
entrypoints Program ;
comment "//" ;
comment "/*" "*/" ;
comment "#";    --Stripping out preprocessor stuff. This will make it just not work on some real-life code.
position token CIdent (letter | '_') (letter | digit | '_')*;       --Identifiers start with letter or '_' and then can have numbers too.


Program.            Program             ::= [Declaration];
TrueLit.            Bool                ::= "true";    --Naming it boolean it won't compile
FalseLit.           Bool                ::= "false";
Typestrng.          Type                ::= "string";    --Maybe someone will not like this?
Typebool.           Type                ::= "boolean";
Typedouble.         Type                ::= "double";
Typeint.            Type                ::= "int";
Typevoid.           Type                ::= "void";
[].                 [Declaration]       ::= ;--Allow empty declaration list
(:).                [Declaration]       ::= Declaration [Declaration];
[].                 [Statement]         ::= ; --Allow empty statement list
(:).                [Statement]         ::= Statement [Statement];
Argument.           Argument            ::= Type CIdent;
[].                 [Argument]          ::= ; --3 rules to have no arguments, and having the ending argument without the ','
(:[]).              [Argument]          ::= Argument;
(:).                [Argument]          ::= Argument "," [Argument];
Fnct.               Declaration         ::= Type CIdent "(" [Argument] ")" "{" [Statement] "}"; --2nd part of function declaration. Splitted for conflicts problems
(:[]).              [VItem]             ::= VItem;
(:).                [VItem]             ::= VItem "," [VItem];
[].                 [Expr]              ::= ;
(:[]).              [Expr]              ::= Expr;
(:).                [Expr]              ::= Expr "," [Expr];
coercions Expr 16 ;
'''

import typechecker
import sys
import cpp
import context
import inferred
import improve
import os.path
import options
import lcontext

def llvm_compile(filename):
    '''Compiles the program into LLVM assembly'''
    prog,contx,inf=typechecker.checkfile(filename)
    
    #Gets the name of the module
    mname='.'.join(os.path.basename(filename).split('.')[:-1])
    
    mod=module(prog,contx,inf,mname)
    
    dname='%s/%s.ll' % (os.path.dirname(filename),mname)
    f=file(dname,"w")
    
    
    #Declarations
    f.write('declare void @printInt(i32 %x)\n')
    f.write('declare void @printDouble(double %x)\n')
    f.write('declare void @printString(i8* %s)\n')
    f.write('declare i32 @readInt()\n')
    f.write('declare double @readDouble()\n')


    
    for i in mod.code:
        f.write('%s\n'% i)
    f.close()
    return dname

class module():
    '''This class contains the description of a compilation module and can be
    used to compile it.'''
    
    def __init__(self,prog,contx,inf,mname):
        self.labelcount=-1
        self.constcount=0
        self.const={}
        
        self.prog=prog
        self.contx=contx
        self.inf=inf
        self.mname=mname
        self.code=[]
        
        for i in prog.listdeclaration_:
            c=function(i,contx,inf,mname,self)
            for j in c.code:
                self.code.append(j)
        
        
        #Adding consts in the header
        for i in self.const:
            self.code.insert(0,'%s = internal constant [%d x i8] c"%s\\00"' % (self.const[i],len(i)+1,i))
        pass
    
    def get_lbl(self):
        '''Returns a module-unique id for a new label'''
        self.labelcount+=1
        return self.labelcount
    
    def add_constant(self,cnst):
        if cnst not in self.const:
            self.const[cnst]='@const_%d' % self.constcount
            self.constcount+=1
        return self.const[cnst]
    
    def get_size(self,type_):
        if isinstance(type_,cpp.Absyn.Typeint):
            return 'i32'
        elif isinstance(type_,cpp.Absyn.Typebool):
            return 'i1'
        elif isinstance(type_,cpp.Absyn.Typestrng):
            return 'i8*'
        elif isinstance(type_,cpp.Absyn.Typedouble):
            return 'double'
        elif isinstance(type_,cpp.Absyn.Typevoid):
            return 'void'
        else: #/TODO REMOVE THIS!!!
            return '128'
    
class function():
    def __init__(self,f,contx,inf,mname,module):
        self.aritm= {# Dictionary to compile operations with integers and doubles
            cpp.Absyn.Typeint: {cpp.Absyn.Emul:'mul',cpp.Absyn.Ediv:'sdiv',cpp.Absyn.Emod:'srem',cpp.Absyn.Eadd:'add',cpp.Absyn.Esub:'sub'},
            cpp.Absyn.Typedouble: {cpp.Absyn.Emul:'fmul',cpp.Absyn.Ediv:'fdiv',cpp.Absyn.Emod:'frem',cpp.Absyn.Eadd:'fadd',cpp.Absyn.Esub:'fsub'},
        }
        
        self.comparisons= {# Dictionary to compile operations with comparisons
            cpp.Absyn.Typeint: {cpp.Absyn.Elt :'slt',cpp.Absyn.Egt :'sgt',cpp.Absyn.Eelt:'sle',cpp.Absyn.Eegt:'sge',cpp.Absyn.Eeql:'eq',cpp.Absyn.Edif:'ne'},
            cpp.Absyn.Typedouble: {cpp.Absyn.Elt :'olt',cpp.Absyn.Egt :'ogt',cpp.Absyn.Eelt:'ole',cpp.Absyn.Eegt:'oge',cpp.Absyn.Eeql:'oeq',cpp.Absyn.Edif:'one'},
        }
        
        #Function to compile
        self.fnct=f
        
        #Context from typechecker (only contains the other functions)
        self.contx=contx
        
        #Inferred types for the expression (see inferred module)
        self.inf=inf
        
        #Module name
        self.mname=mname
        
        #Module class (that called this method)
        self.module=module
        
        #Counter for the register
        self.register=-1
        
        #Counter for the vars
        self.var_name=-1
        
        #Context to keep trace of the new names of the vars
        self.var_contx=lcontext.v_context()
        
        #Code
        self.code=[]
        
        
        self.var_contx.push()

        args=[]
        par=0
        for i in f.listargument_:
            size=module.get_size(i.type_)
            p='%%par_%d' % par
            args.insert(0,'%s %s' % (size,p))
            par+=1
        params=','.join(args)
        
        self.emit("define %s @%s(%s) {" % (self.module.get_size(f.type_),f.cident_,params))
        
        self.emit("entry:")
        
        #Puts params to the stack
        par=0
        for i in f.listargument_:
            var=self.get_var_name()
            self.var_contx.put(i.cident_,var)
            self.emit('%s = alloca %s' % (var,size))
            p='%%par_%d' % par
            self.emit('store %s %s, %s* %s' % (size,p,size,var))
            par+=1
        
        self.compile_block(f.liststatement_)
        
        #Adds an 'unreachable' statement if needed
        if self.code[len(self.code)-1].endswith(':'):
            self.emit('unreachable')
        
        
        self.emit("}")
        
        self.var_contx.pop()
        pass
    
    def get_register_id(self):
        self.register+=1
        return self.register
        
    def get_var_name(self):
        '''Returns a name for a new variable'''
        self.var_name+=1
        return '%%v_%d' % self.var_name
        
    
    def emit(self,instr):
        self.code.append(instr)
        #/TODO just temporary
        print instr
    
    def compile_block(self,statements,new_context=True):
        if new_context:
            self.var_contx.push()
        
        for instr_id in range(len(statements)):
            i=statements[instr_id]
            
            if isinstance(i,cpp.Absyn.Expression):
                self.compile_expr(i.expr_)
            elif isinstance(i,cpp.Absyn.VoidReturn):
                self.emit('ret void')
            elif isinstance(i,cpp.Absyn.Return):
                r1=self.compile_expr(i.expr_)
                self.emit('ret %s %s' % (self.module.get_size( self.inf.getinfer(i.expr_)),r1))
            elif isinstance(i,cpp.Absyn.Block):
                self.compile_block(i.liststatement_)
            elif isinstance(i,cpp.Absyn.If) or isinstance(i,cpp.Absyn.IfElse):
                
                #Code generation if the condition is constant
                if isinstance(i,cpp.Absyn.IfElse):
                    if self.inf.getinfer(i.expr_)==True:
                        self.compile_block((i.statement_1,),False)  #True branch
                        continue
                    elif self.inf.getinfer(i.expr_)==False:
                        self.compile_block((i.statement_2,),False)  #False branch
                        continue
                else: #Simple if
                    if self.inf.getinfer(i.expr_)==True:
                        self.compile_block((i.statement_,),False)  #True branch
                        continue
                    elif self.inf.getinfer(i.expr_)==False:
                        continue
                                
                #Normal code generation
                r1=self.compile_expr(i.expr_) #Calculate the expression
                
                
                #Labels
                l_id=self.module.get_lbl()
                lbl_if='if_%d' % l_id
                lbl_else='else_%d' % l_id
                lbl_endif='endif_%d' % l_id
                
                #Emitting the code
                self.emit('br i1 %s , label %%%s , label %%%s' % (r1,lbl_if,lbl_else) )
                
                self.emit('%s:' % lbl_if) # IF
                if isinstance(i,cpp.Absyn.IfElse):
                    self.compile_block((i.statement_1,),False)
                else:
                    self.compile_block((i.statement_,),False)
                self.emit('br label %%%s' % (lbl_endif))
                
                self.emit('%s:' % lbl_else) # ELSE
                if isinstance(i,cpp.Absyn.IfElse):
                    self.compile_block((i.statement_2,),False)
                self.emit('br label %%%s' % (lbl_endif))
                
                self.emit('%s:' % lbl_endif) # ENDIF
            elif isinstance(i,cpp.Absyn.While) or isinstance(i,cpp.Absyn.DoWhile):    #While/Do-while loop
                #Labels
                l_id=self.module.get_lbl()
                lbl_while="while_%d" %l_id
                lbl_expr="expr_%d" %l_id
                lbl_endwhile="endwhile_%d" %l_id
                
                #Code generation if the condition is constant
                if self.inf.getinfer(i.expr_)==True:
                    self.emit('br label %%%s' % (lbl_while))
                    self.emit ( "%s:" % lbl_while)
                    self.compile_block((i.statement_,),False)  #While body
                    self.emit('br label %%%s' % (lbl_while))
                    self.emit('unreachable')
                    if options.warningLevel>2:
                        print "WARNING: infinite loop detected. This warning will be shown until the problem will be fixed"
                    continue
                elif self.inf.getinfer(i.expr_)==False and isinstance(i,cpp.Absyn.While):
                    if options.warningLevel>2:
                        print  "WARNING: never executed while loop"
                    continue
                elif self.inf.getinfer(i.expr_)==False and isinstance(i,cpp.Absyn.DoWhile):
                    self.compile_block((i.statement_,),False)
                    if options.warningLevel>2:
                        print "WARNING: do-while will be executed only once"
                    continue
                
                #A do-while always executes the 1st time
                if isinstance(i,cpp.Absyn.While):
                    self.emit('br label %%%s' % (lbl_expr))
                else:
                    self.emit('br label %%%s' % (lbl_while))
                    
                self.emit ( "%s:" % lbl_while)
                self.compile_block((i.statement_,),False)  #While body
                
                self.emit('br label %%%s' % (lbl_expr))
                
                
                self.emit ( "%s:" % lbl_expr)
                
                r1=self.compile_expr(i.expr_) #Calculate the expression
                
                self.emit('br i1 %s , label %%%s , label %%%s' % (r1,lbl_while,lbl_endwhile) )
                
                self.emit ( "%s:" % lbl_endwhile)
            elif isinstance(i,cpp.Absyn.LocalVars):
                size=self.module.get_size(i.type_)
                for j in i.listvitem_:
                    var=self.get_var_name()
                    self.emit('%s = alloca %s' % (var,size))
                    
                    if isinstance(j,cpp.Absyn.VarNA):
                        #Inits the var to 0
                        if isinstance(i.type_,cpp.Absyn.Typedouble):
                            zero='0.0'
                        else:
                            zero='0'
                            
                        self.emit('store %s %s, %s* %s' % (size,zero,size,var))
                    elif isinstance(j,cpp.Absyn.VarVA):
                        r1=self.compile_expr(j.expr_)
                        self.emit('store %s %s, %s* %s' % (size,r1,size,var))
                    self.var_contx.put(j.cident_,var)
        if new_context:
            self.var_contx.pop()
        
        pass
    
    def compile_expr(self,expr):
        id_='%%t%d' % self.get_register_id()
        expr_size=self.module.get_size( self.inf.getinfer(expr))
        
        if isinstance(expr,cpp.Absyn.Eint):
            #self.emit('%s = add %s 0 , %d' % (id_,self.module.get_size( self.inf.getinfer(expr)),expr.integer_))
            return str(expr.integer_)
        elif isinstance(expr,cpp.Absyn.Edbl):
            return str(expr.double_)
        elif isinstance(expr,cpp.Absyn.Ebool):
            if isinstance(expr.bool_,cpp.Absyn.TrueLit):
                return 'true'
            elif isinstance(expr.bool_,cpp.Absyn.FalseLit):
                return 'false'
        elif isinstance(expr,cpp.Absyn.Estrng):
            handle=self.module.add_constant(expr.string_)
            self.emit('%s = bitcast [%d x i8]* %s to i8*' % (id_,len(expr.string_)+1,handle))
        #Arithmetic instructions
        elif expr.__class__ in self.aritm[cpp.Absyn.Typeint]:
            r1=self.compile_expr(expr.expr_1)
            r2=self.compile_expr(expr.expr_2)
           
            op=self.aritm[self.inf.getinfer(expr).__class__][expr.__class__]
            self.emit('%s = %s %s %s , %s' % (id_,op,expr_size,r1,r2 ))
        #Comparisons
        elif expr.__class__ in self.comparisons[cpp.Absyn.Typeint]:
            r1=self.compile_expr(expr.expr_1)
            r2=self.compile_expr(expr.expr_2)
            
            op=self.comparisons[self.inf.getinfer(expr.expr_1).__class__][expr.__class__]
            
            if isinstance(self.inf.getinfer(expr.expr_1),cpp.Absyn.Typeint):
                int_or_float='i'
            else:
                int_or_float='f'
            
            type_=self.module.get_size(self.inf.getinfer(expr.expr_1))
            
            self.emit('%s = %ccmp %s %s %s , %s'%(id_,int_or_float,op,type_,r1,r2))
        #Variable
        elif isinstance(expr,cpp.Absyn.Eitm):
            var=self.var_contx.get(expr.cident_)
            self.emit('%s = load %s* %s' % (id_,expr_size,var))
        #Assignment (as expression, not as statement)
        elif isinstance(expr,cpp.Absyn.Eass):
            var=self.var_contx.get(expr.expr_1.cident_)
            r1=self.compile_expr(expr.expr_2)
            self.emit('store %s %s, %s* %s' % (expr_size,r1,expr_size,var))
            return r1
        #Pre and post increment/decrement
        elif isinstance(expr,cpp.Absyn.Eainc):
            r1=self.compile_expr(expr.expr_)
            self.emit('%s = add %s 1 , %s' % (id_,expr_size,r1))
            var=self.var_contx.get(expr.expr_.cident_)
            self.emit('store %s %s, %s* %s' % (expr_size,id_,expr_size,var))
            return r1
        elif isinstance(expr,cpp.Absyn.Eadec):
            r1=self.compile_expr(expr.expr_)
            self.emit('%s = sub %s %s , 1' % (id_,expr_size,r1))
            var=self.var_contx.get(expr.expr_.cident_)
            self.emit('store %s %s, %s* %s' % (expr_size,id_,expr_size,var))
            return r1
        elif isinstance(expr,cpp.Absyn.Epinc):
            r1=self.compile_expr(expr.expr_)
            self.emit('%s = add %s 1 , %s' % (id_,expr_size,r1))
            var=self.var_contx.get(expr.expr_.cident_)
            self.emit('store %s %s, %s* %s' % (expr_size,id_,expr_size,var))
        elif isinstance(expr,cpp.Absyn.Epdec):
            r1=self.compile_expr(expr.expr_)
            self.emit('%s = sub %s %s , 1' % (id_,expr_size,r1))
            var=self.var_contx.get(expr.expr_.cident_)
            self.emit('store %s %s, %s* %s' % (expr_size,id_,expr_size,var))
        #Function call
        elif isinstance(expr,cpp.Absyn.Efun):
            parlist=[]
            for i in expr.listexpr_:
                r=self.compile_expr(i)
                size=self.module.get_size( self.inf.getinfer(i))
                parlist.insert(0,'%s %s'% (size,r))
            
            params=','.join(parlist)
            
            if isinstance(self.inf.getinfer(expr),cpp.Absyn.Typevoid):
                #Call to void
                self.emit ('call void @%s (%s)' % (expr.cident_,params))
            else:
                #Normal call with result
                self.emit ('%s = call %s @%s (%s)' % (id_,expr_size,expr.cident_,params))
        #Short-circuit AND
        elif isinstance(expr,cpp.Absyn.Eand):
            l_id=self.module.get_lbl()
            lbl_begin='and_begin_%d' % l_id
            lbl_second='and_second_%d' % l_id
            lbl_end='and_end_%d' % l_id
            
            #I need the and to be in a block for the phi instruction
            self.emit('br label %%%s' % (lbl_begin))
            self.emit('%s:' % lbl_begin)
            r1=self.compile_expr(expr.expr_1)
                
            self.emit('br i1 %s , label %%%s , label %%%s' % (r1,lbl_second,lbl_end) )
            self.emit('%s:' % lbl_second)
            r2=self.compile_expr(expr.expr_2)
            self.emit('br label %%%s' % (lbl_end))
            self.emit('%s:' % lbl_end)
            
            #Assign the value depending on from which block is jumping here
            self.emit('%s = phi %s [ 0 , %%%s ] , [ %s , %%%s ]' % (id_,expr_size,lbl_begin,r2,lbl_second))
            
        
        '''
        ENeg.               Expr12              ::= "-" Expr13 ;
        ENot.               Expr12              ::= "!" Expr13 ;
        Eand.               Expr4               ::= Expr4 "&&" Expr5;
        Eor.                Expr3               ::= Expr3 "||" Expr4;
        '''

        return id_
    
    
    
    
    
    
    
    
    
    
    
    
    