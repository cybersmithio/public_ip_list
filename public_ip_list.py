#!/usr/bin/python
# Written by: James Smith
# Version: 0.9
# Created: May 3, 2018
#
# Given an IP range, this script will
#
# Set these environment variables to log in:
#     SCHOST
#     SCUSERNAME
#     SCPASSWORD
#
#
# Requires the following:
#   pip install pysecuritycenter
#   pip install ipaddr
#   pip install netaddr

import ipaddress
import argparse

###############################################
# CODE BELOW HERE - NOTHING TO CHANGE BY USER #
###############################################



#Not the most efficient, but it works
def displayRemainingPublicIPs(DEBUG,iplist):
    cidrlist=[]
    publicips=[ipaddress.ip_network("0.0.0.0/0")]

    if iplist != "":
        if DEBUG:
            print("iplist:",iplist)

        for i in str(iplist).split(sep=","):
            if DEBUG:
                print("CIDR:",i.strip())
            #cidrlist.append(netaddr.iprange_to_cidrs(i))
            cidrlist.append(ipaddress.ip_network(i.strip(),strict=False))

    cidrlist.append(ipaddress.ip_network("10.0.0.0/8"))
    cidrlist.append(ipaddress.ip_network("192.168.0.0/16"))
    cidrlist.append(ipaddress.ip_network("172.16.0.0/12"))

    if DEBUG:
        print("\n\n")
    for i in cidrlist:
        if DEBUG:
            print("CIDR:",i)
        new=[]
        for j in publicips:
            if i.subnet_of(j):
                for k in j.address_exclude(i):
                    new.append(k)
            else:
                new.append(j)
        publicips=new

        #print("exclude:",publicips.address_exclude(i))
        #publicips=publicips.address_exclude(i)
        if DEBUG:
            print("Public IP addresses:")
        for j in publicips:
            if DEBUG:
                print(">>",str(j))
        if DEBUG:
            print("\n\n")

    print("Public IP addresses:")
    for j in publicips:
            print("  ",str(j))

    return()





######################
###
### Program start
###
######################
parser = argparse.ArgumentParser(description="Displays a list of all public IP addresses not covered in the IP ranges provided.")
parser.add_argument('--iplist',help="A list of subnets in CIDR, comma-separated, that should be excluding from the public IP list",nargs=1,action="store",default=[""])
parser.add_argument('--debug',help="Display a **LOT** of information",action="store_true")
args = parser.parse_args()

DEBUG=False

if args.debug:
    DEBUG=True

displayRemainingPublicIPs(DEBUG,args.iplist[0])

exit()