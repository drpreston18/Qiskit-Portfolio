from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt 
import numpy as np

# Declare & Initialize our quantum & classical registers with 3 qubits & 3 bits respectively.
QR1 = QuantumRegister( 3 )
CR1 = ClassicalRegister( 3 )

# Declare & initialize our quantum circuit with 3 qubits & 3 classical bits.
QC = QuantumCircuit( QR1, CR1 )

# Rotate our target qubit for teleportation to some unique arbitrary state. 
# To do this, let's use variables for our random numbers so we can reference them later.
Theta  = np.random.uniform( 0 , ( 2 * np.pi ) )
Phi    = np.random.uniform( 0 , ( 2 * np.pi ) )
Lambda = np.random.uniform( 0 , ( 2 * np.pi ) )

# First rotate around Y axis, then Z axis, then X axis.
QC.ry( Theta  , QR1[ 0 ] )
QC.rz( Phi    , QR1[ 0 ] )
QC.rx( Lambda , QR1[ 0 ] )

# Because we are teleporting a arbitrary unique state, we must first verify what
# the state of our target qubit is before teleportation so we can compare later.
Temp_QC = QuantumCircuit( QR1 )
Temp_QC.ry( Theta , 0 )
Temp_QC.rz( Phi , 0 )
Temp_QC.rx( Lambda , 0 )
InitialState = Statevector.from_instruction( Temp_QC )

# Display initial state on bloch sphere.
plot_bloch_multivector( InitialState )
plt.show()

# Create maximally entangle bell state between qubits 1 & 2.
QC.h( QR1[ 1 ] )
QC.cx( QR1[ 1 ], QR1[ 2 ] )
# Now entangle qubits 0 & 1.
QC.cx( QR1[ 0 ], QR1[ 1 ] )
QC.h( QR1[ 0 ] )

# Measure qubits 0 & 1 & store them as classical bits 0 & 1 respectively.
QC.measure( QR1[ 0 ], CR1[ 0 ] )
QC.measure( QR1[ 1 ], CR1[ 1 ] )

# Now apply conditional gates based on our classical bit states.
# Apply X gate on qubit 2 if classical bit 0 is 1.
with QC.if_test( ( CR1[ 1 ], 1 ) ):
    QC.x( QR1[ 2 ] )
# Apply Z gate on qubit 2 if classical bit 1 is 1.
with QC.if_test( ( CR1[ 0 ], 1 ) ):
    QC.z( QR1[ 2 ] )

# Save statevector.
QC.save_statevector()

# Simulate the circuit.
Simulator = AerSimulator()
Outcome = Simulator.run( QC ).result()

# Get final statevector.
FinalState = Outcome.get_statevector( QC )

# Display as plot.
plot_bloch_multivector( FinalState )
plt.show()