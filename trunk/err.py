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

def error(message,contx,kind="TYPE ERROR"):
    print kind
    print "\tContext:",contx.getname()
    print "\t"+message
    raise Exception(message)
    pass

def printabletype(ty):
    if isinstance(ty,cpp.Absyn.Typeint):
        t="int"
    elif isinstance(ty,cpp.Absyn.Typebool):
        t="bool"
    elif isinstance(ty,cpp.Absyn.Typedouble):
        t="double"
    elif isinstance(ty,cpp.Absyn.Typevoid):
        t="void"
    elif isinstance(ty,cpp.Absyn.Typestrng):
        t="string"
    return t