from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_distribution
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np

# Simple demonstration of Grover's Algorithm on a three qubit register. 
# Note: marked state is |101> 

# Oracle function that marks desired state |101> by applying a global phase change.
# UserQuantumCircuit -> QuantumCircuit object.
# QubitNumber        -> Number of qubits in the register. 
def oracle( UserQuantumCircuit, QubitNumber ):
    UserQuantumCircuit.h( QubitNumber - 1 )
    UserQuantumCircuit.mcx( [ 0, 1 ], QubitNumber - 1, ctrl_state='01' )
    UserQuantumCircuit.h( QubitNumber - 1 )
    return UserQuantumCircuit

# Diffuser function that amplifies the probability amplitude of the marked state.
# UserQuantumCircuit -> QuantumCircuit object.
# QubitNumber        -> Number of qubits in the register.
def diffuser( UserQuantumCircuit, QubitNumber ):
    UserQuantumCircuit.h( range( QubitNumber ) )
    UserQuantumCircuit.x( QubitNumber - 1 )
    UserQuantumCircuit.h( QubitNumber - 1 )
    UserQuantumCircuit.mcx( [ 0 , 1 ], QubitNumber - 1, ctrl_state='00' )
    UserQuantumCircuit.h( QubitNumber - 1 )
    UserQuantumCircuit.x( QubitNumber - 1 )
    UserQuantumCircuit.h( range( QubitNumber ) )
    return UserQuantumCircuit

# Delcare & Initialize a quantum circuit with three qubits
QC = QuantumCircuit( 3 )

# Alpha calculation for number of iterations.
# Note: number of solutions is 1.
Alpha = np.arcsin( np.sqrt( 1 / np.power( 2, 3 ) ) )
# Number of iterations using Alpha. 
Iterations = round( np.pi / ( 4 * Alpha ) )
QC.h( range( 3 ) )

# Loop that iterates oracle & diffuser r times. 
for i in range( Iterations ):
    oracle( QC, 3 )
    diffuser( QC, 3 )

# Measure all qubits in our quantum circuit
QC.measure_all()

# Simulate complied circuit & Store results in Counts. 
Simulator = AerSimulator()
CompiledQC = transpile( QC, Simulator )
Result  = Simulator.run( CompiledQC, shots = 1024 ).result()
Counts = Result.get_counts()

# Print number of counts for each state & plot distribution 
print( f"Counts: { Counts }" )
plot_distribution( Counts )
plt.show()

