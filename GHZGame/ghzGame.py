from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import execute, BasicAer
from random import randint

#ColorX shape y

def Alice(Alices_x, Alices_y): global a_x; global a_y; a_x = Alices_x; a_y = Alices_y;
def Bob(Bobs_x, Bobs_y): global b_x; global b_y; b_x = Bobs_x; b_y = Bobs_y;
def Charlie(Charlies_x, Charlies_y): global c_x; global c_y; c_x = Charlies_x; c_y = Charlies_y;

def geta_x(): return a_x;
def getb_x(): return b_x;
def getc_x(): return c_x;
def geta_y(): return a_y;
def getb_y(): return b_y;
def getc_y(): return c_y;

def ghz_state(qc,q):
    # create GHZ state
    qc.h(q[0])
    qc.cx(q[0],q[1])
    qc.cx(q[0],q[2])
    qc.barrier()
    return qc

def runExperiment():
    for i in range (1,5):
        correctABC = False; correctQuantum = False;
        # create the quantum circuit with the chosen coin moves
        q = QuantumRegister(3) # create a quantum register with one qubit
        # create a classical register that will hold the results of the measurement
        c = ClassicalRegister(3) 
        qc = QuantumCircuit(q, c) # creates the quantum circuit
        ghz_state(qc,q) # bring circuit in ghz_state
        if (i ==1): # ask all for x
            # team ABC 
            if (a_x*b_x*c_x == -1): correctABC = True; # if the product of the x values = 1 -> win
            # team Quantum (quantum)
            xxx(qc, q)
            counts = simulate(qc, q, c, 1)
            if ("000" in counts or "011" in counts or "101" in counts or "110" in counts): correctQuantum = True; # if the product of the x values = -1 -> win 
        else:
            if (i==2): # if the random number is 1 make an XYY-measurement
                if (a_x*b_y*c_y == 1): correctABC = True;
                xyy(qc, q)
            elif (i==3): # YXY-measurement
                if (a_y*b_x*c_y == 1): correctABC = True;
                yxy(qc, q)
            elif (i==4): # YYX-measurement
                if (a_y*b_y*c_x == 1): correctABC = True;
                yyx(qc, q)
            counts = simulate(qc, q, c, 1)
            if ("001" in counts or "010" in counts or "100" in counts or "111" in counts): correctQuantum = True; # if product = 1 -> win
        print ("Round ", i, ", Question ", i)
        if (correctQuantum == True and correctABC != True): print ("Team ABC is wrong, Team Quantum was right"); 
        elif (correctQuantum != True and correctABC == True): print ("Team ABC was right, Team Quantum was wrong");
        else: print ("Both teams are right")
        i = i+1;

def xxx(qc, q):
    qc.h(q[0])
    qc.h(q[1])
    qc.h(q[2])
    return qc

def xyy(qc, q):
    qc.h(q[0])
    qc.sdg(q[1])
    qc.h(q[1])
    qc.sdg (q[2])
    qc.h(q[2])
    return qc

def yxy(qc, q):
    qc.sdg(q[0])
    qc.h(q[0])
    qc.h(q[1])
    qc.sdg (q[2])
    qc.h(q[2])
    return qc

def yyx(qc, q):
    qc.sdg(q[0])
    qc.h(q[0])
    qc.h(q[1])
    qc.sdg(q[2])
    qc.h(q[2])
    return qc

def simulate(qc, q, c, s):
    backend = BasicAer.get_backend('qasm_simulator') # define the backend
    qc.measure(q,c) 
    job = execute(qc, backend, shots=s) # run the job simulation
    result = job.result() # grab the result
    counts = result.get_counts(qc) # results for the number of runs
    return counts

def randomQuestion():
    print ("The question to Team ABC is getting asked is:")
    Q = randint (1,4)
    if (Q == 1): print("x, x, x"); 
    if (Q == 2): print("x, y, y");
    if (Q == 3): print("y, y, x");
    if (Q == 4): print("y, x, y");
    return Q;

def correctAnswer(Q): # prints out the 
    print ("Copy the following code in the cell above:\n\n")
    if (Q==1):
        print ("qc.h(q[0])\nqc.h(q[1])\nqc.h(q[2])")
    if (Q==2):
        print ("qc.h(q[0])\nqc.sdg(q[1])\nqc.h(q[1])\nqc.sdg(q[2])\nqc.h(q[2])")
    if (Q==3):
        print ("qc.sdg(q[0])\nqc.h(q[0])\nqc.sdg(q[1])\nqc.h(q[1])\nqc.h(q[2])")
    if (Q==4):
        print ("qc.sdg(q[0])\nqc.h(q[0])\nqc.h(q[1])\nqc.sdg(q[2])\nqc.h(q[2])")


def circuitCheck(qc,q,c,Q):
    counts = simulate(qc, q, c, 10000)
    if (Q==2): 
        if (("000" in counts or "011" in counts or "101" in counts or "110" in counts) and ("001" not in counts and "010" not in counts and "100" not in counts and "111" not in counts)):
            print ("Perfect! Team ABC won!")
        else: print ("Hmmm... There might still be a mistake.")
    else:
        if (("001" in counts or "010" in counts or "100" in counts or "111" in counts) and ("000" not in counts and "011" not in counts and "101" not in counts and "110" not in counts)):
            print ("Perfect! Team ABC won!")
        else: print ("Hmmm... There might still be a mistake.")
            
def quiz():
    print ("(a) All 8 possible states equally mixed (|000>, |001>, |010>, ..., |110>, |111>)\n(b) A random distribution across all 8 states (|000>, |001>, |010>, ..., |110>, |111>)\n(c) Measurement result in 50% is state |000> and in 50% is state |100>\n(d) Measurement result in 50% is state |000> and in 50% is state |111>")
    answer = input()
    if answer == "d" or answer == "D":
        print ("Your answer was correct!")
    else: 
        print ("No, try again!")
  
