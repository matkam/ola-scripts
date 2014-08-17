#!/usr/bin/env python

from array import *
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import DMX_MIN_SLOT_VALUE, DMX_MAX_SLOT_VALUE, \
  DMX_UNIVERSE_SIZE

UPDATE_INTERVAL = 25 # In ms, this comes about to ~40 frames a second
LIGHTS = 17
COLORS = 3
UNIVERSE = 1

R = 0
G = 1
B = 2

MODE_PINK = 0
MODE_WHITE = 1
MODE_GREEN = 2
MODE_BLACK = 3

class CoolController(object):
  def __init__(self, universe, update_interval, client_wrapper,
               dmx_data_size=DMX_UNIVERSE_SIZE):
    dmx_data_size = min(dmx_data_size, DMX_UNIVERSE_SIZE)
    self._universe = universe
    self._update_interval = update_interval
    self._data = array ('B', [DMX_MIN_SLOT_VALUE] * dmx_data_size)
    self._wrapper = client_wrapper
    self._client = client_wrapper.Client()
    self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)

    self.curr_light = 0

    self.curr_mode = MODE_PINK
    self.curr_red = 255
    self.curr_green = 0
    self.curr_blue = 255


  def SetModePink(self):
    self.curr_mode = MODE_PINK
    self.curr_red = 255
    self.curr_green = 0
    self.curr_blue = 255

  def SetModeGreen(self):
    self.curr_mode = MODE_GREEN
    self.curr_red = 0
    self.curr_green = 255
    self.curr_blue = 0

  def SetModeWhite(self):
    self.curr_mode = MODE_WHITE
    self.curr_red = 255
    self.curr_green = 255
    self.curr_blue = 255

  def SetModeBlack(self):
    self.curr_mode = MODE_BLACK
    self.curr_red = 0
    self.curr_green = 0
    self.curr_blue = 0

  def UpdateDmx(self):
    if self.curr_light >= LIGHTS:
      self.curr_light = 0
      if self.curr_mode == MODE_PINK:
        self.SetModeWhite()
      elif self.curr_mode == MODE_WHITE:
        self.SetModeGreen()
      elif self.curr_mode == MODE_GREEN:
        self.SetModeBlack()
      elif self.curr_mode == MODE_BLACK:
        self.SetModePink()

    offset = self.curr_light*COLORS
    self._data[offset+R] = self.curr_red
    self._data[offset+G] = self.curr_green
    self._data[offset+B] = self.curr_blue
    self.curr_light += 1
    
    self._client.SendDmx(self._universe, self._data)
    self._wrapper.AddEvent(self._update_interval, self.UpdateDmx)

if __name__ == '__main__':
  wrapper = ClientWrapper()
  controller = CoolController(UNIVERSE, UPDATE_INTERVAL, wrapper,
                                    LIGHTS*COLORS)
  try:
    wrapper.Run()
  except KeyboardInterrupt:
    wrapper.Stop

