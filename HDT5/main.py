import simpy
import random



def process(env, processName, ram_memory, memory_size, time, instructions, velocity):
  #NEW
  #simular cuando el proceso se inicie
  yield env.timeout(time)
  
  startTime = env.now
  print("Tiempo [%a] - %s necesita %d de RAM" % (time, processName, memory_size))

  #READY
  yield ram_memory.get(memory_size)
  print("%s usara %d de ram" % (processName, memory_size)) 
  
  instructions_Ready = 0 
 
  #RUNNING
  while instructions_Ready < instructions:
    with cpu.request() as req:
      yield req 
      if(instructions - instructions_Ready) >= velocity:
        executed = velocity
      else: 
        executed = instructions - instructions_Ready
      
      print("%s - el cpu ejecuta %d instrucciones" % (processName, executed))

      yield env.timeout(executed/velocity)
      
      instructions_Ready += executed
      print("%s - Terminadas con CPU (%d/%d)" % (processName, instructions_Ready, instructions))
      
    decision = random.randint(1, 2)
    
    if (decision == 1) and (instructions_Ready < instructions):
      with __wait__.request() as req_1:
        yield req_1 
        yield env.timeout(1)

  yield ram_memory.put(memory_size)
  print("Tiempo [%s] - %s - libero %d de ram" % (time, processName, memory_size))
   
  global time_list 
  global time_T 
  time_list.append((env.now - startTime))
  time_T += (env.now - startTime)
  
  
#-----------------------------------------------

velocity = 6
process_c = 25
time_T = 0
time_list = []

env = simpy.Environment()
ram_memory = simpy.Container(env, init=100, capacity=100)
cpu = simpy.Resource(env, capacity=4)
__wait__ = simpy.Resource(env, capacity=2)

intevalo = 1

for i in range(process_c):
  memory_size = random.randint(1,10)
  instructions_ = random.randint(1, 10)
  time = random.expovariate(1 / intevalo)
  
  env.process(process(env, ("Program" + str(i)), ram_memory, memory_size, time, instructions_, velocity))
  
env.run()

#Promedio
print()
print("Tiempo promedio es: " + str((time_T / process_c)) + " seg")

#Desviacion estandar 
sum = 0
for i in time_list:
  sum += (i - ((time_T / process_c))) ** 2
print()
print("Desviacion estandar es: " + str((sum / (process_c - 1)) ** 0.5))