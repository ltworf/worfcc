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

import sys
import getopt
import typechecker
import compiler
import options
import os

version="0.1"

def printversion():
    print "\tworfcc"
    print "Version: %s" % version
    sys.exit(0)

def printhelp(code=0):
    print "\tworfcc"
    print
    print "Usage: %s [options] [files]" % sys.argv[0]
    print 
    print "  -v            Print version and exits"
    print "  -h            Print this help and exits"
    print "  -t            Only performs typechecking"
    print "  -O            Optimization level"

    sys.exit(code)

def chkf(files):
    for i in files:
        typechecker.checkfile(i)
        print "OK: %s"%i

if __name__ == "__main__":
    s,files=getopt.getopt(sys.argv[1:],"O:vht")
    
    for i in s:
        if i[0] == '-t':
            chkf(files)
            sys.exit(0)
        elif i[0]== '-h':
            printhelp()
        elif i[0]== '-v':
            printversion()
        elif i[0]== '-O':
            options.improvementLevel=int(i[1])

    #Compile the files
    
    rfiles=[]
    for i in files:
        print "Generating assembly for %s"%i
        rfiles.append(compiler.ijvm_compile(i))
    
    print "Compiling class files"
    print "java -jar jasmin.jar %s" % ' '.join(rfiles)
    os.system("java -jar jasmin.jar %s" % ' '.join(rfiles))
