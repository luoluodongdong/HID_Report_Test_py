from pywinusb import hid
import time

def readData(data):
  print(data)
  return None

def test():

  #hid_list=hid.find_all_hid_devices()
  hid_dev=hid.HidDeviceFilter(vendor_id=0x45e,product_id=0x0955).get_devices()[3]
  print(str(hid_dev.vendor_id))
  hid_dev.set_raw_data_handler(readData)
  

  try:
    hid_dev.open()
    time.sleep(0.1)
    report=hid_dev.find_any_reports()
    print("report"+str(report))

    buffer=[0x00]*64
    buffer[0]=0x24
    buffer[1]=0x01
    buffer[2]=0x00
    hid_dev.send_feature_report(buffer)
    #report.send()
    time.sleep(1)
    hid_dev.close()
  except Exception as ex:
    print("err:"+str(ex))


test()