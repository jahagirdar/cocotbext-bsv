# bsv 


# install
`pip3 install cocotbext_bsv`

#Usage

```
from cocotbext.bsv import BsvBus,BsvDriver,BsvConfig

....
class Env:
   def __init__(self,dut):
	bsv_bus = BsvBus(from_prefix='...',dut=....)
	bsv_config = BsvConfig()
	bsv_config.<key>=<value>
	bsv_driver = bsvDriver(bsv_bus, bsv_config)
   async def xyz(self):
 	bsv_driver.write(address,byteArray)
 	rv =bsv_driver.read(address,numbytes)
	assert rv=byteArray, "Data mismatch at %X"%(address)

