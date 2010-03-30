# -*- coding: utf-8 -*-
# Copyright (C) 2010  Salvo "LtWorf" Tomaselli
# 
# Typechecker
# Typechecker is free software: you can redistribute it and/or modify
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

import err

class var_env:
    '''This class is used for the last exercise'''
    
    def __init__(self):
        
        self.contexts=[]
        self.contexts.append(Context(""))
        
        self.c=0
        self.cx=[0,]
        self.maxc=0
        
    def getmax(self):
        return self.maxc+1 #The +1 is for 2 words values
    def get(self,ident):
        for i in range(len(self.contexts)-1,-1,-1):
            try:
                return self.contexts[i].get(ident)
            except:
                pass
    def push(self):
        self.contexts.append(Context(None))
        
        self.cx.append(self.c)
    def pop(self):
        self.contexts.pop()
        self.c=self.cx.pop()
    def put(self,ident,inc=1):
        '''Puts a variable into the context'''
        
        self.contexts[len(self.contexts)-1].put(ident,self.c-1+inc)
        
        #The -1+inc is required to assign c if a variable is 1 word and to assign c+1 if the variable is two words
        self.c=self.c+inc
        if self.c>self.maxc:
            self.maxc=self.c

class GeneralContext:
    '''This class is the general context
    It contains a stack of local contexts'''
    def __init__(self,name):
        '''Inits an empty context'''
        self.contexts=[]
        self.contexts.append(Context(name))
    def update(self,ident,val):
        '''Sets the value for a variable.
        Searches for the var in the newest context 1st'''
        for i in range(len(self.contexts)-1,-1,-1):
            if ident in self.contexts[i].table:
                self.contexts[i].table[ident]=val
                return
    def put (self,ident,obj):
        '''Puts an identifier in the top context (if it is not already declared in that context)'''
        if not self.isInLastContext(ident):
            self.contexts[len(self.contexts)-1].put(ident,obj)
        else:
            err.error(ident+" is already defined in this context",self)
    def get(self,ident):
        '''Gets an identifier from a context, exploring from the top to the bottom'''
        for i in range(len(self.contexts)-1,-1,-1):
            try:
                return self.contexts[i].get(ident)
            except:
                pass
        err.error(ident+ " is undefined",self)
    def getname(self):
        '''Returns the name of the actual context'''
        return self.contexts[len(self.contexts)-1].name
    def push(self,name=None,cntx=None):
        '''Pushes an empty context on the top of the stack.
        The name will be inherited if not overridden'''
        if name==None:
            name=self.contexts[len(self.contexts)-1].name
        if cntx==None:
            cntx=Context(name)
        self.contexts.append(cntx)
    def pop(self):
        '''Removes a context from the top of the stack'''
        return self.contexts.pop()
    def isInLastContext(self,ident):
        '''True if an identifier already exists in the top context'''
        return ident in self.contexts[len(self.contexts)-1].table
class Context:
    def __init__(self,name):
        self.table={}
        self.name=name
    def put(self,ident,obj):
        self.table[ident]=obj
    def get(self,ident):
        return self.table[ident]