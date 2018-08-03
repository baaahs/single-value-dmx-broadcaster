import array
from ola.ClientWrapper import ClientWrapper

wrapper = None
TICK_INTERVAL = 1000

def DmxSent(state):
  if not state.Succeeded():
    wrapper.Stop()

def SendDMXFrame():

  wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
  data = array.array('B', [255] * 512)
  wrapper.Client().SendDmx(0, data, DmxSent)
                                                                                                                        
wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()
