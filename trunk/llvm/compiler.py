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
VarNA.              VItem               ::= CIdent;
VarVA.              VItem               ::= CIdent "=" Expr;
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
        self.fnct=f
        self.contx=contx
        self.inf=inf
        self.mname=mname
        self.module=module
        
        self.register=-1


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
        
    
    def emit(self,instr):
        
        #/TODO just temporary
        print instr
    
    def compile_block(self,statements):
        '''LocalVars.          Statement           ::= Type [VItem] ";";
        Nop.                Statement           ::= ";"; --Allow empty instruction
        Return.             Statement           ::= "return" Expr ";";
        VoidReturn.         Statement           ::= "return" ";";
        Block.              Statement           ::= "{" [Statement] "}";
        While.              Statement           ::= "while" "(" Expr ")" Statement;
        DoWhile.            Statement           ::= "do" Statement "while" "(" Expr ")" ";"; --My own addition to the language
        Expression.         Statement           ::= Expr ";" ;
        IfElse.             Statement           ::= "if" "(" Expr ")" Statement "else" Statement;
        If.                 Statement           ::= "if" "(" Expr ")" Statement;'''
        for i in statements:
            if isinstance(i,cpp.Absyn.Expression):
                self.compile_expr(i.expr_)
        pass
    
    def compile_expr(self,expr):
        
        if isinstance(expr,cpp.Absyn.Eint):
            id_=self.get_register_id()
            
            self.emit("%%t%d = add i%d 0 , %d" % (id_,self.module.get_size( self.inf.getinfer(expr)),expr.integer_))
            return id_
            
            
        
        '''
        Edbl.               Expr16              ::= Double;
        Ebool.              Expr16              ::= Bool;
        Estrng.             Expr16              ::= String;
        Eitm.               Expr16              ::= CIdent;
        Efun.               Expr15              ::= CIdent "(" [Expr] ")";
        Eainc.              Expr14              ::= Expr15 "++";
        Eadec.              Expr14              ::= Expr15 "--";
        Epinc.              Expr13              ::= "++" Expr14;
        Epdec.              Expr13              ::= "--" Expr14;
        ENeg.               Expr12              ::= "-" Expr13 ;
        ENot.               Expr12              ::= "!" Expr13 ;
        Emul.               Expr11              ::= Expr11 "*" Expr12;
        Ediv.               Expr11              ::= Expr11 "/" Expr12;
        Emod.               Expr11              ::= Expr11 "%" Expr12;
        Eadd.               Expr10              ::= Expr10 "+" Expr11;
        Esub.               Expr10              ::= Expr10 "-" Expr11;
        Elt.                Expr9               ::= Expr9 "<" Expr10;
        Egt.                Expr9               ::= Expr9 ">" Expr10;
        Eelt.               Expr9               ::= Expr9 "<=" Expr10;
        Eegt.               Expr9               ::= Expr9 ">=" Expr10;
        Eeql.               Expr8               ::= Expr8 "==" Expr9;
        Edif.               Expr8               ::= Expr8 "!=" Expr9;
        Eand.               Expr4               ::= Expr4 "&&" Expr5;
        Eor.                Expr3               ::= Expr3 "||" Expr4;
        Eass.               Expr2               ::= Expr3 "=" Expr2;'''

        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    