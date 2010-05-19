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


import java.io             
import cpp          #Importing the cpp classes
import context      #Package that provides the stack of contexts
import sys
import java_cup
import err
import inferred
import options

builtins=("printInt","printDouble","printString","readInt","readDouble") #"printBool"

def checkfile(filename):
    '''Typechecking for a file
    filename            file to typecheck
    
    This function does not return in case of failure'''
    t_inf=inferred.inferred()
    gcont=context.GeneralContext("Declaration")      #Initializing the general context, will automatically have an empty context
    builtin(gcont)  #Adds built-in definitions
    try:
        lexer =  cpp.Yylex(java.io.FileReader(filename));
        parser=cpp.parser(lexer)
        res=parser.parse()
        prog=res.value
    except:
        print >> sys.stderr,"ERROR\nSYNTAX ERROR"
        print >> sys.stderr,"At line ",lexer.line_num()
        print >> sys.stderr,"near ", lexer.buff()
        raise Exception("SYNTAX ERROR")
    
    #Performs constant folding
    if options.improvementLevel>1:
        import cfold
        cfold.fold(prog)
    
    #Adding all the functions to the context, because their definition doesn't have to be before their 1st call
    for i in prog.listdeclaration_:
        if isinstance(i,cpp.Absyn.Fnct)or isinstance(i,cpp.Absyn.Strct):
            gcont.put(i.cident_,i)
        elif isinstance(i,cpp.Absyn.Typedef):
            gcont.put(i.cident_2,i)


    #Typechecking the functions
    for i in prog.listdeclaration_:
        if isinstance(i,cpp.Absyn.Fnct):
            check_fnct(i,gcont,t_inf)
    
    #Special check for the main function
    main=gcont.get("main")
    if len(main.listargument_)!=0 or (not isinstance( main.type_,cpp.Absyn.Typeint)) :
        err.error("Main function must be:\nint main();",gcont)
    
    #Will return the tree and the context containing only the functions
    return (prog,gcont,t_inf)

def check_fnct(f,contx,t_inf):
    '''Checks a function
    f               function
    contx           context
    
    This function will add the arguments to a new context and call chk_block with the same context.
    
    A return statement is mandatory for non-void functions.
    '''
    contx.push(f.cident_)    #Adding a new context for the function
    
    #Adding the arguments to the current context
    for i in f.listargument_:
        contx.put(i.cident_,i.type_)

    ret=chk_block(f.liststatement_,contx,False,f.type_,t_inf) #Checking the statements in a block that has the same context
    
    
    if not isinstance(f.type_,cpp.Absyn.Typevoid) and not ret: #Raise exception for missing return statement
        err.error("Missing return statement in non void function "+f.cident_,contx)
    elif isinstance(f.type_,cpp.Absyn.Typevoid): #Adds a return in the end of every
        f.liststatement_.addLast(cpp.Absyn.VoidReturn())
    
    contx.pop()     #Removing the context

def check_const_expr(i,t_inf,contx):
    #Check if the condition is a boolean literal.. bah
    if isinstance(i.expr_,cpp.Absyn.Ebool):
        if options.warningLevel>1:
            print "WARNING: using constants in condition is a very poor way of programming"
        if isinstance (i.expr_.bool_,cpp.Absyn.TrueLit):
            t_inf.putinfer(i.expr_,True)
        else:
            t_inf.putinfer(i.expr_,False)
        return cpp.Absyn.Typebool()
    else:
        return infer(i.expr_,contx,t_inf)

def for_each_to_while(s):
    '''Converts a foreach cycle into a while cycle'''
    b1=cpp.Absyn.ListStatement() #Block
    b2=cpp.Absyn.ListStatement() #While body
    
    ind_name='__index__%s' % s.__str__() #Indexvar name
    
    #Iter variable
    t1=cpp.Absyn.VarNA(s.cident_)
    t2=cpp.Absyn.ListVItem()
    t2.add(t1)
    t3=cpp.Absyn.LocalVars(s.type_,t2)
    b1.add(t3)
    
    #index variable
    t1=cpp.Absyn.VarNA(ind_name)
    t2=cpp.Absyn.ListVItem()
    t2.add(t1)
    t3=cpp.Absyn.LocalVars(cpp.Absyn.Typeint(),t2)
    b1.add(t3)
    
    #Creating while condition
    #index<a.length
    e_index=cpp.Absyn.Eitm(ind_name) #Expression with index name
    a_prop=cpp.Absyn.Eprop(s.expr_,'length') #array.length
    expr= cpp.Absyn.Elt(e_index,a_prop)
    
    #Creating while body
    # i=a[__index__];__index__++
    
    if isinstance(s.expr_,cpp.Absyn.Eitm):
        t2=cpp.Absyn.ArrSize(e_index)
        t3=cpp.Absyn.ListArrSize()
        t3.add(t2)
        t4=cpp.Absyn.Eaitm(s.expr_.cident_,t3)
    elif isinstance(s.expr_,cpp.Absyn.Eaitm):
        s.expr_.listarrsize_.add(e_index)
        t4=s.expr_
    
    t5=cpp.Absyn.Eitm(s.cident_)
    t6=cpp.Absyn.Eass(t5,t4)
    
    b2.add(cpp.Absyn.Expression(t6))
    
    t1=cpp.Absyn.Epinc(e_index) #__index__++
    b2.add(cpp.Absyn.Expression(t1))
    
    b2.add(s.statement_)
    
    #Creating the while cycle
    w=cpp.Absyn.While(expr,cpp.Absyn.Block(b2))
    b1.add(w)
    
    return cpp.Absyn.Block(b1)
    
def for_to_while(s):
    '''Converts a for loop into a while loop'''
    
    #List for 1st level block
    b1=cpp.Absyn.ListStatement()
    b2=cpp.Absyn.ListStatement()
    
    
    #Adds the initialization
    if isinstance(s.initfor_,cpp.Absyn.ForExpr):
        for i in s.initfor_.listexpr_:
            b1.add(cpp.Absyn.Expression(i))
    elif isinstance(s.initfor_,cpp.Absyn.ForDecl):
        b1.add(cpp.Absyn.LocalVars(s.initfor_.type_,s.initfor_.listvitem_))
    
    if len(s.listexpr_1)>0:
        #Expr of 2nd expression
        for i in range(len(s.listexpr_1)-1):
            b1.add(cpp.Absyn.Expression(s.listexpr_1[i]))
        #The last expr is the condition
        e=s.listexpr_1[len(s.listexpr_1)-1]
    else: #No condition expression
        e=cpp.Absyn.Ebool(cpp.Absyn.TrueLit())
        
    #While cycle
    b1.add(cpp.Absyn.While(e,cpp.Absyn.Block(b2)))
    
    #Statements
    b2.add(s.statement_)
    
    #Expr3
    for i in s.listexpr_2:
        b2.add(cpp.Absyn.Expression(i))
    
    #Expr2 again
    if len(s.listexpr_1)>1:
        for i in range(len(s.listexpr_1)-1):
            b2.add(cpp.Absyn.Expression(s.listexpr_1[i]))
    
    #Return the block
    return cpp.Absyn.Block(b1)
    

def chk_block(statements,contx,new_contx,return_,t_inf):
    '''Checks a block. A block can be a function.
    statements          list of the statements in the block (order is important)
    contx               context
    new_contx           tells if a new contexthas to be created (inner block) or the same has to be used
    return_             tells the return type that is expected by the function
    
    It will return a boolean value saying if the block has a return statement or not.
    An if statement having a return statement in both if and else branches is considered to have a return statement, otherwise not.
    
    It is not allowed to have statements after a return statement (unreacheable ccode)
    '''
    has_return=False
    if new_contx:
        contx.push()
    
    #Checking the statements
    for index in range(len(statements)):
        i=statements[index] #I use this to know if there are statements after the return
        
        
        #Replaces for/foreach with while
        if isinstance(i,cpp.Absyn.For):
            i=statements[index]=for_to_while(i)
        elif isinstance(i,cpp.Absyn.Foreach):
            i=statements[index]=for_each_to_while(i)

        if isinstance(i,cpp.Absyn.Return):    #Return with value
            has_return=True
            
            inf=infer(i.expr_,contx,t_inf)
            if inf.__class__!=return_.__class__: #Return with value, checking its type
                err.printabletype(return_)
                err.error ("Type mismatch in return, expected "+err.printabletype(return_)+ " got "+ err.printabletype(inf),contx)
        elif isinstance(i,cpp.Absyn.VoidReturn):
            has_return=True
            
            if not isinstance(return_,cpp.Absyn.Typevoid):
                err.error("Must return an expression",contx)
            
        elif isinstance(i,cpp.Absyn.LocalVars):   #Var declaration (multiple vars)
            if isinstance(i.type_,cpp.Absyn.Typevoid):
                err.error("Unable to declare void vars",contx)
            for j in i.listvitem_:
                if isinstance(j,cpp.Absyn.VarNA): #Declaration without assignment
                    contx.put(j.cident_,i.type_)    #Putting the new vars into the context
                else: #Declaration and assignment
                    q=infer(j.expr_,contx,t_inf)
                    
                    if q==i.type_:
                        contx.put(j.cident_,i.type_)
                    else:
                        err.error("Type mismatch in declaration %s, expected %s got %s"% (j.cident_,err.printabletype(i.type_),err.printabletype(q)),contx)
        elif isinstance(i,cpp.Absyn.Block):     #Block
            #Checking the block creating a new context
            has_return=chk_block(i.liststatement_,contx,True,return_,t_inf);
        elif isinstance(i,cpp.Absyn.Expression):    #Expression
            infer(i.expr_,contx,t_inf)
        elif isinstance(i,cpp.Absyn.While) or isinstance(i,cpp.Absyn.DoWhile):    #While/Do-while loop
            inf=check_const_expr(i,t_inf,contx)
            
            if not isinstance(inf,cpp.Absyn.Typebool):
                err.error("Condition in while must be bool, got "+ err.printabletype(inf) + " instead" ,contx)
            #Check while's statement in the same context, as a list of one item.
            # If it is a block, another recoursive call will create the new context
            r=chk_block([i.statement_,],contx,False,return_,t_inf)#Check the instructions
            
            #Do while body is always executed
            if r and isinstance(i,cpp.Absyn.DoWhile):
                has_return=True
                index-=1
            
            if t_inf.getinfer(i.expr_)==True:
                has_return=r
            
        elif isinstance(i,cpp.Absyn.If):#If without else
            inf=check_const_expr(i,t_inf,contx)
                
            if not isinstance(inf,cpp.Absyn.Typebool):
                err.error("Condition in if must be bool, got "+ err.printabletype(inf) + " instead" ,contx)
            r=chk_block([i.statement_,],contx,False,return_,t_inf)#Check the instructions
            
            #Consider as always returning if expression is true
            if t_inf.getinfer(i.expr_)==True:
                q=True
            else:
                q=False
                
            has_return=q and r
                
            
        elif isinstance(i,cpp.Absyn.IfElse):    #if else
            inf=check_const_expr(i,t_inf,contx)
            
            if not isinstance(inf,cpp.Absyn.Typebool):
                err.error("Condition in if must be bool, got "+ err.printabletype(inf) + " instead" ,contx)
            #has_return will be true if both of the branches contains a return
            has_return1=chk_block((i.statement_1,),contx,False,return_,t_inf) #Check the instructions in the if
            has_return2=chk_block((i.statement_2,),contx,False,return_,t_inf)
            
            if t_inf.getinfer(i.expr_)==True:
                has_return=has_return1
            elif t_inf.getinfer(i.expr_)==False:
                has_return=has_return2
            else:
                has_return=has_return1 and has_return2 #Check the instructions in the else

        #Disallow statements after the return
        if has_return and index != len(statements)-1: 
            err.error("Unreachable code after return",contx)
            
    if new_contx:
        contx.pop()
    return has_return

def infer(expr,contx,t_inf):
    '''Returns the type of an expression
    expr        Expression to infer
    contx       context'''
    
    #Literals
    #Null pointer
    if isinstance(expr,cpp.Absyn.Enull):
        return t_inf.putinfer(expr,cpp.Absyn.Typecustom(expr.cident_))
    elif isinstance(expr,cpp.Absyn.Eint):
        return t_inf.putinfer(expr,cpp.Absyn.Typeint())
    elif isinstance(expr,cpp.Absyn.Edbl):
        return t_inf.putinfer(expr,cpp.Absyn.Typedouble())
    elif isinstance(expr,cpp.Absyn.Ebool):
        return t_inf.putinfer(expr,cpp.Absyn.Typebool())
    elif isinstance(expr,cpp.Absyn.Estrng):
        return t_inf.putinfer(expr,cpp.Absyn.Typestrng())
    elif isinstance(expr,cpp.Absyn.Enew):
        q=cpp.Absyn.Typearray(expr.type_)
        q.level_=len(expr.listarrsize_)
        for i in expr.listarrsize_:
            inf=infer(i.expr_,contx,t_inf)
            if not isinstance(inf,cpp.Absyn.Typeint):
                err.error('Array index must be int',contx)
        return t_inf.putinfer(expr,q)
    elif isinstance(expr,cpp.Absyn.Eaitm):
        if isinstance(contx.get(expr.cident_),cpp.Absyn.Typearray):
            p=contx.get(expr.cident_)
            print p.level_,p.type_
            
            #Check index expressions
            for i in expr.listarrsize_:
                inf=infer(i.expr_,contx,t_inf)
                if not isinstance(inf,cpp.Absyn.Typeint):
                    err.error('Array index must be int',contx)
            if p.level_-len(expr.listarrsize_)<0:
                err.error('Wrong number of dimentions in array index',contx)
            elif p.level_-len(expr.listarrsize_)==0:
                return t_inf.putinfer(expr,p.type_)
            else:
                q=cpp.Absyn.Typearray(contx.get(expr.cident_).type_)
                q.level_=contx.get(expr.cident_).level_-1
                return t_inf.putinfer(expr,q)
        else:
            err.error("Can't index non-array items",contx)
        
    elif isinstance(expr,cpp.Absyn.Eprop):
        inf=infer(expr.expr_,contx,t_inf)
        if expr.cident_=='length' and isinstance(inf,cpp.Absyn.Typearray):
            return t_inf.putinfer(expr,cpp.Absyn.Typeint())
        err.error("Unexpected attribute or attribute on non-array",contx)
    #Negation "-a"
    elif isinstance(expr,cpp.Absyn.ENeg):
        inf=infer(expr.expr_,contx,t_inf)
        if isinstance(inf,cpp.Absyn.Typeint) or isinstance(inf,cpp.Absyn.Typedouble):
            return t_inf.putinfer(expr,inf)
        err.error("Expected numeric expression for - operator",contx)
    #Boolean negation "!a"
    elif isinstance(expr,cpp.Absyn.ENot):
        inf=infer(expr.expr_,contx,t_inf)
        if isinstance(inf,cpp.Absyn.Typebool):
            return t_inf.putinfer(expr,inf)
        err.error("Expected boolean expression for ! operator",contx)
    #&& and ||
    elif isinstance(expr,cpp.Absyn.Eand) or isinstance(expr,cpp.Absyn.Eor):
        #if both are bool
        inf1=infer(expr.expr_1,contx,t_inf)
        inf2=infer(expr.expr_2,contx,t_inf)
        if isinstance(inf1,cpp.Absyn.Typebool) and isinstance(inf2,cpp.Absyn.Typebool):
            return t_inf.putinfer(expr,cpp.Absyn.Typebool())
        else:
            err.error("|| and && are boolean operators, got " + err.printabletype(inf1) +"," + err.printabletype(inf2) + " instead",contx)
    #Dereference
    elif isinstance(expr,cpp.Absyn.Ederef):
        inf=infer(expr.expr_,contx,t_inf)
        if not isinstance(inf,cpp.Absyn.Typecustom):
            err.error("Only structured types support dereferencing",contx)
            
        typedef=contx.get(inf.cident_)
        struct=contx.get(typedef.cident_1)
        
        for i in struct.liststrctelm_:
            if i.cident_==expr.cident_: #Found the right field
                return t_inf.putinfer(expr,i.type_)
        err.error("Field %s is not present in the struct %s" % (expr.cident_,struct.cident_),contx)
        #    .           StrctElm            ::= Type CIdent ";";
        #.             Expr16              ::= Expr15 "->" CIdent;
    #Vars
    elif isinstance(expr,cpp.Absyn.Eitm):
        return t_inf.putinfer(expr,contx.get(expr.cident_))
    #-- and ++
    elif isinstance(expr,cpp.Absyn.Eainc) or isinstance(expr,cpp.Absyn.Eadec) or isinstance(expr,cpp.Absyn.Epinc) or isinstance(expr,cpp.Absyn.Epdec):
        inf=infer(expr.expr_,contx,t_inf)
        
        #If the operand is a variable, return its type if it is numeric or raise an error if it is not numeric
        if (isinstance(expr.expr_,cpp.Absyn.Eitm)or isinstance(expr.expr_,cpp.Absyn.Eaitm)) and isinstance(inf,cpp.Absyn.Typeint):
            return t_inf.putinfer(expr,inf)
        else:
            err.error("++ and -- require an int variable",contx)
            
    #== and !=
    elif isinstance(expr,cpp.Absyn.Eeql) or isinstance(expr,cpp.Absyn.Edif):
        type1=infer(expr.expr_1,contx,t_inf)
        type2=infer(expr.expr_2,contx,t_inf)
                
        if type1.__class__ == type2.__class__:
            return t_inf.putinfer(expr,cpp.Absyn.Typebool())
        else:
            err.error("Type mismatch for == or !=, got "+ err.printabletype(type1)+ "," + err.printabletype(type2),contx)
    # %
    elif isinstance(expr,cpp.Absyn.Emod):
        type1=infer(expr.expr_1,contx,t_inf)
        type2=infer(expr.expr_2,contx,t_inf)
        
        #If types are the same and type1 is either double or int
        if type1.__class__==type2.__class__ and isinstance(type1,cpp.Absyn.Typeint):
            return t_inf.putinfer(expr,type1)
        else:
            err.error("Types for %% must match and be int, got "+ err.printabletype(type1)+ "," + err.printabletype(type2),contx)
    #+ - * /
    elif isinstance(expr,cpp.Absyn.Emul) or isinstance(expr,cpp.Absyn.Ediv) or isinstance(expr,cpp.Absyn.Eadd) or isinstance(expr,cpp.Absyn.Esub):
        type1=infer(expr.expr_1,contx,t_inf)
        type2=infer(expr.expr_2,contx,t_inf)
        
        #If types are the same and type1 is either double or int
        if type1.__class__==type2.__class__ and (isinstance(type1,cpp.Absyn.Typedouble) or isinstance(type1,cpp.Absyn.Typeint)):
            return t_inf.putinfer(expr,type1)
        else:
            err.error("Types for + - * / must match and be numeric, got "+ err.printabletype(type1)+ "," + err.printabletype(type2),contx)
    #< > >= <=
    elif isinstance(expr,cpp.Absyn.Elt) or isinstance(expr,cpp.Absyn.Egt) or isinstance(expr,cpp.Absyn.Eegt) or isinstance(expr,cpp.Absyn.Eelt):
        type1=infer(expr.expr_1,contx,t_inf)
        type2=infer(expr.expr_2,contx,t_inf)
                
        #If they have the same class and type1 is either double or int
        if type1.__class__ == type2.__class__ and (isinstance(type1,cpp.Absyn.Typedouble) or isinstance(type1,cpp.Absyn.Typeint)):
            return t_inf.putinfer(expr,cpp.Absyn.Typebool())
        else:
            err.error("Type mismatch for <,>,>=,<=, got "+ err.printabletype(type1)+ "," + err.printabletype(type2),contx)

    #Function call
    elif isinstance(expr,cpp.Absyn.Efun):
        fnct=contx.get(expr.cident_)
        
        if not isinstance(fnct,cpp.Absyn.Fnct):
            err.error(expr.cident_+ " is not a function: can't be invoked",contx)
        
        chk_fnct_call(expr,contx,fnct,t_inf)
        
        #if we are here, no exception was generated
        return t_inf.putinfer(expr,fnct.type_)

    #Assigment
    elif isinstance(expr,cpp.Absyn.Eass):
        if not (isinstance(expr.expr_1,cpp.Absyn.Eitm) or isinstance(expr.expr_1,cpp.Absyn.Eaitm)):
            err.error("Can't assign expression to expression",contx)
        
        inf_1=infer(expr.expr_2,contx,t_inf) #Infer right side expression
        inf_2=infer(expr.expr_1,contx,t_inf) #Infer left side expression
        
        if inf_1==inf_2:
            return t_inf.putinfer(expr,inf_1)
        '''if inf_1.__class__==inf_2.__class__ and isinstance(inf_1,cpp.Absyn.Typearray):
            if (inf_1.type_.__class__==inf_2.type_.__class__ and inf_1.level_==inf_2.level_): #Both are array, checking array type and level
                return t_inf.putinfer(expr,inf_1)
            else:
                err.error("Type mismatch in assignment, expected "+ err.printabletype(inf_2)   +" got " + err.printabletype(inf_1),contx)
        if inf_1.__class__==inf_2.__class__:
            return t_inf.putinfer(expr,inf_1)'''
        err.error("Type mismatch in assignment, expected "+ err.printabletype(inf_2)   +" got " + err.printabletype(inf_1),contx)

def chk_fnct_call(expr,contx,fnct,t_inf):
    '''Checks if a function call has the right number of arguments and that they have the right types
    Does not support overloading, but it would be a nice feature to add
    expr        expression to evaluate (call to a function)
    contx       context
    fnct        function (to know the signature)'''
    if len(fnct.listargument_) != len(expr.listexpr_):
        err.error("Wrong number of arguments, exptected "+str(len(fnct.listargument_))+ " got " + str(len (expr.listexpr_)),contx)
    
    for i in range(len(fnct.listargument_)):
        inf = infer(expr.listexpr_[i],contx,t_inf)
        if inf.__class__ != fnct.listargument_[i].type_.__class__:
            err.error("Type mismatch in function call, expected " + err.printabletype(fnct.listargument_[i].type_) + " got " + err.printabletype(inf),contx)
def builtin(contx):
    '''Adds the builtin definitions for lab3'''
    
    arg=cpp.Absyn.Argument(cpp.Absyn.Typeint(),"x")
    larg=cpp.Absyn.ListArgument()
    larg.add(arg)
    printint=cpp.Absyn.Fnct(cpp.Absyn.Typevoid(),"printInt",larg,None)
    contx.put("printInt",printint)
    
    #arg=cpp.Absyn.Argument(cpp.Absyn.Typebool(),"x")
    #larg=cpp.Absyn.ListArgument()
    #larg.add(arg)
    #printbool=cpp.Absyn.Fnct(cpp.Absyn.Typevoid(),"printBool",larg,None)
    #contx.put("printBool",printbool)

    arg=cpp.Absyn.Argument(cpp.Absyn.Typedouble(),"x")
    larg=cpp.Absyn.ListArgument()
    larg.add(arg)
    printdouble=cpp.Absyn.Fnct(cpp.Absyn.Typevoid(),"printDouble",larg,None)
    contx.put("printDouble",printdouble)
    
    arg=cpp.Absyn.Argument(cpp.Absyn.Typestrng(),"x")
    larg=cpp.Absyn.ListArgument()
    larg.add(arg)
    printdouble=cpp.Absyn.Fnct(cpp.Absyn.Typevoid(),"printString",larg,None)
    contx.put("printString",printdouble)

    larg=cpp.Absyn.ListArgument()
    readint=cpp.Absyn.Fnct(cpp.Absyn.Typeint(),"readInt",larg,None)
    contx.put("readInt",readint)

    larg=cpp.Absyn.ListArgument()
    readdouble=cpp.Absyn.Fnct(cpp.Absyn.Typedouble(),"readDouble",larg,None)
    contx.put("readDouble",readdouble)


if __name__=="__main__":
    for f in range(1,len(sys.argv)):
        try:
            checkfile(sys.argv[f])
            print "OK"
        except Exception , inst:
            print sys.argv[f], "\tFailed"
            print inst