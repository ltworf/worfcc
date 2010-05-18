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
    
    f.write('declare noalias i8* @calloc(i32,i32) nounwind\n')
    
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
    
    def get_byte_size(self,type_):
        if isinstance(type_,cpp.Absyn.Typeint):
            return 4
        elif isinstance(type_,cpp.Absyn.Typebool):
            return 1
        elif isinstance(type_,cpp.Absyn.Typestrng):
            return 'i8*' #//TODO
        elif isinstance(type_,cpp.Absyn.Typedouble):
            return 8
        elif isinstance(type_,cpp.Absyn.Typevoid):
            return 'void' #//TODO
        else: #/TODO REMOVE THIS!!!
            return 'i32*' #//TODO
            
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
        elif isinstance(type_,cpp.Absyn.Typearray):
            if type_.level_<=1: #Can be 0 only to avoid extra code somewhere else, but the result will be ignored
                t=self.get_size(type_.type_)
            else:
                a=cpp.Absyn.Typearray(type_.type_)
                a.level_=type_.level_-1
                t=self.get_size(a)
            return '{i32,[ 0 x %s ]}*' % t
        else: #/TODO REMOVE THIS!!!
            return 'i32*'
    
class function():
    def __init__(self,f,contx,inf,mname,module):
        self.aritm= {# Dictionary to compile operations with integers and doubles
            cpp.Absyn.Typeint: {cpp.Absyn.Emul:'mul',cpp.Absyn.Ediv:'sdiv',cpp.Absyn.Emod:'srem',cpp.Absyn.Eadd:'add',cpp.Absyn.Esub:'sub'},
            cpp.Absyn.Typedouble: {cpp.Absyn.Emul:'fmul',cpp.Absyn.Ediv:'fdiv',cpp.Absyn.Emod:'frem',cpp.Absyn.Eadd:'fadd',cpp.Absyn.Esub:'fsub'},
        }
        
        self.comparisons= {# Dictionary to compile operations with comparisons
            cpp.Absyn.Typebool: {cpp.Absyn.Eeql:'eq',cpp.Absyn.Edif:'ne'},
            cpp.Absyn.Typeint: {cpp.Absyn.Elt :'slt',cpp.Absyn.Egt :'sgt',cpp.Absyn.Eelt:'sle',cpp.Absyn.Eegt:'sge',cpp.Absyn.Eeql:'eq',cpp.Absyn.Edif:'ne'},
            cpp.Absyn.Typedouble: {cpp.Absyn.Elt :'olt',cpp.Absyn.Egt :'ogt',cpp.Absyn.Eelt:'ole',cpp.Absyn.Eegt:'oge',cpp.Absyn.Eeql:'oeq',cpp.Absyn.Edif:'one'},
        }
        
        #Label to jump when meeting a break
        self.breaklabel=None
        
        #Label to jump when meeting a continue
        self.continuelabel=None
        
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
        
        #Puts params to the stack //TODO add code for arrays
        par=0
        for i in f.listargument_:
            var=level_string(self.get_var_name())
            if isinstance(i.type_,cpp.Absyn.Typearray):
                var.level=i.type_.level_
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
        
    def __get_zero__(self,type_,num='0'):
        if isinstance(type_,cpp.Absyn.Typedouble):
            return '%s.0' % num
        return '%s' % num
                            
                            
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
            elif isinstance(i,cpp.Absyn.Break):
                if self.breaklabel!=None:
                    self.emit('br label %%%s' % (self.breaklabel))
                else:
                    raise Exception("break in wrong position")
            elif isinstance(i,cpp.Absyn.Continue):
                if self.continuelabel!=None:
                    self.emit('br label %%%s' % (self.continuelabel))
                else:
                    raise Exception("continue in wrong position")
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
                oldbreaklabel=self.breaklabel
                oldcontinuelabel=self.continuelabel
            
                #Labels
                l_id=self.module.get_lbl()
                lbl_while="while_%d" %l_id
                self.continuelabel=lbl_expr="expr_%d" %l_id
                self.breaklabel=lbl_endwhile="endwhile_%d" %l_id
                
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
                
                #Restoring labels for break and continue
                self.breaklabel=oldbreaklabel
                self.continuelabel=oldcontinuelabel
            elif isinstance(i,cpp.Absyn.LocalVars):
                size=self.module.get_size(i.type_)
                for j in i.listvitem_:
                    var=level_string(self.get_var_name())
                    if isinstance(i.type_,cpp.Absyn.Typearray):
                        var.level=i.type_.level_
                    self.emit('%s = alloca %s' % (var,size))
                    
                    if isinstance(j,cpp.Absyn.VarNA):
                        #Inits the var to 0
                        zero=self.__get_zero__(i.type_)
                            
                        self.emit('store %s %s, %s* %s' % (size,zero,size,var))
                    elif isinstance(j,cpp.Absyn.VarVA):
                        r1=self.compile_expr(j.expr_)
                        self.emit('store %s %s, %s* %s' % (size,r1,size,var))
                    self.var_contx.put(j.cident_,var)
        if new_context:
            self.var_contx.pop()
        
        pass
    
    def compile_array_access(self,expr):
        '''Returns an address containing the reference to the
        array item.'''
        #.              Expr16              ::= CIdent[ArrSize];
        #ArrSize.            ArrSize             ::= "[" Expr "]";
        
        #Create a new instance of Typearray because it's going to be modified
        #So i have to recreate it
        t_a=cpp.Absyn.Typearray(self.inf.getinfer(expr))
        t_a.level_=self.var_contx.get(expr.cident_).level #len(expr.listarrsize_)
        expr_size=self.module.get_size(t_a)
        
        var=self.var_contx.get(expr.cident_)
        
        for i in expr.listarrsize_:
            ide_=self.compile_expr(i.expr_)
            
            id_1='%%t%d' % self.get_register_id()
            id_='%%t%d' % self.get_register_id()
            
            self.emit('%s = load %s* %s' % (id_1,expr_size,var))
            var=id_
            self.emit('%s = getelementptr %s %s, i32 0, i32 1, i32 %s' % (id_,expr_size,id_1,ide_))
            
            #Reduces size for the next iteration
            t_a.level_-=1
            expr_size=self.module.get_size(t_a)
            
        return id_
    
    
    def alloc_array(self,size,a_size,expr_size):
        id_='%%t%d' % self.get_register_id()
        id_2='%%t%d' % self.get_register_id()
        id_3='%%t%d' % self.get_register_id()
        
        self.emit('%s = call noalias i8* @calloc(i32 %s,i32 1) nounwind' % (id_2,size))
        self.emit('%s = bitcast i8* %s to %s' % (id_,id_2,expr_size))
    
        #Save the len
        self.emit('%s = getelementptr %s %s, i32 0, i32 0' %(id_3,expr_size,id_))
        self.emit('store i32 %s, i32* %s\t;stores the size of the array' % (a_size,id_3))
        return id_
    
    def compile_array_size(self,b_size,r1):
        id_1='%%t%d' % self.get_register_id()
        id_2='%%t%d' % self.get_register_id()
        
        self.emit('%s = mul i32 %s, %s\t;Calculate the size of the memory for the array' % (id_1,r1,b_size))
        self.emit('%s = add i32 4,%s\t;Plus 4 bytes for the length' % (id_2,id_1))
        return id_2
    
    def compile_new(self,expr,level,size=None,expr_size=None,r1=None):
        if expr_size==None: expr_size=self.module.get_size( self.inf.getinfer(expr))
        
        #Item size is 4 for pointers and otherwise checks for the type
        b_size= level==1 and self.module.get_byte_size(expr.type_) or 4
        
        if r1==None: r1=self.compile_expr(expr.listarrsize_[level-1].expr_)
        if size==None: size=self.compile_array_size(b_size,r1)

        if level==1:
            return self.alloc_array(size,r1,expr_size)
        else:
            ret= self.alloc_array(size,r1,expr_size)
            
            var_0=self.get_var_name()
            lbl_body='ar_loop_body_%d'%self.module.get_lbl()
            lbl_expr='ar_loop_expr_%d'%self.module.get_lbl()
            lbl_exit='ar_loop_exit_%d'%self.module.get_lbl()
            id_1='%%t%d' % self.get_register_id()
            id_2='%%t%d' % self.get_register_id()
            id_3='%%t%d' % self.get_register_id()
            id_4='%%t%d' % self.get_register_id()
            id_5='%%t%d' % self.get_register_id()
            
            #init var_0 to 0, it is the index of the array
            self.emit ('%s = alloca i32'% (var_0))
            self.emit('store i32 0, i32* %s' % (var_0))
            
            r2=self.compile_expr(expr.listarrsize_[level-1].expr_)
            
            e=self.inf.getinfer(expr)
            e.level_=-1
            expr_size_=self.module.get_size(e)
            
            b_size= level-1==1 and self.module.get_byte_size(expr.type_) or 4
            size_=self.compile_array_size(b_size,r2)
            
            #Cycle
            self.emit('br label %%%s'%lbl_expr) #Jump to evaluate the expr
            
           
            self.emit('%s:'%lbl_body)
            
            #Load index variable
            self.emit('%s = load i32* %s'%(id_1,var_0))
            
            arr_ptr=self.compile_new(expr,level-1,size_,expr_size_,r2)
            e.level_=+1 #Restore the level
            
            
            #ret mem to my array
            #arr_ptr mem to child array
            #id_1 index
            self.emit ('%s = getelementptr %s %s, i32 0, i32 1, i32 %s' % (id_5,expr_size,ret,id_1))
            self.emit ('store %s %s, %s* %s'% (expr_size_,arr_ptr,expr_size_,id_5))
            
            #//TODO store in position
            
            
            #Increases index by 1
            self.emit('%s = add i32 1 , %s' % (id_2,id_1))
            self.emit('store i32 %s, i32* %s' % (id_2,var_0))
            
            self.emit('br label %%%s'%lbl_expr) #Jump to next block
            self.emit('%s:'%lbl_expr)#LOOP expression
            
            self.emit('%s = load i32* %s'%(id_3,var_0)) #Load the index var
            self.emit('%s = icmp slt i32 %s , %s' % (id_4,id_3,r1))
            self.emit('br i1 %s , label %%%s , label %%%s' % (id_4,lbl_body,lbl_exit)) #Jump
            
            self.emit('%s:'%lbl_exit)
            
            return ret
    
    def compile_expr(self,expr,r_reg=False):
        '''
        If reg is set to true, the return will be a tuple of
        (%register_with_result,%var_location)
        it works only if expr is Eitm or Eaitm
        '''
        
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
        #New
        elif isinstance(expr,cpp.Absyn.Enew):
            return self.compile_new(expr,len(expr.listarrsize_))
        #Property
        elif isinstance(expr,cpp.Absyn.Eprop):
            
            #We only have one prop so it's safe to assume it's length
            r1=self.compile_expr(expr.expr_)
            id_2='%%t%d' % self.get_register_id()
            self.emit('%s = getelementptr %s %s, i32 0, i32 0' %(id_2,self.module.get_size( self.inf.getinfer(expr.expr_)) ,r1))
            self.emit('%s = load i32* %s'%(id_,id_2))
            
        #Arithmetic instructions
        elif expr.__class__ in self.aritm[cpp.Absyn.Typeint]:
            r1=self.compile_expr(expr.expr_1)
            r2=self.compile_expr(expr.expr_2)
           
            op=self.aritm[self.inf.getinfer(expr).__class__][expr.__class__]
            self.emit('%s = %s %s %s , %s' % (id_,op,expr_size,r1,r2 ))
        #Negative
        elif isinstance(expr,cpp.Absyn.ENeg):
            r1=self.compile_expr(expr.expr_)
            
            op=self.aritm[self.inf.getinfer(expr).__class__][cpp.Absyn.Emul]
            zero=self.__get_zero__(self.inf.getinfer(expr),1)
            self.emit('%s = %s %s %s , -%s' % (id_,op,expr_size,r1,zero ))
            
        #Comparisons
        elif expr.__class__ in self.comparisons[cpp.Absyn.Typeint]:
            r1=self.compile_expr(expr.expr_1)
            r2=self.compile_expr(expr.expr_2)
            
            op=self.comparisons[self.inf.getinfer(expr.expr_1).__class__][expr.__class__]
            
            if isinstance(self.inf.getinfer(expr.expr_1),cpp.Absyn.Typedouble):
                int_or_float='f'
            else:
                int_or_float='i'
            
            type_=self.module.get_size(self.inf.getinfer(expr.expr_1))
            
            self.emit('%s = %ccmp %s %s %s , %s'%(id_,int_or_float,op,type_,r1,r2))
        #Variable
        elif isinstance(expr,cpp.Absyn.Eitm):
            var=self.var_contx.get(expr.cident_)
            self.emit('%s = load %s* %s' % (id_,expr_size,var))
            if r_reg: return id_,var
        elif isinstance(expr,cpp.Absyn.Eaitm):
            var=self.compile_array_access(expr)
            self.emit('%s = load %s* %s' % (id_,expr_size,var))
            if r_reg: return id_,var
        #Assignment (as expression, not as statement)
        elif isinstance(expr,cpp.Absyn.Eass):
            var=self.var_contx.get(expr.expr_1.cident_)
            r1=self.compile_expr(expr.expr_2)
            
            if isinstance(expr.expr_1,cpp.Absyn.Eitm):
                self.emit('store %s %s, %s* %s' % (expr_size,r1,expr_size,var))
            else:
                id_2=self.compile_array_access(expr.expr_1)
                self.emit('store %s %s, %s* %s' %(expr_size,r1,expr_size,id_2))
            return r1
        #Pre and post increment/decrement
        elif isinstance(expr,cpp.Absyn.Eainc):
            r1,var=self.compile_expr(expr.expr_,True)
            self.emit('%s = add %s 1 , %s' % (id_,expr_size,r1))
            self.emit('store %s %s, %s* %s' % (expr_size,id_,expr_size,var))
            return r1
        elif isinstance(expr,cpp.Absyn.Eadec):
            r1,var=self.compile_expr(expr.expr_,True)
            self.emit('%s = sub %s %s , 1' % (id_,expr_size,r1))
            self.emit('store %s %s, %s* %s' % (expr_size,id_,expr_size,var))
            return r1
        elif isinstance(expr,cpp.Absyn.Epinc):
            r1,var=self.compile_expr(expr.expr_,True)
            self.emit('%s = add %s 1 , %s' % (id_,expr_size,r1))
            self.emit('store %s %s, %s* %s' % (expr_size,id_,expr_size,var))
        elif isinstance(expr,cpp.Absyn.Epdec):
            r1,var=self.compile_expr(expr.expr_,True)
            self.emit('%s = sub %s %s , 1' % (id_,expr_size,r1))
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
            lbl_third='and_third_%d' % l_id
            lbl_end='and_end_%d' % l_id
            
            r1=self.compile_expr(expr.expr_1)
            
            #I need the and to be in a block for the phi instruction
            self.emit('br label %%%s' % (lbl_begin))
            self.emit('%s:' % lbl_begin)
            self.emit('br i1 %s , label %%%s , label %%%s' % (r1,lbl_second,lbl_end) )

            self.emit('%s:' % lbl_second)
            r2=self.compile_expr(expr.expr_2)
            self.emit('br label %%%s' % (lbl_third))
            self.emit('%s:' % lbl_third)
            
            self.emit('br label %%%s' % (lbl_end))
            self.emit('%s:' % lbl_end)
            
            #Assign the value depending on from which block is jumping here
            self.emit('%s = phi %s [ 0 , %%%s ] , [ %s , %%%s ]' % (id_,expr_size,lbl_begin,r2,lbl_third))
        #Short-circuit OR
        elif isinstance(expr,cpp.Absyn.Eor):
            l_id=self.module.get_lbl()
            lbl_begin='or_begin_%d' % l_id
            lbl_second='or_second_%d' % l_id
            lbl_third='or_third_%d' % l_id
            lbl_end='or_end_%d' % l_id
            
            r1=self.compile_expr(expr.expr_1)
            
            #I need the and to be in a block for the phi instruction
            self.emit('br label %%%s' % (lbl_begin))
            self.emit('%s:' % lbl_begin)
            self.emit('br i1 %s , label %%%s , label %%%s' % (r1,lbl_end,lbl_second) )

            self.emit('%s:' % lbl_second)
            r2=self.compile_expr(expr.expr_2)
            self.emit('br label %%%s' % (lbl_third))
            self.emit('%s:' % lbl_third)
            
            self.emit('br label %%%s' % (lbl_end))
            self.emit('%s:' % lbl_end)
            
            #Assign the value depending on from which block is jumping here
            self.emit('%s = phi %s [ 1 , %%%s ] , [ %s , %%%s ]' % (id_,expr_size,lbl_begin,r2,lbl_third))
        #NOT
        elif isinstance(expr,cpp.Absyn.ENot):
            #This will work because the register is 1bit
            r1=self.compile_expr(expr.expr_)
            self.emit('%s = add i1 %s , 1' % (id_,r1))

        return id_
    
    
    
class level_string(str):
    level=0
    