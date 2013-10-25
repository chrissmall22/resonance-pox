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
from pox.lib.util import str_to_bool
from pox.lib.addresses import IPAddr, EthAddr

#import mysql.connector

log = core.getLogger()


class resonance (object):
  """
  Waits for OpenFlow switches to connect.
  """
  def __init__ (self, transparent):
    core.openflow.addListeners(self)
    self.transparent = transparent
    
    # Cache of authorized MAC DB -- includes userid and state associated with MAC
    self.macDB = {}
    HTTP_PORT = 80
    HTTPS_PORT = 443
    
  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    push_default_rules(event)
    #add_trusted_hosts(event)


  def _handle_ConnectionDown (self, event):
    log.debug("Connection %s" % (event.connection,))
  
  
  def _handle_PacketIn (self, event):
    packet = event.parsed
    
    log.debug("PacketIn Connection %s" % (event.connection,))

    # Check if in the known MAC addresses, if so move host to last known state
    state = self.macDB.get(packet.src)
    
    
    log.debug("Packet In, mac=%s DB state=%s",
              packet.src, state)
    
    
    # Check what state the host was in

    # UNKNOWN state,push rules to move to registration state
    if state == None:

      # Push rules for Registration
      # Add trusted Devices 

      # Captive Portal
      if packet.src == EthAddr('1a:33:d5:0b:e2:45'):
        msg_portal = of.ofp_flow_mod()
        msg_portal.match.dl_dst = packet.src
        msg_portal.actions.append(of.ofp_action_output(port = event.port))
        event.connection.send(msg_portal)

      """
      msg_dns2 = of.ofp_flow_mod()
      msg_dns2.match.dl_type = pkt.ethernet.IP_TYPE
      msg_dns2.match.nw_proto = pkt.ipv4.UDP_PROTOCOL
      msg_dns2.match.tp_dst = pkt.dns.SERVER_PORT
      msg_dns2.actions.append(of.ofp_action_output(port = event.port))
      event.connection.send(msg_dns2)


      # Web redirect 
      portal_ip = get_portal_ip()
      msg_web_redirect = of.ofp_flow_mod()
      msg_web_redirect.match.dl_type = pkt.ethernet.IP_TYPE
      msg_web_redirect.match.nw_proto = pkt.ipv4.TCP_PROTOCOL
      msg_web_redirect.match.tp_dst = 80
      msg_web_redirect.actions.append(of.ofp_action_nw_addr.set_dst(IPAddr(portal_ip)))
      event.connection.send(msg_web_redirect)  
      """

      # If sending to port 80 redirect to portal

      # Allow return web traffic to client
      msg_web = of.ofp_flow_mod()
      msg_web.match.dl_type = pkt.ethernet.IP_TYPE
      msg_web.match.nw_proto = pkt.ipv4.TCP_PROTOCOL
      msg_web.match.tp_src = 80
      msg_web.match.dl_src = packet.src
      msg_web.actions.append(of.ofp_action_output(port = event.port))
      event.connection.send(msg_web)

      

      # Drop 
      #msg_drop = of.ofp_flow_mod()
      #msg_drop.match.dl_src = packet.src
      #event.connection.send(msg_drop)

      
      #portal_ip = get_portal_ip()
      #msg_web = of.ofp_flow_mod()
      #msg_web.match.dl_type = pkt.ethernet.IP_TYPE
      #msg_web.match.nw_proto = pkt.ipv4.TCP_PROTOCOL
      #msg_web.actions.append(of.ofp_action_output(nw_addr.set_dst(portal_ip)))
      #event.connection.send(msg_web)	
				
    if state == 'OPER':
      # Flush precious rules for this MAC
      # Push in normal rule	
      msg_oper = of.ofp_flow_mod() 
      msg_oper.match.dl_src = packet.src
      msg_oper.actions.append(of.ofp_action_output(port = event.port))
      event.connection.send(msg_oper)

def push_default_rules (event):

   # Clear all existing rules
   msg_flush = of.ofp_flow_mod(command=of.OFPFC_DELETE)
   event.connection.send(msg_flush)

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

   # Put in a rule to bypass all all V6 Traffic 
   #msg_v6 = of.ofp_flow_mod()
   #msg_v6.match.dl_type = pkt.ethernet.IPV6_TYPE
   #msg_v6.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
   #event.connection.send(msg_v6)
        
   # Drop all other traffic
   #msg_drop = of.ofp_flow_mod()
   #event.connection.send(msg_drop)
    	
   return 

"""
def add_trusted_hosts (event):
   # Allow tusted macs to send/recieve packets 
   #
   # Could be real mac of portal or gateway MAC 
   msg_portal = of.ofp_flow_mod()
   msg_portal.match.dl_dst = EthAddr('1a:33:d5:0b:e2:45') 
   msg_portal.actions.append(of.ofp_action_output(port = of.OFPP_NORMAL))
   event.connection.send(msg_portal)
"""

		
		
def get_portal_ip ():	
  # Get Web Portal IP
  webportal_ip = '10.200.0.3'	 
  return webportal_ip
      
        
    

def launch (transparent=False):
  """
  Starts the resonance process 

  """ 
  core.registerNew(resonance, str_to_bool(transparent))
