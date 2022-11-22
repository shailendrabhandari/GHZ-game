
##Shailendra Bhandari November 15 2022.
'''

MIT License

Copyright (c) 2022 Shailendra Bhandari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.'''



#import necessary libraries
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit
from qiskit import execute, BasicAer
from random import randint

###Alice, Bob and Charlie are the three players of Team ABC and they will get either x or y from the referee. Therefore their variables are defined as a_x, b_x,c_x and a_y, b_y, c_y respectively.

def Alice(Alices_x, Alices_y): global a_x; global a_y; a_x = Alices_x; a_y = Alices_y;
def Bob(Bobs_x, Bobs_y): global b_x; global b_y; b_x = Bobs_x; b_y = Bobs_y;
def Charlie(Charlies_x, Charlies_y): global c_x; global c_y; c_x = Charlies_x; c_y = Charlies_y;

def geta_x(): return a_x;
def getb_x(): return b_x;
def getc_x(): return c_x;
def geta_y(): return a_y;
def getb_y(): return b_y;
def getc_y(): return c_y;

##In order to always win the game they need to use the quantum strategy and typically a three state entangled quantum circuit. Alice, Bob and Charlie

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
        q = QuantumRegister(3) #this creates a quantum register with one qubit
        # create a classical register that will hold the results of the measurement
        c = ClassicalRegister(3) 
        qc = QuantumCircuit(q, c) # creates the quantum circuit
        ghz_state(qc,q) # bring circuit in ghz_state (entangled)
        if (i ==1): # ask all for xxx
            # team ABC 
            if (a_x*b_x*c_x == 1): correctABC = True; # if the product of the x values = 1 -> win
            # ask team Quantum (for all) for xxx
            xxx(qc, q)
            counts = simulate(qc, q, c, 1)
            if ("000" in counts or "011" in counts or "101" in counts or "110" in counts): correctQuantum = True; # if the product of the x values = -1 -> win
## for xy in different combination
        else:
            if (i==2): # if the random number is 1 make an XYY-measurement
                if (a_x*b_y*c_y == -1): correctABC = True;
                xyy(qc, q)
            elif (i==3): # YXY-measurement
                if (a_y*b_x*c_y == -1): correctABC = True;
                yxy(qc, q)
            elif (i==4): # YYX-measurement
                if (a_y*b_y*c_x == -1): correctABC = True;
                yyx(qc, q)
            counts = simulate(qc, q, c, 1)

            if ("001" in counts or "010" in counts or "100" in counts or "111" in counts): correctQuantum = True; # if product = -1 -> win  Because the winning condition of the game is either +1/or-1
        print ("Round ", i, ", Question ", i)
        if (correctQuantum == True and correctABC != True): print ("Team ABC is wrong, Team Quantum is right"); 
        elif (correctQuantum != True and correctABC == True): print ("Team ABC is right, Team Quantum is wrong");
        else: print ("Both teams are right")
        i = i+1;

def xxx(qc, q):  #for xxx
    qc.h(q[0])
    qc.h(q[1])
    qc.h(q[2])
    return qc

def xyy(qc, q):  #for xxy
    qc.h(q[0])
    qc.sdg(q[1])
    qc.h(q[1])
    qc.sdg (q[2])
    qc.h(q[2])
    return qc

def yxy(qc, q):    #for yxy
    qc.sdg(q[0])
    qc.h(q[0])
    qc.h(q[1])
    qc.sdg (q[2])
    qc.h(q[2])
    return qc

def yyx(qc, q):   # for yyx
    qc.sdg(q[0])
    qc.h(q[0])
    qc.h(q[1])
    qc.sdg(q[2])
    qc.h(q[2])
    return qc

def simulate(qc, q, c, s):
    backend = BasicAer.get_backend('qasm_simulator') # define the backend for simulation
    qc.measure(q,c) 
    job = execute(qc, backend, shots=s) # run the job simulation
    result = job.result() # grab the result
    counts = result.get_counts(qc) # results for the number of runs
    return counts

def randomQuestion():
    print ("The question to Team ABC is getting asked by the referee is:")
    Q = randint (1,4)
    if (Q == 1): print("x, x, x"); 
    if (Q == 2): print("x, y, y");
    if (Q == 3): print("y, y, x");
    if (Q == 4): print("y, x, y");
    return Q;

def correctAnswer(Q): # prints out the appropriate list of gates per questions so as to generate the GHZ circuit later
    print ("Copy the following code in the cell below for the measurement of above question:\n\n")
    if (Q==1):
        print ("qc.h(q[0])\nqc.h(q[1])\nqc.h(q[2])")
    if (Q==2):
        print ("qc.h(q[0])\nqc.sdg(q[1])\nqc.h(q[1])\nqc.sdg(q[2])\nqc.h(q[2])")
    if (Q==3):
        print ("qc.sdg(q[0])\nqc.h(q[0])\nqc.sdg(q[1])\nqc.h(q[1])\nqc.h(q[2])")
    if (Q==4):
        print ("qc.sdg(q[0])\nqc.h(q[0])\nqc.h(q[1])\nqc.sdg(q[2])\nqc.h(q[2])")


def circuitCheck(qc,q,c,Q): ##there are 8 possible combination and the game can be played with either of 4 best ways to win
    counts = simulate(qc, q, c, 10000) # number of counts for the simulations/shots=10000
    if (Q==1): 
        if (("000" in counts or "011" in counts or "101" in counts or "110" in counts) and ("001" not in counts and "010" not in counts and "100" not in counts and "111" not in counts)):
            print ("Perfect! Team ABC won!☺️")
        else: print ("There might still be a mistake.🤔️")
    else:
        if (("001" in counts or "010" in counts or "100" in counts or "111" in counts) and ("000" not in counts and "011" not in counts and "101" not in counts and "110" not in counts)):
            print ("Perfect! Team ABC won!😊️")
        else: print ("There might still be a mistake.🤔️")
            
