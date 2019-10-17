from pywinusb import hid
import time
import sys


def readData(data):
    print("[DATA]:"+str(data))
    return None

def getHIDlist():
    hid_list=hid.find_all_hid_devices()
    if len(hid_list) == 0:
        print('NA')
        return
    for i in range(len(hid_list)):
        print("[FINDHID]{};VID:{},PID:{},vendor:{},product:{}".format(i,
        hex(hid_list[i].vendor_id),hex(hid_list[i].product_id),
        hid_list[i].vendor_name,hid_list[i].product_name))


def getInfo(vid=0x45e, pid=0x09ad, index=3, cmd=[0x24,0x01], usage_page=0xff07, usage=0x0212):
    #hid_list=hid.find_all_hid_devices()
    try:
        devices = hid.HidDeviceFilter(vendor_id=vid,product_id=pid).get_devices()
        for hid_dev in devices:
            hid_dev.open()
            if (usage_page != hid_dev.hid_caps.usage_page) or (usage != hid_dev.hid_caps.usage):
                hid_dev.close()
                continue
            else:
                hid_dev.set_raw_data_handler(readData)
                time.sleep(0.1)
                reports = hid_dev.find_any_reports()
                print("report"+str(reports))
                if reports is not None and len(reports) > 0:
                    buffer = [0x00] * hid_dev.hid_caps.feature_report_byte_length
                    for i in range(len(cmd)):
                        if i < hid_dev.hid_caps.feature_report_byte_length:
                            buffer[i] = cmd[i]
                        else:
                            break

                    hid_dev.send_feature_report(buffer)
                    #report.send()
                    time.sleep(0.5)

                else:
                    print("Fail to find any reports.")

                hid_dev.close()
                #print('finish')
                return
        else:
            print('Fail to find any device.')

    except Exception as ex:
        print("ERR:" + str(ex))


#getHIDlist()
#getInfo()


def main():
  cmd_list=sys.argv
  if len(cmd_list) == 1:
    print("ERR:no request")
    return
  if cmd_list[1].upper() == "SCAN":
    getHIDlist()
  elif cmd_list[1].upper().find("SEND") != -1:
    print(cmd_list[1])
    #SEND:VID=0x45e;PID=0X955;INDEX=3;CMD=24,01
    usage_page = 0xff07
    usage = 0x0212
    try:
        r_list = cmd_list[1].split(':')
        arg_list = r_list[1].split(';')
        v_id = int(arg_list[0].split('=')[1], 16)
        p_id = int(arg_list[1].split('=')[1], 16)
        hid_index = int(arg_list[2].split('=')[1])
        cmd_raw = arg_list[3].split('=')
        cmd_send = []
        for item in cmd_raw[1].split(','):
            cmd_send.append(int(item, 16))
        if len(arg_list) > 4:
            arr = str(arg_list[4]).split('=')
            if len(arr) > 1:
                usage_page = int(arr[1], 16)
        if len(arg_list) > 5:
            arr = str(arg_list[5]).split('=')
            if len(arr) > 1:
                usage = int(arr[1], 16)

        #print(v_id)
        #print(p_id)
        #print(hid_index)
        #print(cmd_send)
        getInfo(vid=v_id,pid=p_id,index=hid_index,cmd=cmd_send, usage_page=usage_page, usage=usage)
    except Exception as ex:
        print("ERR:"+str(ex))

  elif cmd_list[1].upper() == "HELP":
    print("SCAN      get hid list")
    print("SEND:VID=0x45e;PID=0X9ad;INDEX=3;CMD=24,01;hid device execute cmds")
    print("SEND:VID=0x45e;PID=0X9ad;INDEX=3;CMD=24,01;usagePage=ff07;page=0212;hid device execute cmds")
  else:
    print("ERR:bad request:"+cmd_list[1])

if __name__ == '__main__':
    #sys.argv = ['', 'SEND:VID=0x45e;PID=0X9ad;INDEX=3;CMD=24,34;usagePage=ff07;page=0212']
    #sys.argv = ['', 'SEND:VID=0x45e;PID=0X9ad;INDEX=3;CMD=24,34;hid device execute cmds']
    main()
