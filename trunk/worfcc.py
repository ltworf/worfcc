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
    print "  -a            Only generates the jasmin assembly"
    print "  -h            Print this help and exits"
    print "  -r            Runs the compiled files after compiling"
    print "  -t            Only performs typechecking"
    print "  -v            Print version and exits"
    print "  -O            Optimization level"

    sys.exit(code)

def chkf(files):
    for i in files:
        typechecker.checkfile(i)
        print "OK: %s"%i

if __name__ == "__main__":
    assembly_only=False
    run_after=False
    
    s,files=getopt.getopt(sys.argv[1:],"aO:vhtr")
    
    log=file("compile.log","a")
    
    log.write("Execution \n")
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
        elif i[0]== '-a':
            assembly_only=True
        elif i[0]== '-r':
            run_after=True
    #Compile the files
    
    rfiles=[]
    for i in files:
        if not os.path.exists(i):
            print >> sys.stderr, "Unable to find file %s" %i
            sys.exit(1)
        #print "Generating assembly for %s"%i
        log.write("Generating assembly for %s\n"%i)
        rfiles.append(compiler.ijvm_compile(i))
    log.close()
    
    if assembly_only:
        sys.exit(0)
    #print "Compiling class files"
    
    for r in rfiles:
        #print "java -jar jasmin.jar -d %s %s" % (os.path.dirname(r),r)
        os.system("java -jar jasmin.jar -d %s %s" % (os.path.dirname(r),r))
    
    if run_after:
        cdir=os.path.realpath(os.path.curdir+"/lib")
        for i in files:
            
            os.chdir(os.path.dirname(i))
            nn=os.path.basename(i)
            
            #print os.path.dirname(i)
            #print "java -cp .:%s %s" % (cdir,nn[:nn.rindex('.')])
            os.system("java -cp .:%s %s" % (cdir,nn[:nn.rindex('.')]))
        