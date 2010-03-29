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

''' if e.integer_ == -1:    #Constants
                self.emit("iconst_m1",1)
            elif e.integer_ in range(-1,6):
                self.emit("iconst_%d" % e.integer_,1)
            elif e.integer_ in range(-129,128):   #Push byte
                self.emit ("bipush %d"%e.integer_,1)
            elif e.integer_ in range(-32769,32768): #Push short
                self.emit("sipush %d" % e.integer_ ,1)
            else:                                   #Push integer
                self.emit("ldc %d" % e.integer_,1)'''