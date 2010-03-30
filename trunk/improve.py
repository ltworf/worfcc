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

import options

jumps=("if_icmpgt","if_icmplt","if_icmple","if_icmpge","if_icmpeq","if_icmpne","ifgt","iflt","ifle","ifge","ifeq","ifne","goto")

def reduce_instruction(i):
    '''This function reduces instructions into the smaller version
    iload 0 -> iload_0
    ldc 0 -> iconst_0
    and so on...'''
    s=i.split(' ')
    if s[0]=='ldc' and s[1].isdigit(): #Integer constant
        
        val=int(s[1])
        
        if val == -1:    #Constants
            return 'iconst_m1'
        elif val in range(-1,6):
            return 'iconst_%d' % val
        elif val in range(-129,128):   #Push byte
            return 'bipush %d' % val
        elif val in range(-32769,32768): #Push short
            return 'sipush %d' % val
    
    if s[0]=='ldc2_w': #Double constant
        val=float(s[1])
        if val==0:
            return 'dconst_0'
        elif val==1:
            return 'dconst_1'
    
    if s[0]=='istore':
        val=int(s[1])
        if val in range(0,4):
            return 'istore_%d' % val
    if s[0]=='iload':
        val=int(s[1])
        if val in range(0,4):
            return 'iload_%d' % val    
    if s[0]=='dstore':
        val=int(s[1])
        if val in range(0,4):
            return 'dstore_%d' % val
    if s[0]=='dload':
        val=int(s[1])
        if val in range(0,4):
            return 'dload_%d' % val      
    return i    

class codeblock:
    '''
    This class represents a block of code without jumps.
    Self initializes itself, it is enough to give to the 
    constructor the list of the assembly statements.
    
    It assumes that all the labels are there for a reason:
        there is one and only one branch pointing to them.
    '''
    
    def __init__(self,statements,labeled={},prev=None):
        '''Statements is a list of statements.
        labeled is used internally, leave the default value.
        
        Beware that the list of statements will be discarded
        during the processing'''
        
        self.statements=[]
        
        self.next=None #Pointer of the next block
        self.jump=None #Label of the destination block
        
        #Pointers to blocks eventually executed before this one
        self.prevjump=None
        self.prev=prev
        
        self.labeled=labeled
        
        first=True
        
        while len(statements)>0:
            i=reduce_instruction(statements.pop(0))
            
            s=i.split(' ')
            if s[0] in jumps:
                self.jump=s[1]
                if (s[1],1) in labeled:
                    labeled[(s[1],1)].prevjump=self
                labeled[(s[1],1)]=self
                self.next=codeblock(statements,labeled,self)
            
            elif i.endswith(':'):#It is a label
                if first:#Naming the block
                    labeled[(i[:-1],0)]=self
                    
                    if (i[:-1],1) in labeled:
                        self.prevjump=labeled[(i[:-1],1)]
                    else:
                        labeled[(i[:-1],1)]=self
                else:
                    #Putting the label back to its place
                    statements.insert(0,i)
                    self.next=codeblock(statements,labeled,self)
                    return
            
            self.statements.append(i)
            
            first=False
        #print self.statements
    def getPrev(self):
        '''Pointer to the previous block'''
        return self.prev
    def getPrevJump(self):
        '''Pointer to the block that jumps to this block'''
        return self.prevjump
    def getStatements(self):
        '''Returns the pointer to the list of the statements'''
        return self.statements
    def getNext(self):
        '''Returns the next code block'''
        return self.next
    def getJump(self):
        '''Returns the pointer to the jump code block'''
        if self.jump==None:
            return None
        else:
            return self.labeled[(self.jump,0)]
    def getProgramStatements(self):
        l=list(self.statements)
        if self.next!=None:
            l+=self.next.getProgramStatements()
        return l
    def __str__(self):
        r='\n'.join(self.statements)
        if self.next!=None:
            r+='\n' + self.next.__str__()
        return r
    
def removereturns(block):
    '''This removes the returns from an if-else that returns in each case
    and replaces them with a single return after the end of the if-else structure'''
    
    prev=block.getPrev()
    next=block.getNext()
    prevj=block.getPrevJump()
    
    if prev!=None and prevj!=None:
        for r in ('ireturn','dreturn','return'):
            if r in prev.statements and r in prevj.statements:
                prev.statements.remove(r)
                prevj.statements.remove(r)
                
                if block.statements[0].endswith(':'):
                    block.statements.insert(1,r)
                else:
                    block.statements.insert(0,r)
                
                break
    
    if next!=None:
        removereturns(next)

def remove_dup_pop(code):
    '''This function removes things like
    dup
    istore 0
    pop
    
    and same for the double version
    '''
    i=0
    m=len(code)
    while i <m:
        try:
            code[i+1].index('store')
            is_store=True
        except:
            is_store=False
        
        if code[i] in ('dup','dup2') and i+2<len(code) and code[i+2] in ('pop','pop2') and is_store:
            code.pop(i+2)
            code.pop(i)
            m-=2
        else:
            i+=1

def improve(code):
    '''Returns an improved version of the code'''
    
    o=options.improvementLevel
    if o<1:
        print "Warning, some optimizations are required for a proper compilation"
        return code
    
    if o>1:
        remove_dup_pop(code)
    
    #Improvements on the blocks
    #This will also convert the instructions into their shorter version
    block=codeblock(code)
    
    removereturns(block)
    
    return block.getProgramStatements() 
