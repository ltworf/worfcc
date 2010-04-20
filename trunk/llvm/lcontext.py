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

class v_context:
    '''This class is the context for the variables in the llvm target
    '''
    def __init__(self):
        '''Inits an empty context, a first context must be pushed or
        it will not work'''
        self.contexts=[]
        
        
    def put (self,ident,obj):
        '''Puts an identifier in the top context (if it is not already declared in that context)'''
        self.contexts[len(self.contexts)-1].put(ident,obj)
    def get(self,ident):
        '''Gets an identifier from a context, exploring from the top to the bottom'''
        for i in range(len(self.contexts)-1,-1,-1):
            try:
                return self.contexts[i].get(ident)
            except:
                pass
        raise Exception('Unable to get desired %s'%ident)

    def push(self):
        '''Pushes an empty context on the top of the stack.'''
        self.contexts.append(cntx())
    def pop(self):
        '''Removes a context from the top of the stack'''
        return self.contexts.pop()
    def isInLastContext(self,ident):
        '''True if an identifier already exists in the top context'''
        return ident in self.contexts[len(self.contexts)-1].table

class cntx:
    def __init__(self):
        self.table={}
    def put(self,ident,obj):
        self.table[ident]=obj
    def get(self,ident):
        return self.table[ident]