/* Copyright (C) 2010  Salvo "LtWorf" Tomaselli
 *  
 * worfcc
 * worfcc is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * 
 * author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>
*/

import java.util.Scanner;

class runtime {
    /**
    Class with support methods, considered as builtins by worfcc
    */
    public static Scanner in = new Scanner(System.in);  


    public static void printInt(int a) {
        System.out.println(a);
    }

    public static void printDouble(double a) {
        System.out.println(a);
    }

    public static void printString(String a) {
        System.out.println(a);
    }

    public static int readInt() {
	return in.nextInt();
    }
    
    public static double readDouble() {
        return in.nextDouble();    
    }
    
    public static void printBool(int a) {
        if (a!=0)
            System.out.println("true");
        else
            System.out.println("false");
    }
}
