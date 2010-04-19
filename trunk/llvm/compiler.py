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
LocalVars.          Statement           ::= Type [VItem] ";";
Nop.                Statement           ::= ";"; --Allow empty instruction
Return.             Statement           ::= "return" Expr ";";
VoidReturn.         Statement           ::= "return" ";";
Block.              Statement           ::= "{" [Statement] "}";
While.              Statement           ::= "while" "(" Expr ")" Statement;
DoWhile.            Statement           ::= "do" Statement "while" "(" Expr ")" ";"; --My own addition to the language
Expression.         Statement           ::= Expr ";" ;
IfElse.             Statement           ::= "if" "(" Expr ")" Statement "else" Statement;
If.                 Statement           ::= "if" "(" Expr ")" Statement;
[].                 [Expr]              ::= ;
(:[]).              [Expr]              ::= Expr;
(:).                [Expr]              ::= Expr "," [Expr];
Eint.               Expr16              ::= Integer;
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
Eass.               Expr2               ::= Expr3 "=" Expr2;
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
    print "lalal"
    '''Compiles the program into LLVM assembly'''
    prog,contx,inf=typechecker.checkfile(filename)
    
    #Gets the name of the module
    cname='.'.join(os.path.basename(filename).split('.')[:-1])
    
    
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
        self.prog=prog
        self.contx=contx
        self.inf=inf
        self.mname=mname
        
        for i in prog.listdeclaration_:
            c=function(i,contx,inf,mname)
        pass
    
    def addConstant(self):
        pass
    
    
    
class function():
    def __init__(self,f,contx,inf,mname):
        print "Generating function "+ f.cident_
        pass