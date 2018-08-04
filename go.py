#!/usr/bin/env python2.7

import argparse
import array
from ola.ClientWrapper import ClientWrapper

DEFAULT_FRAME_VALUE = 255
DEFAULT_UNIVERSE = 0
DEFAULT_TICK_INTERVAL = 1000

parser = argparse.ArgumentParser(description='Universe Broadcast Ticker')

def check_range(arg):
    try:
        value = int(arg)
    except ValueError as err:
       raise argparse.ArgumentTypeError(str(err))

    if value < 0 or value > 255:
        message = "Expected 0-255, got value = {}".format(value)
        raise argparse.ArgumentTypeError(message)

    return value

parser.add_argument("--frame-value", type=check_range, default=DEFAULT_FRAME_VALUE, nargs="?", help="Frame value")
parser.add_argument('--universe', dest='universe', type=int, default=DEFAULT_UNIVERSE, help="DMX universe")
parser.add_argument('--tick-interval', dest='tick_interval', type=int, default=DEFAULT_TICK_INTERVAL, help="Tick (callback) interval")

args = parser.parse_args()

wrapper = None

def DmxSent(state):
  if not state.Succeeded():
    wrapper.Stop()

def SendDMXFrame():

  wrapper.AddEvent(args.tick_interval, SendDMXFrame)
  data = array.array('B', [args.frame_value] * 512)
  wrapper.Client().SendDmx(args.universe, data, DmxSent)
                                                                                                                        
wrapper = ClientWrapper()
wrapper.AddEvent(args.tick_interval, SendDMXFrame)
wrapper.Run()
