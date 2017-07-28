'''
Put this file in the python2.7/site-packages folder
Place the suitable kernel folder in either /usr/local/share/jupyter/kernels or /usr/share/jupyter/kernels
'''

from ipykernel.ipkernel import IPythonKernel
from IPython.utils import io

class AndrewKernel(IPythonKernel):
	
    #executed jupyter commands are saved here in order as a record 
    currentCode = {} #  { count:[code, stdout, stderr] } 
    
    recordOutput = False
    
    #override ipkernel methods
	
    def start(self):   
		     
        self.currentCode = {}
        super(AndrewKernel, self).start()
		

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
		
        code_lower = code.lower()
		
        # Function for calling base class's execution method
        def super_execute(execcode):
            currentStdout = currentStderr = ""
            
            if self.recordOutput == True:
                #capture stdout and stderr
                with io.capture_output() as captured:                  
                    res = super(AndrewKernel, self).do_execute(code=execcode, silent=silent, store_history=store_history, user_expressions=user_expressions, allow_stdin=allow_stdin)        
                
                currentStdout = captured.stdout
                currentStderr = captured.stderr
                
                #show stdout and stderr to user
                if captured.stdout != "":
                    print captured.stdout
                if captured.stderr != "":
                    print captured.stderr
            
            else:
                res = super(AndrewKernel, self).do_execute(code=execcode, silent=silent, store_history=store_history, user_expressions=user_expressions, allow_stdin=allow_stdin)
            
            #add to my code record    
            self.currentCode[self.execution_count - 1] = [execcode, str(currentStdout), str(currentStderr)]
            return res
        
        
        if "%reset" in code_lower:
            self.currentCode = {}

		# Print the record of everything run since restart/reset for debug
        if "##printmy" in code_lower:
            
            printmysession = False; printmyout = False
            if "session" in code_lower:
                printmysession = True
            if "out" in code_lower:
                printmyout = True
					
            for blockNo in self.currentCode:
                blockCode = self.currentCode[blockNo]
                
                print "####################### BLOCK {0} #######################\n".format(blockNo)    
                
                if printmysession == True:
                    print "{0}\n".format(blockCode[0].encode("utf-8"))
                if printmyout == True:
                    if blockCode[1] != "":
                        print "##CAPTURED STDOUT##\n{0}".format(blockCode[1].encode("utf-8"))
                    if blockCode[2] != "":
                        print "##CAPTURED STDERR##\n{0}".format(blockCode[2].encode("utf-8"))
                
            return

        # Rerun block(s) of code (i.e. ##rerun 2 4 executes 2,3,4)
        if "##rerun" in code_lower:
            codelist = code_lower.split()          
            
            startrange = int(codelist[1])
            try: endrange = int(codelist[2])
            except IndexError: endrange = int(codelist[1])
            
            for i in range(startrange, endrange + 1):
                if i in self.currentCode.keys():
                    
                    #re-execute blocks of code from the record
                    super_execute(self.currentCode[i][0])      
            return
        
        # Change recording settings
        if "##recordoutput" in code_lower:
            if "off" in code_lower:
                self.recordOutput = False
                print "Recording output off"
            else:
                self.recordOutput = True
                print "Recording output on"
            
            return
        
               
        return super_execute(code)
        
        

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=AndrewKernel)
