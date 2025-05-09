
valid_commands = [10,11,20,21,22,30,31,32,33,40,41,42,43]

class Virtual_Machine:
    #setup
    def __init__(self):
        self.accumulator = 0

        self.registers = []

        self.line = 0

        self.cf = {10:self.read,11:self.write,
        20:self.load,21:self.store,22:self.set_a,
        30:self.add,31:self.sub,33:self.mul,32:self.div,
        40:self.branch,41:self.branchneg,42:self.branchzero}

        for i in range(100):
            self.registers.append(0)

    #functionality

    #i/o
    def read(self,addr):
        self.registers[addr] = int(input('?-'))


    def write(self,addr):
        print('VM- ' + str(self.registers[addr]))

    #load/store
    def load(self,addr):
        self.accumulator = int(self.registers[addr])

    def store(self,addr):
        self.registers[addr] = self.accumulator

    def set_a(self,num):
        self.accumulator = num

    #math ops
    def add(self,addr):
        self.accumulator += int(self.registers[addr])

    def sub(self,addr):
        self.accumulator -= int(self.registers[addr])

    def mul(self,addr):
        self.accumulator *= int(self.registers[addr])

    def div(self,addr):
        self.accumulator /= int(self.registers[addr])

    #control ops
    def branch(self,addr):
        self.line = addr

    def branchneg(self,addr):
        if self.accumulator < 0:
            self.line = addr

    def branchzero(self,addr):
        if self.accumulator == 0:
            self.line = addr

    def newcommand(self,command,reg):
        self.registers[reg] = command
    
    #run program
    def run_command(self,operator,operand):
        self.cf[operator](operand)

    def run_program(self):
        command = self.registers[self.line]
        if int(command) == 0:
            return False
        operator = int(str(command)[:2])
        operand = int(str(command)[2:])
        if (0 <= operand < 100) and (operator in valid_commands):
            if operator == 43:
                self.line = 0
                return 2
            self.run_command(operator,operand)
            self.line += 1
            if self.line == 100:
                self.line = 0
            return True
        self.line = 0
        return False

class Operator:
    def __init__(self):
        self.commandline = 0
        self.vm = Virtual_Machine()
    
    def start_up_sequence(self):
        print('***         Welcome To The Simple Virtual Machine         ***')
        print('***  You May Write A Program Using The Basic ML Language  ***')
        print('***            To Run Your Program Type 99999            ***')
        print('***        To Halt The Virtual Machine Type 99998         ***')

    def memory_dump(self):
        print('VM- Commencing Memory Dump\n\n')
        num = 0
        string = ''
        for i in self.vm.registers:
            snm = str(num)
            if len(snm) == 1:
                snm = '0' + snm
            mstr = str(i)
            while len(mstr) < 4:
                mstr = '0' + mstr
            snm += ':' + mstr
            snm += ' '
            if (num % 10 == 0) and (num > 0):
                snm = '\n'+snm
            string += snm
            num += 1
        print(string)
    
    def take_user_input(self):
        inp = int(input(str(self.commandline)+':-'))
        while not self.store_command(inp):
            print('VM- Incorrect Command')
            print('VM- Please Try Again')
            inp = int(input(str(self.commandline)+':-'))
        self.commandline += 1

    def store_command(self,command):
        if command == 99999:
            print('VM- Initiating Program...')
            self.run_program()
            return True
        elif command == 99998:
            print('VM- Goodbye')
            quit()
        else:
            operator = int(str(command)[:2])
            operand = str(command)[2:]
            if (operator in valid_commands) and (len(operand) == 2):
                self.vm.newcommand(command,self.commandline)
                return True
        return False
    
    def run_program(self):
        while True:
            rt = self.vm.run_program()
            if rt != True:
                break
        if rt == 2:
            print('VM- Program Halted')
            self.memory_dump()
        else:
            print('VM- Forced Halt At Line ' + str(self.vm.line))
            self.vm.line = 0
        self.commandline = -1
    
    def main_loop(self):
        self.start_up_sequence()
        while True:
            self.take_user_input()

mymachine = Operator()

mymachine.main_loop()