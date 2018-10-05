#! python2
# -*- coding: utf-8 -*-

from os.path import join, realpath

Import("env")

define = "MODBUS_INTERFACE"
interfaces = {
	"MB_SERIAL"   : ("Serial"      , "MB_SERIAL"),
	"MB_ETHERNET" : ("IP"          , "MB_ETHERNET"),
	"MB_ENC28J60" : ("IP_ENC28J60" , "MB_ENC28J60"),
	"MB_ESP8266AT": ("IP_ESP8266AT", "MB_ESP8266AT")
}

for item in env.get("CPPDEFINES", []):
    if isinstance(item, tuple) and item[0] == define:
		ifc = item[1]
		try:
			ifc, ifcid = interfaces[ifc]
		except KeyError:
			print("Selected Unsupported interface {}. Please select one of {}.".format(ifc, interfaces.keys()))
			exit(-1)
		prefix = "Modbus"
		ifc = prefix + ifc
		env.Append(CPPPATH=[realpath(join("libraries", ifc))])
		flt = ["+<*>"]
		for v in interfaces.values():
			flt.append("{}<{}>".format('+' if ifcid == v[1] else '-', join("libraries", prefix + v[0])))
		env.Replace(SRC_FILTER=flt)
		# env.ProcessUnFlags("-D{}={}".format(*item))
		# env.Append(CPPDEFINES=(define, ifcid))
		break
