# Copyright 2013 Christopher Small

"""
Resonance-PoX

A rewrite of the Resonance Network Access Control Application in PoX

While using some of the logic this is a rewrite with a DB and web interface view 
to be closly intergrated

"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt
from pox.lib.util import dpid_to_str
#import mysql.connector

log = core.getLogger()


class resonance (object):
  """
  Waits for OpenFlow switches to connect.
  """
  # STATES
  UNKNOWN = 0
  REG = 1
  AUTH = 2
  QUAR = 3
  OPER = 4
 
  
  
  def __init__ (self, transparent):
    core.openflow.addListeners(self)
    self.transparent = transparent
    
    # Cache of authorized MAC DB -- includes userid and state associated with MAC
    self.macDB = {}
    

  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    push_default_rules(event)
  
  
  def _handle_PacketIn (self, event):
    packet = event.parsed
    
    log.debug("PacketIn Connection %s" % (event.connection,))
    
    # Check if in the known MAC addresses, if so move host to last known state
    if state = self.macDB[packet.src]
    else state = REG
    
    log.debug("Packet In, mac=%s DB state=%s",
              packet.src, state)
    
    
    # Check what state the host was in
    
    # UNKNOWN state,push rules to move to registration state
	if state == REG
		# Push Web Redirect	
		portal_ip = get_portal_ip()
		msg_web = of.ofp_flow_mod()
        msg_web.match.dl_type = pkt.ethernet.IP_TYPE
        msg_web.match.nw_proto = pkt.ipv4.TCP_PROTOCOL
        msg_dhcp.actions.append(of.ofp_action_output(nw_addr.set_dst(portal_ip)
		event.connection.send(msg_web)	
				
	if state == OPER
	     # Push in normal rule	
	     #event.connection.send
    
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
    	
      	# Existing DHCPD server on network  -- client -> server
        msg_dhcp.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        event.connection.send(msg_dhcp)
        
        # DHCP Server -> Client
        msg_dhcp.match.tp_src = pkt.dhcp.SERVER_PORT
      	msg_dhcp.match.tp_dst = pkt.dhcp.CLIENT_PORT
        
        event.connection.send(msg_dhcp)
        
        # DNS - should this be only done at first packet in so doesn't need to be flood?
	    msg_dns = of.ofp_flow_mod()
    	msg_dns.match.dl_type = pkt.ethernet.IP_TYPE
      	msg_dns.match.nw_proto = pkt.ipv4.UDP_PROTOCOL
      	msg_dns.match.tp_src = pkt.dns.SERVER_PORT
      	msg_dhcp.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      	
      	event.connection.send(msg_dns)
      	msg_dns.match.tp_dst = pkt.dns.SERVER_PORT
      	event.connection.send(msg_dns)
	     	
        # Put in a rule to bypass all all V6 Traffic 
        msg_v6 = of.ofp_flow_mod()
        msg_v6.match.dl_type = pkt.ethernet.IPV6_TYPE
        msg_v6.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
        event.connection.send(msg_v6)
        

        # Drop all other traffic
        msg_drop= of.ofp_flow_mod()
    	msg_drop.actions.append(of.ofp_action_output(port = of.OFPP_DROP)
    	event.connection.send(drop)
    	
		return 
		
		
	def get_web_portal ():	
	  # Get Web Portal IP
      webportal_ip = '128.208.125.59'	 
      return webportal_ip
      
        
      
    
    
"""    
    def authentication
  	  # Set rules for authentication and then wait for auth
  	  auth_channel = core.MessengerNexus.get_channel("auth")  
      return 
"""


def launch (transparent=False, hold_down=_flood_delay):
  """
  Starts the resonance process 

  """ 
  core.registerNew(resonance, str_to_bool(transparent))
