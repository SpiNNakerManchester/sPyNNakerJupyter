'''
Put this file in the python2.7/site-packages folder
Place the suitable kernel folder in either /usr/local/share/jupyter/kernels or /usr/share/jupyter/kernels
'''

from ipykernel.ipkernel import IPythonKernel

class AndrewKernel(IPythonKernel):
	
    #executed jupyter commands are saved here in order as a record 
    currentCode = {}
    
	
    #override ipkernel methods
	
    def start(self):   
		     
        self.currentCode = {}
        super(AndrewKernel, self).start()
		

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
		
        code_lower = code.lower()
		
        def super_execute(execcode):
            return super(AndrewKernel, self).do_execute(code=execcode, silent=silent, store_history=store_history, user_expressions=user_expressions, allow_stdin=allow_stdin)
        
        if "%reset" in code_lower:
            self.currentCode = {}

		# Print the record of everything run since restart/reset for debug
        if "##printmysession" in code_lower:
            for blockNo in self.currentCode:
                print "#block {0}\n{1}\n".format(blockNo, self.currentCode[blockNo])
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
                    self.currentCode[self.execution_count] = self.currentCode[i]
                    super_execute(self.currentCode[i])      
            return
        
        
        self.currentCode[self.execution_count] = code
        
        return super_execute(code)
        
        

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=AndrewKernel)
