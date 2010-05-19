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

import cpp

def fold(prog):
    print "suca"
    for i in prog.listdeclaration_:
        print i
        if isinstance(i,cpp.Absyn.Fnct):
            fold_function_declaration(i)


def fold_function_declaration(f):
    print "suca"
    for i in f.liststatement_:
        fold_statement(i)

def fold_statement(s):
    print "suca"
    '''Folds the expressions contained within the statement and 
    does nothing on the statements without expressions'''
    
    #Folds the expression
    if s.__class__ in (cpp.Absyn.Return,cpp.Absyn.While,cpp.Absyn.DoWhile,cpp.Absyn.Expression,cpp.Absyn.IfElse,cpp.Absyn.If,cpp.Absyn.Foreach):
        s.expr_=fold_expression(s.expr_)

    #Recoursive step on the statements
    if s.__class__ in (cpp.Absyn.While,cpp.Absyn.DoWhile,cpp.Absyn.If,cpp.Absyn.Foreach):
        fold_statement(s.statement_)
    elif isinstance(s,cpp.Absyn.Block):
        for i in s.liststatement_:
            fold_statement(i)
    elif isinstance(s,cpp.Absyn.IfElse):
        fold_statement(s.statement_1)
        fold_statement(s.statement_2)
    elif isinstance(s,cpp.Absyn.LocalVars):
        for i in s.listvitem_:
            if isinstance(i,cpp.Absyn.VarVA):
                i.expr_=fold_expression(i.expr_)
    #For.                Statement           ::= "for" "(" InitFor ";" [Expr] ";" [Expr] ")" Statement;

current_module=None
j_modules=None

def rewrite_function_name(f):
    '''Determines the new internal name for a function'''
    
    #main doesn't change
    if f=='main':
        return f
    
    #Search for function in current module
    for i in j_modules[current_module].listdeclaration_:
        if isinstance(i,cpp.Absyn.Fnct) and i.cident_==f:
            return '___ext___%s___%s_' % (current_module,f)
    
    #Search for function in other modules, and mess it up if it is in multiple modules
    found=0
    
    for j in j_modules:
        for i in j_modules[j].listdeclaration_:
            if isinstance(i,cpp.Absyn.Fnct) and i.cident_==f:
                found+=1
                res = '___ext___%s___%s_' % (j,f)
    if found==1:
        return res
    return f #In this way if the function isn't defined, the correct name will be shown in the error
def fold_expression(e):
    binary=(cpp.Absyn.Emul,cpp.Absyn.Ediv,cpp.Absyn.Emod,cpp.Absyn.Eadd,cpp.Absyn.Esub,cpp.Absyn.Elt,cpp.Absyn.Egt,cpp.Absyn.Eelt,cpp.Absyn.Eegt,cpp.Absyn.Eeql,cpp.Absyn.Edif,cpp.Absyn.Eand,cpp.Absyn.Eor,cpp.Absyn.Eass)
    unary=(cpp.Absyn.Eainc,cpp.Absyn.Eadec,cpp.Absyn.Epinc,cpp.Absyn.Epdec,cpp.Absyn.ENeg,cpp.Absyn.ENot,cpp.Absyn.Ederef)
    
    
    if e.__class__ in binary:
        e.expr_1=fold_expression(e.expr_1)
        e.expr_2=fold_expression(e.expr_2)
    elif e.__class__ in unary:
        e.expr_=fold_expression(e.expr_)
    elif isinstance(e,cpp.Absyn.Efun):
        print "OLD F NAME %s"% e.cident_
        e.cident_=rewrite_function_name(e.cident_)
        print "NEW F NAME %s"% e.cident_
        for i in range(len(e.listexpr_)):
            e.listexpr_[i]=fold_expression(e.listexpr_[i])
    
    
    elif isinstance(e,cpp.Absyn.Eaitm) or isinstance(e,cpp.Absyn.Enew):
        for i in range(len(e.listarrsize_)):
            e.listarrsize_[i].expr_=fold_expression(e.listarrsize_[i].expr_)
    #Special cases for arrays and props and new
    
    #'___ext___%s___%s_'
    elif isinstance(e,cpp.Absyn.Eprop):
        if isinstance(e.prs_,cpp.Absyn.PrsNo): #Normal prop, nothing special to do
            e.expr_=fold_expression(e.expr_)
        if isinstance(e.prs_,cpp.Absyn.PrsYes) and isinstance(e.expr_,cpp.Absyn.Eitm): #Call to external module, converting it
            return fold_expression(cpp.Absyn.Efun('___ext___%s___%s_'% (e.expr_.cident_,e.cident_), e.prs_.listexpr_))
    '''Efun.               Expr15              ::= CIdent "(" [Expr] ")";

PrsYes.             Prs                 ::= "(" [Expr] ")";
PrsNo.              Prs                 ::= ;

Eprop.              Expr16              ::= Expr15 "." CIdent Prs;
.             Expr16              ::= Expr15 "->" CIdent;
'''

    #Tries to solve the tree and return the result
    r=solve_expression(e)
    if r!=None:
        return r
    
    return e

rev_rel= {
        cpp.Absyn.Elt:cpp.Absyn.Eegt,
        cpp.Absyn.Egt:cpp.Absyn.Eelt,
        cpp.Absyn.Eelt:cpp.Absyn.Egt,
        cpp.Absyn.Eegt:cpp.Absyn.Elt,
        cpp.Absyn.Eeql:cpp.Absyn.Edif,
        cpp.Absyn.Edif:cpp.Absyn.Eeql
    }

def solve_expression(e):
    
    #Reverting relational operators
    if isinstance(e,cpp.Absyn.ENot) and e.expr_.__class__ in rev_rel:
        return rev_rel[e.expr_.__class__](e.expr_.expr_1,e.expr_.expr_2)
    
    #Removing double NOT
    if isinstance(e,cpp.Absyn.ENot) and isinstance(e.expr_,cpp.Absyn.ENot):
        return e.expr_.expr_
    
    #Boolean
    elif isinstance(e,cpp.Absyn.Eeql) and isinstance(e.expr_1,cpp.Absyn.Ebool) and isinstance(e.expr_2,cpp.Absyn.Ebool):
        if e.expr_1.bool_.__class__ == e.expr_2.bool_.__class__:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance(e,cpp.Absyn.Edif) and isinstance(e.expr_1,cpp.Absyn.Ebool) and isinstance(e.expr_2,cpp.Absyn.Ebool):
        if e.expr_1.bool_.__class__ != e.expr_2.bool_.__class__:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance(e,cpp.Absyn.Eand) and isinstance(e.expr_1,cpp.Absyn.Ebool) and isinstance(e.expr_2,cpp.Absyn.Ebool):
        if isinstance(e.expr_1.bool_,cpp.Absyn.TrueLit) and isinstance(e.expr_2.bool_,cpp.Absyn.TrueLit):
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance(e,cpp.Absyn.Eor) and isinstance(e.expr_1,cpp.Absyn.Ebool) and isinstance(e.expr_2,cpp.Absyn.Ebool):
        if isinstance(e.expr_1.bool_,cpp.Absyn.TrueLit) or isinstance(e.expr_2.bool_,cpp.Absyn.TrueLit):
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance(e,cpp.Absyn.ENot) and isinstance(e.expr_,cpp.Absyn.Ebool):
        if isinstance(e.expr_.bool_,cpp.Absyn.FalseLit):
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    
    #Integer arithmetic
    elif isinstance (e,cpp.Absyn.Emul) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        return cpp.Absyn.Eint(e.expr_1.integer_ * e.expr_2.integer_ )
    elif isinstance (e,cpp.Absyn.Ediv) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        return cpp.Absyn.Eint(e.expr_1.integer_ / e.expr_2.integer_ )
    elif isinstance (e,cpp.Absyn.Emod) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        return cpp.Absyn.Eint(e.expr_1.integer_ % e.expr_2.integer_ )
    elif isinstance (e,cpp.Absyn.Eadd) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        return cpp.Absyn.Eint(e.expr_1.integer_ + e.expr_2.integer_ )
    elif isinstance (e,cpp.Absyn.Esub) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        return cpp.Absyn.Eint(e.expr_1.integer_ - e.expr_2.integer_ )
    elif isinstance (e,cpp.Absyn.ENeg) and isinstance (e.expr_,cpp.Absyn.Eint):
        return cpp.Absyn.Eint(e.expr_.integer_ * -1)
    
    #double arithmetic
    elif isinstance (e,cpp.Absyn.Emul) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        return cpp.Absyn.Edbl(e.expr_1.double_ * e.expr_2.double_ )
    elif isinstance (e,cpp.Absyn.Ediv) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        return cpp.Absyn.Edbl(e.expr_1.double_ / e.expr_2.double_ )
    elif isinstance (e,cpp.Absyn.Eadd) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        return cpp.Absyn.Edbl(e.expr_1.double_ + e.expr_2.double_ )
    elif isinstance (e,cpp.Absyn.Esub) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        return cpp.Absyn.Edbl(e.expr_1.double_ - e.expr_2.double_ )
    elif isinstance (e,cpp.Absyn.ENeg) and isinstance (e.expr_,cpp.Absyn.Edbl):
        return cpp.Absyn.Edbl(e.expr_.double_ * -1)


    #integer relational
    elif isinstance (e,cpp.Absyn.Elt) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        if e.expr_1.integer_ < e.expr_2.integer_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Egt) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        if e.expr_1.integer_ > e.expr_2.integer_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Eelt) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        if e.expr_1.integer_ <= e.expr_2.integer_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Eegt) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        if e.expr_1.integer_ >= e.expr_2.integer_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Eeql) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        if e.expr_1.integer_ == e.expr_2.integer_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Edif) and isinstance (e.expr_1,cpp.Absyn.Eint) and isinstance (e.expr_2,cpp.Absyn.Eint):
        if e.expr_1.integer_ != e.expr_2.integer_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    
    #double relational
    elif isinstance (e,cpp.Absyn.Elt) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        if e.expr_1.double_ < e.expr_2.double_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Egt) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        if e.expr_1.double_ > e.expr_2.double_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Eelt) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        if e.expr_1.double_ <= e.expr_2.double_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Eegt) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        if e.expr_1.double_ >= e.expr_2.double_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Eeql) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        if e.expr_1.double_ == e.expr_2.double_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    elif isinstance (e,cpp.Absyn.Edif) and isinstance (e.expr_1,cpp.Absyn.Edbl) and isinstance (e.expr_2,cpp.Absyn.Edbl):
        if e.expr_1.double_ != e.expr_2.double_:
            return cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        else:
            return cpp.Absyn.Ebool(cpp.Absyn.FalseLit())
    
    return None
