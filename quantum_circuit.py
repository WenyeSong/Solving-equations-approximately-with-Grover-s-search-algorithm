#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[2]:


from qiskit_ibm_runtime import QiskitRuntimeService, Session, Sampler
from qiskit import QuantumCircuit, transpile

from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.compiler import transpile


service = QiskitRuntimeService(
    channel='ibm_quantum',
    instance='ibm-q/open/main',
    token='8faa1f6398ff0a6e69b87ceda395546e9adc6ce4359891e2895badc8893ae7f6d583d5b6481296cca3438a604e14d2853cc2843b019cffbaa2498dfb8a9dc9eb'
) # Wenye Song's IMB account API

my_backend = service.backend(name="ibm_brisbane")
print(my_backend)
print(service.backends())
print(my_backend.configuration())
print(my_backend.status())


# In[3]:


from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
#from qiskit.visualization import plot_histogram
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2 as Sampler

# first time need to login to IBM account to save_account）
#QiskitRuntimeService.save_account(channel="ibm_quantum", token="8faa1f6398ff0a6e69b87ceda395546e9adc6ce4359891e2895badc8893ae7f6d583d5b6481296cca3438a604e14d2853cc2843b019cffbaa2498dfb8a9dc9eb")
#service = QiskitRuntimeService(channel="ibm_quantum")

provider=QiskitRuntimeService(channel="ibm_quantum", token="8faa1f6398ff0a6e69b87ceda395546e9adc6ce4359891e2895badc8893ae7f6d583d5b6481296cca3438a604e14d2853cc2843b019cffbaa2498dfb8a9dc9eb")
backend = service.backend("ibm_brisbane")
pm = generate_preset_pass_manager(optimization_level=3, backend=backend)  # optimize cricuit


# In[4]:


# circuit: 3x+1=0
# successfully run 3x+1=0 on a real processor in python3.8 and 3.9

from qiskit.circuit.library import C4XGate

qreg_f = QuantumRegister(1, 'f')
qreg_a = QuantumRegister(4, 'a')
qreg_j = QuantumRegister(2, 'j')
creg_c = ClassicalRegister(2, 'c')
circuit = QuantumCircuit(qreg_f, qreg_a, qreg_j, creg_c)    # this is the circuit for 3x+1=0, qiskit code

circuit.x(qreg_f[0])
circuit.h(qreg_j[0])
circuit.h(qreg_j[1])
circuit.h(qreg_f[0])
circuit.barrier(qreg_f[0], qreg_a[0], qreg_a[1], qreg_a[2], qreg_a[3], qreg_j[0], qreg_j[1])
circuit.cx(qreg_j[0], qreg_a[0])
circuit.cx(qreg_j[0], qreg_a[1])
circuit.cx(qreg_j[1], qreg_a[1])
circuit.ccx(qreg_j[0], qreg_j[1], qreg_a[2])
circuit.cx(qreg_j[1], qreg_a[3])
circuit.barrier(qreg_f[0], qreg_a[0], qreg_a[1], qreg_a[2], qreg_a[3], qreg_j[0], qreg_j[1])
circuit.cx(qreg_a[1], qreg_a[2])
circuit.x(qreg_a[1])
circuit.barrier(qreg_f[0], qreg_a[0], qreg_a[1], qreg_a[2], qreg_a[3], qreg_j[0], qreg_j[1])
circuit.append(C4XGate(), [qreg_a[1], qreg_a[0], qreg_a[2], qreg_a[3], qreg_f[0]])
circuit.x(qreg_a[0])
circuit.x(qreg_a[1])
circuit.x(qreg_a[2])
circuit.x(qreg_a[3])
circuit.append(C4XGate(), [qreg_a[1], qreg_a[0], qreg_a[2], qreg_a[3], qreg_f[0]])
circuit.x(qreg_a[0])
circuit.append(C4XGate(), [qreg_a[1], qreg_a[0], qreg_a[2], qreg_a[3], qreg_f[0]])
circuit.x(qreg_a[1])
circuit.x(qreg_a[2])
circuit.x(qreg_a[3])
circuit.barrier(qreg_f[0], qreg_a[0], qreg_a[1], qreg_a[2], qreg_a[3], qreg_j[0], qreg_j[1])
circuit.x(qreg_a[1])
circuit.cx(qreg_a[1], qreg_a[2])
circuit.cx(qreg_j[1], qreg_a[3])
circuit.ccx(qreg_j[0], qreg_j[1], qreg_a[2])
circuit.cx(qreg_j[1], qreg_a[1])
circuit.cx(qreg_j[0], qreg_a[1])
circuit.cx(qreg_j[0], qreg_a[0])
circuit.barrier(qreg_f[0], qreg_a[0], qreg_a[1], qreg_a[2], qreg_a[3], qreg_j[0], qreg_j[1])
circuit.h(qreg_j[0])
circuit.h(qreg_j[1])
circuit.x(qreg_j[0])
circuit.x(qreg_j[1])
circuit.cz(qreg_j[1], qreg_j[0])
circuit.x(qreg_j[0])
circuit.x(qreg_j[1])
circuit.h(qreg_j[0])
circuit.h(qreg_j[1])
circuit.measure(qreg_j[1], creg_c[1])
circuit.measure(qreg_j[0], creg_c[0])




# In[6]:


# run in real processor without mitigation
circuit1 = pm.run(circuit)  

with Session(backend=backend) as session:  # the correct way to run the circuit: in session
    sampler = Sampler() 
    job = sampler.run([circuit1]) 
    result = job.result()
    print(f">>> Job ID: {job.job_id()}")
    print(f">>> Job Status: {job.status()}")


#sampler = Sampler(backend=backend)

pub_result = result[0]
print(f"Counts for the meas output register: {pub_result.data.c.get_counts()}")


# In[18]:


# error mitigation set up
from qiskit.circuit.library import RealAmplitudes
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
import mthree
import numpy as np

mit = mthree.M3Mitigation(backend) # need python 3.9


# In[19]:


# run in real processor with mitigation

from qiskit import transpile  

transpiled_circuit = transpile(circuit, backend=backend)


#print("Final layout mapping:", transpiled_circuit.layout)

physical_qubits = [12,17] # by checking the physical_qubits of logical qubits (qreg_j[0] and qreg_j[1] by printing the layout)


# excute error mitigation: collect the error： By running multiple times (shots=1024) to statistically analyze measurement errors
# the error mitigation calibration measures all possible states and constructs a measurement error transition matrix, which is used to invert the errors.
# A⋅Ptrue = Pmean, Aij: the probibility j will be measured to i

mit.cals_from_system(  
    qubits=physical_qubits,
    shots=1024
)

with Session(backend=backend) as session:
    sampler = Sampler()
    job = sampler.run([transpiled_circuit])
    print(f">>> Job ID: {job.job_id()}")
    print(f">>> Job Status: {job.status()}")
    result = job.result()
    print(f">>> Job Status: {job.status()}")



# In[14]:


# run in real processor with mitigation

raw_prob = result[0].data.c.get_counts()
num_qubits = len(physical_qubits)  # = 2
raw_counts_int = {format(int(k), f"0{num_qubits}b"): v for k, v in raw_prob.items()}


# apply the measurement error transition matrix to the result: Ptrue = A^-1·Pmean
corrected_prob = mit.apply_correction(raw_prob, qubits=physical_qubits, return_mitigation_overhead=False)

print("Corrected probability distribution:", corrected_prob)

# transferred the disteribution to counts
corrected_counts = {}
for int_state, prob in corrected_prob.items():
    corrected_counts[int_state] = float(round(prob * 1024, 2))


print("Corrected approx counts:", corrected_counts)


# In[ ]:





# In[23]:


job_to_cancel = service.job("cz4jdmekvm9g008g6pm0")
job_to_cancel.cancel()
print(f"Canceled job: {job_to_cancel.job_id()}")

job_to_cancel = service.job("cz4ja50kvm9g008g6nvg")
job_to_cancel.cancel()
print(f"Canceled job: {job_to_cancel.job_id()}")


# In[ ]:




