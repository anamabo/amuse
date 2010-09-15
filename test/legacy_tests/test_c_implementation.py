from amuse.support.legacy.core import *

from amuse.support.data import core
from amuse.support.units import nbody_system
from amuse.support.units import units
from amuse.support.legacy import channel

from amuse.support.interface import CodeInterface

from amuse.test.amusetest import TestWithMPI
from amuse.support.legacy import create_c
from amuse.support import exceptions

import subprocess
import os

codestring = """

int echo_int(int int_in, int * int_out) {
    *int_out = int_in;
    if(int_in < 0) {
        return -1;
    } else {
        return 0;
    }
}

int echo_double(double in, double * out) {
    *out = in;
    return 0;
}

int echo_float(float in, float * out) {
    *out = in;
    return 0;
}
int echo_string(char * in, char ** out) {
    *out = in;
    return 0;
}

int echo_strings(char ** inout1, char ** inout2) {
    char * tmp;
    tmp = *inout1;
    *inout1 = *inout2;
    *inout2 = tmp;
    
    return 0;
}

void echo_array(int * in, int * out, int len) {
    int i = 0;
    for(i = 0; i < len; i++) {
        out[i] = in[i];
    }
}

int echo_array_with_result(int * in, int *out, int len) {
    int i = 0;
    for(i = 0; i < len; i++) {
        out[i] = in[i];
    }
    return -1;
}
        
int echo_2_int(int * int_in1, int * int_in2, int * int_out1, int * int_out2, int len) {
    int i = 0;
    for(i = 0; i < len; i++) {
        int_out1[i] = int_in1[i];
        int_out2[i] = int_in2[i];
    }
    
    return len;
}
int echo_3_int(int * i, int * j, int * k, int * l, int * m, int * int_out, int len) {
    int x = 0;
    for(x = 0; x < len; x++) {
        int_out[x] = i;
    }    
    return len;
}
"""

class ForTestingInterface(LegacyInterface):
    
    def __init__(self, exefile):
        LegacyInterface.__init__(self, exefile)

    @legacy_function
    def echo_int():
        function = LegacyFunctionSpecification()
        function.addParameter('int_in', dtype='int32', direction=function.IN)
        function.addParameter('int_out', dtype='int32', direction=function.OUT)
        function.result_type = 'int32'
        function.can_handle_array = True
        return function     
        
    @legacy_function
    def echo_double():
        function = LegacyFunctionSpecification()  
        function.addParameter('double_in', dtype='float64', direction=function.IN)
        function.addParameter('double_out', dtype='float64', direction=function.OUT)
        function.result_type = 'int32'
        function.can_handle_array = True
        return function  
        
    @legacy_function
    def echo_float():
        function = LegacyFunctionSpecification()  
        function.addParameter('float_in', dtype='float32', direction=function.IN)
        function.addParameter('float_out', dtype='float32', direction=function.OUT)
        function.result_type = 'int32'
        function.can_handle_array = True
        return function  
          
    @legacy_function
    def echo_string():
        function = LegacyFunctionSpecification()  
        function.addParameter('string_in', dtype='string', direction=function.IN)
        function.addParameter('string_out', dtype='string', direction=function.OUT)
        function.result_type = 'int32'
        function.can_handle_array = True
        return function  
          
    @legacy_function
    def echo_strings():
        function = LegacyFunctionSpecification()  
        function.addParameter('string_inout1', dtype='string', direction=function.INOUT)
        function.addParameter('string_inout2', dtype='string', direction=function.INOUT)
        function.result_type = 'int32'
        function.can_handle_array = True
        return function  
        
    @legacy_function
    def echo_array():
        function = LegacyFunctionSpecification()  
        function.addParameter('int_in', dtype='int32', direction=function.IN)
        function.addParameter('int_out', dtype='int32', direction=function.OUT)
        function.addParameter('len', dtype='int32', direction=function.LENGTH)
        function.result_type = None
        function.must_handle_array = True
        return function
        
    @legacy_function
    def echo_array_with_result():
        function = LegacyFunctionSpecification()  
        function.addParameter('int_in', dtype='int32', direction=function.IN)
        function.addParameter('int_out', dtype='int32', direction=function.OUT)
        function.addParameter('len', dtype='int32', direction=function.LENGTH)
        function.result_type = 'int32'
        function.must_handle_array = True
        return function    
    
    #@legacy_function
    def return_string():
        function = LegacyFunctionSpecification()  
        function.addParameter('string_in', dtype='string', direction=function.IN)
        function.result_type = 'string'
        function.can_handle_array = True
        return function  
        
    @legacy_function
    def echo_2_int():
        function = LegacyFunctionSpecification()
        function.addParameter('int_in1', dtype='int32', direction=function.IN)
        function.addParameter('int_in2', dtype='int32', direction=function.IN, default = 1)
        function.addParameter('int_out1', dtype='int32', direction=function.OUT)
        function.addParameter('int_out2', dtype='int32', direction=function.OUT)
        function.addParameter('len', dtype='int32', direction=function.LENGTH)
        function.result_type = 'int32'
        function.must_handle_array = True
        return function    
        


    @legacy_function
    def echo_3_int():
        function = LegacyFunctionSpecification()
        function.addParameter('i', dtype='int32', direction=function.IN)
        function.addParameter('j', dtype='int32', direction=function.IN)
        function.addParameter('k', dtype='int32', direction=function.IN)
        function.addParameter('l', dtype='int32', direction=function.IN, default = 0)
        function.addParameter('m', dtype='int32', direction=function.IN, default = 1)
        function.addParameter('int_out', dtype='int32', direction=function.OUT)
        function.addParameter('len', dtype='int32', direction=function.LENGTH)
        function.result_type = 'int32'
        function.must_handle_array = True
        return function
    
    
class ForTesting(CodeInterface):
    
    def __init__(self, exefile, **options):
        CodeInterface.__init__(self, ForTestingInterface(exefile), **options)
    
    def define_methods(self, object):
        object.add_method(
            'echo_int',
            (units.m,)
            ,
            (
                units.m,
                object.ERROR_CODE,
            )
        )



class TestInterface(TestWithMPI):
      
    def c_compile(self, objectname, string):
        root, ext = os.path.splitext(objectname)
        sourcename = root + '.c'
        
        if os.path.exists(objectname):
            os.remove(objectname)
        
        with open(sourcename, "w") as f:
            f.write(string)
            
        process = subprocess.Popen(
            ["mpicc", "-I", "lib/stopcond", "-c",  "-o", objectname, sourcename],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        if not os.path.exists(objectname):
            raise Exception("Could not compile {0}, error = {1}".format(objectname, stderr))
    
    def cxx_compile(self, objectname, string):
        root, ext = os.path.splitext(objectname)
        sourcename = root + '.cc'
        
        with open(sourcename, "w") as f:
            f.write(string)
            
        process = subprocess.Popen(
            ["mpicxx", "-I", "lib/stopcond", "-c",  "-o", objectname, sourcename],
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        
        if not os.path.exists(objectname):
            raise Exception("Could not compile {0}, error = {1}".format(objectname, stderr))
            
    def c_build(self, exename, objectnames):
        arguments = ["mpicxx"]
        arguments.extend(objectnames)
        arguments.append("-o")
        arguments.append(exename)
        
        process = subprocess.Popen(
            arguments,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception("Could not build {0}, error = {1}".format(exename, stderr))
    
    def build_worker(self):
        
        path = os.path.abspath(self.get_path_to_results())
        codefile = os.path.join(path,"code.o")
        interfacefile = os.path.join(path,"interface.o")
        self.exefile = os.path.join(path,"c_worker")
        
        self.c_compile(codefile, codestring)
        
        uc = create_c.MakeACHeaderStringOfAClassWithLegacyFunctions()
        uc.class_with_legacy_functions = ForTestingInterface
        header =  uc.result
        
        
        uc = create_c.MakeACStringOfAClassWithLegacyFunctions()
        uc.class_with_legacy_functions = ForTestingInterface
        code =  uc.result
        
        string = '\n\n'.join([header, code])
        
        #print string
        
        self.cxx_compile(interfacefile, string)
        self.c_build(self.exefile, [interfacefile, codefile] )
    
    def setUp(self):
        super(TestInterface, self).setUp()
        print "building"
        self.build_worker()
        
    def test1(self):
        instance = ForTestingInterface(self.exefile)
        int_out, error = instance.echo_int(10)
        del instance
        self.assertEquals(int_out, 10)
        self.assertEquals(error, 0)
        
    def test2(self):
        instance = ForTestingInterface(self.exefile)
        out, error = instance.echo_double(4.0)
        del instance
        self.assertEquals(out, 4.0)
        self.assertEquals(error, 0)
        
        
    def test3(self):
        instance = ForTestingInterface(self.exefile)
        input = [1,2,3,4]
        output, errors = instance.echo_int(input)
        del instance
        self.assertEquals(len(errors),4)
        for actual, expected in zip(output, input):
            self.assertEquals(actual, expected)
            
    def test4(self):
        instance = ForTestingInterface(self.exefile)
        input = [1.0,2.1,3.3,4.2]
        output, errors = instance.echo_double(input)
        instance.stop()
        self.assertEquals(len(errors),4)
        for actual, expected in zip(output, input):
            self.assertEquals(actual, expected)
            
        
    def test5(self):
        instance = ForTestingInterface(self.exefile)
        out, error = instance.echo_float(4.0)
        del instance
        self.assertEquals(out, 4.0)
        self.assertEquals(error, 0)
        
    def test6(self):
        
        instance = ForTestingInterface(self.exefile)
        out, error = instance.echo_string("abc")
        del instance
        self.assertEquals(error, 0)
        self.assertEquals(out[0], "abc")

    def test7(self):
        instance = ForTestingInterface(self.exefile)
        out, error = instance.echo_string(["abc","def"])
        del instance
        
        self.assertEquals(error[0], 0)
        self.assertEquals(error[1], 0)
        self.assertEquals(out[0], "abc")
        self.assertEquals(out[1], "def")

    def test8(self):
        instance = ForTestingInterface(self.exefile)
        out1, out2, error = instance.echo_strings("abc","def")
        del instance
        
        self.assertEquals(error, 0)
        self.assertEquals(out1[0], "def")
        self.assertEquals(out2[0], "abc")
      
    def test9(self):
        instance = ForTestingInterface(self.exefile)
        str1_out, str2_out, error = instance.echo_strings(["abc", "def"], ["ghi", "jkl"])
        del instance
        
        self.assertEquals(error[0], 0)
        self.assertEquals(error[1], 0)
        self.assertEquals(str1_out[0], "ghi")
        self.assertEquals(str1_out[1], "jkl")
        self.assertEquals(str2_out[0], "abc")
        self.assertEquals(str2_out[1], "def")
      
    def xtest10(self):
        """test for ticket #74, 'running out of os file descriptors'
        
        
        Note: this test takes a very long time, to enable it
        remove the 'X' infront of the test name, to disable it
        add an 'X'.
        Also note: to test this, you best set the ulimit
        to a low number (but not too low), for example
        ulimit -n 400
        """
        for x in range(400):
            instance = ForTestingInterface(self.exefile)
            out, error = instance.echo_float(4.0)
            if x % 100 == 0:
                print "x:", x
            instance.stop()

    
    def test11(self):
        instance = ForTestingInterface(self.exefile)
        (output_ints,) = instance.echo_array([4,5,6])
        instance.stop()
        print output_ints
        self.assertEquals(output_ints[0], 4)
        self.assertEquals(output_ints[1], 5)
        self.assertEquals(output_ints[2], 6)
        
    def test12(self):
        instance = ForTestingInterface(self.exefile)
        (output_ints, error) = instance.echo_array_with_result([4,5,6])
        instance.stop()
        self.assertEquals(output_ints[0], 4)
        self.assertEquals(output_ints[1], 5)
        self.assertEquals(output_ints[2], 6)
        
        self.assertEquals(error[0], -1)
        self.assertEquals(error[1], -1)
        self.assertEquals(error[2], -1)

    def test13(self):
        instance = ForTesting(self.exefile)
        self.assertRaises(exceptions.AmuseException, instance.echo_int, [-1, -2]| units.m, 
            expected_message = "Error when calling 'echo_int' of a 'ForTesting', errorcode is -1")
        instance.stop()

    def test14(self):
        instance = ForTesting(self.exefile)
        self.assertRaises(exceptions.LegacyException, lambda : instance.echo_int())
        instance.legacy_interface.echo_int.specification.id = -9
        self.assertRaises(exceptions.LegacyException, lambda : instance.echo_int(1 | units.m))
        instance.stop()
    
    

    def test15(self):
        instance = ForTesting(self.exefile)
        output_ints1, output_ints2, result = instance.echo_2_int([1,2],[3,4])
        output_ints3, output_ints4, result = instance.echo_2_int([1,2,3])
        output_ints5, output_ints6, result = instance.echo_2_int([5],[0])
        output_ints7, output_ints8, result = instance.echo_2_int([5])
        instance.stop()
        self.assertEquals(output_ints1[1], 2)
        self.assertEquals(output_ints2[0], 3)
        self.assertEquals(output_ints2[1], 4)
        for i in range(3):
            self.assertEquals(output_ints3[i], i + 1)
            self.assertEquals(output_ints4[i], 1)
        self.assertEquals(output_ints5[0], 5)
        self.assertEquals(output_ints6[0], 0)
        self.assertEquals(output_ints7[0], 5)
        self.assertEquals(output_ints8[0], 1)
    
    

    def test16(self):
        instance = ForTesting(self.exefile)
        
        #self.assertRaises(exceptions.AmuseException, lambda : instance.echo_int([]))
        instance.stop()
    
    
