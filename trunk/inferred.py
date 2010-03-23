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

class inferred():
    '''Keeps track of the result type of an expression'''
    
    def __init__(self):
        self.dic={}
    def __str__(self):
        return self.dic.__str__()
    def putinfer(self,key,value):
        '''Returns value itself so can be used in return statements directly'''
        self.dic[key]=value
        return value
    def getinfer(self,key):
        return self.dic[key]