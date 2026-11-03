"""Bootstrap for Resolve"""
import sys, logging

try:
	import DaVinciResolveScript as bmd

except ImportError as e:
	print("Cannot find the Davinci Resolve API.  Please ensure Davinci Resolve Studio is installed and operational.", file=sys.stderr)
	sys.exit(1)

if __name__ == "__main__":

	from runtime_calculator import __main__

	__main__.main(bmd=bmd, resolve=bmd.scriptapp("resolve"), fusion=bmd.scriptapp("fusion"))

