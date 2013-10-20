# Copyright 2013 Christopher Small

"""
Resonance 

A rewrite of the Resonance Network Access Control Application in PoX

While using some of the logic this is a rewrite with a DB and web interface view 
to be closly intergrated

"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.util import dpid_to_str

log = core.getLogger()


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

  def _handle_ConnectionUp (self, event):
  
    def record_switch ():
    	#Record new switch in Database if not seen before
		return

  	def push_default_rules (event):
      	# Push default rules so a host can DHCP
		# ARP
		msg_arp = of.ofp_flow_mod()
    	msg_arp.match.dl_type = pkt.ethernet.ARP_TYPE
    	msg_arp.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
    	event.connection.send(msg_arp)
    	
    	# DHCP 
    	msg_dhcp = of.ofp_flow_mod()
    	msg_dhcp.match.dl_type = pkt.ethernet.IP_TYPE
      	msg_dhcp.match.nw_proto = pkt.ipv4.UDP_PROTOCOL
      	msg_dhcp.match.tp_src = pkt.dhcp.CLIENT_PORT
      	msg_dhcp.match.tp_dst = pkt.dhcp.SERVER_PORT
    	
    	# If controller is a DHCPD Server
    	# msg_dhcp_send.actions.append(of.ofp_action_output(port = of.OFPP_CONTROLLER))
      	# Existing DHCPD server on network  -- client -> server
        msg_dhcp.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg_dhcp)
        
        # DHCP Server -> Client
        msg_dhcp.match.tp_src = pkt.dhcp.SERVER_PORT
      	msg_dhcp.match.tp_dst = pkt.dhcp.CLIENT_PORT
        
        event.connection.send(msg_dhcp)
        

        # Drop all other traffic
        msg_drop= of.ofp_flow_mod()
    	msg_drop.actions.append(of.ofp_action_output(port = of.OFPP_DROP)
    	event.connection.send(drop)
    	
		return
		
    push_default_rules(event)


""" 
    Handle all Packet Ins
"""

  def _handle_PacketIn (self, event):

    packet = event.parsed
    
    # Check if in the known MAC addresses, if so move MAC 
    
    wto operational
	


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
