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
    #dname='%s/%s.j' % (os.path.dirname(filename),cname)
    #f=file(dname,"w")
    
    #f.write( class_header(cname))
    #for i in prog.listdeclaration_:
    #    c=cfunction(i,inf,contx,cname)
    #    f.write(c.fcompile())
    #f.close()
    #return dname

class module():
    '''This class contains the description of a compilation module and can be
    used to compile it.'''
    
    def __init__(self,prog,contx,inf,mname):
        self.labelcount=-1
        self.prog=prog
        self.contx=contx
        self.inf=inf
        self.mname=mname
        
        for i in prog.listdeclaration_:
            c=function(i,contx,inf,mname,self)
        pass
    
    def get_lbl(self):
        '''Returns a module-unique id for a new label'''
        self.labelcount+=1
        return self.labelcount
    
    def add_constant(self):
        pass
    
    def get_size(self,type_):
        if isinstance(type_,cpp.Absyn.Typeint):
            return 32
        elif isinstance(type_,cpp.Absyn.Typebool):
            return 1
        else: #/TODO REMOVE THIS!!!
            return 128
    
class function():
    def __init__(self,f,contx,inf,mname,module):
        self.aritm= {# Dictionary to compile operations with integers and doubles
            cpp.Absyn.Typeint: {cpp.Absyn.Emul:'mul',cpp.Absyn.Ediv:'sdiv',cpp.Absyn.Emod:'srem',cpp.Absyn.Eadd:'add',cpp.Absyn.Esub:'sub'},
            cpp.Absyn.Typedouble: {cpp.Absyn.Emul:'fmul',cpp.Absyn.Ediv:'fdiv',cpp.Absyn.Emod:'frem',cpp.Absyn.Eadd:'fadd',cpp.Absyn.Esub:'fsub'},
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


        #/TODO emit params as well
        params=''
        
        self.emit("define i%d @%s(%s) {" % (self.module.get_size(f.type_),f.cident_,params))
        
        self.emit("entry:")
        self.compile_block(f.liststatement_)
        
        self.emit("}")
        
        
        pass
    
    def get_register_id(self):
        self.register+=1
        return self.register
        
    def get_var_name(self):
        '''Returns a name for a new variable'''
        self.var_name+=1
        return '%%v_%d' % self.var_name
        
    
    def emit(self,instr):
        
        #/TODO just temporary
        print instr
    
    def compile_block(self,statements,new_context=True):
        '''
        Nop.                Statement           ::= ";"; --Allow empty instruction
        Block.              Statement           ::= "{" [Statement] "}";
        While.              Statement           ::= "while" "(" Expr ")" Statement;
        DoWhile.            Statement           ::= "do" Statement "while" "(" Expr ")" ";"; --My own addition to the language
        IfElse.             Statement           ::= "if" "(" Expr ")" Statement "else" Statement;
        If.                 Statement           ::= "if" "(" Expr ")" Statement;'''
        if new_context:
            self.var_contx.push()
        
        for i in statements:
            if isinstance(i,cpp.Absyn.Expression):
                self.compile_expr(i.expr_)
            elif isinstance(i,cpp.Absyn.VoidReturn):
                self.emit('ret void')
            elif isinstance(i,cpp.Absyn.Return):
                r1=self.compile_expr(i.expr_)
                self.emit('ret i%d %s' % (self.module.get_size( self.inf.getinfer(i.expr_)),r1))
            elif isinstance(i,cpp.Absyn.Block):
                self.compile_block(i.liststatement_)
            elif isinstance(i,cpp.Absyn.LocalVars):
                #VarNA.              VItem               ::= CIdent;
                #VarVA.              VItem               ::= CIdent "=" Expr;
                size=self.module.get_size(i.type_)
                for j in i.listvitem_:
                    var=self.get_var_name()
                    self.var_contx.put(j.cident_,var)
                    self.emit('%s = alloca i%d' % (var,size))
                    
                    if isinstance(j,cpp.Absyn.VarNA):
                        self.emit('store i%d 0, i%d* %s' % (size,size,var))
                    elif isinstance(j,cpp.Absyn.VarVA):
                        r1=self.compile_expr(j.expr_)
                        self.emit('store i%d %s, i%d* %s' % (size,r1,size,var))
                     
        
        if new_context:
            self.var_contx.pop()
        
        pass
    
    def compile_expr(self,expr):
        id_='%%t%d' % self.get_register_id()
        expr_size=self.module.get_size( self.inf.getinfer(expr))
        
        if isinstance(expr,cpp.Absyn.Eint):
            #self.emit('%s = add i%d 0 , %d' % (id_,self.module.get_size( self.inf.getinfer(expr)),expr.integer_))
            return str(expr.integer_)
        #Arithmetic instructions
        elif expr.__class__ in (cpp.Absyn.Emul,cpp.Absyn.Ediv,cpp.Absyn.Emod,cpp.Absyn.Eadd,cpp.Absyn.Esub):
            r1=self.compile_expr(expr.expr_1)
            r2=self.compile_expr(expr.expr_2)
           
            op=self.aritm[self.inf.getinfer(expr).__class__][expr.__class__]
            self.emit('%s = %s i%d %s , %s' % (id_,op,expr_size,r1,r2 ))
        #Variable
        elif isinstance(expr,cpp.Absyn.Eitm):
            var=self.var_contx.get(expr.cident_)
            self.emit('%s = load i%d* %s' % (id_,expr_size,var))
        #Assignment (as expression, not as statement)
        elif isinstance(expr,cpp.Absyn.Eass):
            #Eass.               Expr2               ::= Expr3 "=" Expr2;
            var=self.var_contx.get(expr.expr_1.cident_)
            r1=self.compile_expr(expr.expr_2)
            self.emit('store i%d %s, i%d* %s' % (expr_size,r1,expr_size,var))
            return r1
            
        '''
        Edbl.               Expr16              ::= Double;
        Ebool.              Expr16              ::= Bool;
        Estrng.             Expr16              ::= String;
        Efun.               Expr15              ::= CIdent "(" [Expr] ")";
        Eainc.              Expr14              ::= Expr15 "++";
        Eadec.              Expr14              ::= Expr15 "--";
        Epinc.              Expr13              ::= "++" Expr14;
        Epdec.              Expr13              ::= "--" Expr14;
        ENeg.               Expr12              ::= "-" Expr13 ;
        ENot.               Expr12              ::= "!" Expr13 ;
        Elt.                Expr9               ::= Expr9 "<" Expr10;
        Egt.                Expr9               ::= Expr9 ">" Expr10;
        Eelt.               Expr9               ::= Expr9 "<=" Expr10;
        Eegt.               Expr9               ::= Expr9 ">=" Expr10;
        Eeql.               Expr8               ::= Expr8 "==" Expr9;
        Edif.               Expr8               ::= Expr8 "!=" Expr9;
        Eand.               Expr4               ::= Expr4 "&&" Expr5;
        Eor.                Expr3               ::= Expr3 "||" Expr4;
        '''

        return id_
    
    
    
    
    
    
    
    
    
    
    
    
    