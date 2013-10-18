# Copyright 2011 James McCauley
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX.  If not, see <http://www.gnu.org/licenses/>.

"""
Resonance 

A rewrite of the Resonance Network Access Control Application in PoX

While using some of the logic this is a rewrite with a DB and web interface view 
to be closly intergrated

"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time

log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0

class Resonance (object):
  """
  Resonance Network Access Control 

  Initalise switch into Registration State for all connections

  May want to add state store to more quickly recover from a disconnection of a switch
  without check of allowed MAC DB
  """
  def __init__ (self, connection, transparent):
    # Switch we'll be adding L2 learning switch capabilities to
    self.connection = connection
    self.transparent = transparent

    # Our Mac to user table
    self.macToUser = {}

    # We want to hear PacketIn messages, so we listen
    # to the connection
    connection.addListeners(self)

    log.debug("Initializing Resonance, transparent=%s",
              str(self.transparent))



  def record_switch ():
   """
    Record new switch in Database if not seen before"

    Update connection time if already seen
   """
	return

  def push_reg_rules ():
     """ 
      On initiation of a new switch push default rules so any connection is in 
      the "Registation" State
     """



	return


  def _handle_PacketIn (self, event):
    """
    Handle packet in messages from the switch to implement above algorithm.
    """

    packet = event.parsed



class resonance (object):
  """
  Waits for OpenFlow switches to connect.
  """
  def __init__ (self, transparent):
    core.openflow.addListeners(self)
    self.transparent = transparent

  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    Resonance(event.connection, self.transparent)


def launch (transparent=False, hold_down=_flood_delay):
  """
  Starts the resonance process 

  """ 
  core.registerNew(resonance, str_to_bool(transparent))
