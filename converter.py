#open source：please follow  GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
#Pleasw refer http://www.gnu.org/licenses/gpl.txt
#Data Record:
#Nov 22 Start Project, add Reg_write, Debug, Delay, Sycn Function
#Nov 23 add write file ,mode control, RxGain Funcation
#Nov 26 add TxGain, DataRecord, DCOC function
#DEC 18 fix some bugs
#JAN 29 Update some function
#=======================================================================


import os
import sys
import time

print('Version2.1, 2019-02-19 Modified')
print('===============================',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'===============================')
print('Reg_Write  Delay  Sync  RxGain  Reg_Read  Debug  ModeControl  TxGain  DCOC')
print('===================================================================================\n')
direct=input("Enter your Path: ")
content=os.listdir(direct)
total_files=1

if str(content).find('.CSV')==-1 and str(content).find('.csv')==-1:
    print('this path has no CSV files, Please Recheck')
    
else:
    if os.path.exists(direct+os.path.sep+'CSV to TPF'):
        print ('CSV to TPF Files Exist，Skip This Step')
    else:
        os.makedirs(direct+os.path.sep+'CSV to TPF')
    if os.path.exists(direct+os.path.sep+'CSV to TPF'+os.path.sep+'DataRecord.txt'):
        os.remove(direct+os.path.sep+'CSV to TPF'+os.path.sep+'DataRecord.txt')
    DataRecord = open(direct+os.path.sep+'CSV to TPF'+os.path.sep+'DataRecord.txt', 'a')
    print('===============================',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),'===============================',file=DataRecord)
    for content in content:
        if content.find('.csv')!=-1:
            print(total_files,content)
            NAME = content.rsplit('.',1)[0]
            f = open(direct+os.path.sep+'CSV to TPF'+os.path.sep+NAME+'.tpf', 'w')
            print(total_files,content,file=DataRecord)
            f.write('<module_file>\n'
                    '\t<module name="'+NAME+'">\n')
            with open(direct+os.path.sep+NAME+'.CSV') as file:
                total_files=total_files+1
                for line in file:
    #=======================================================================
                    if line[0]!=';' and line.find('Reg_Write',0,10)>=0:
                        cache=line[0:].split(',')
                        waddr=cache[1]
                        wdata=cache[2]
                        channel=cache[3][-1]
                        WADDR=waddr.upper().lstrip( )
                        WDATA=wdata.upper().lstrip( ).lstrip('0')
                        if WDATA=='':
                            WDATA='0'
                        count1=bin(int(waddr,16))
                        a1number=count1.count('1')
                        count2=bin(int(wdata,16))
                        b1number=count2.count('1')
                        total=a1number+b1number
                        if (total % 2) == 0:
                                c='1'
                        else:
                                c='0'
                        f.write('\t<frame name="SYNC'+channel+'" execution_type="Default" mask="" repeat="false">\n'
                                '\t</frame>\n'
                                '\t<frame name="LONG_WR'+channel+'" execution_type="Default" mask="" repeat="false">\n'
                                  '\t\t<field name="WADDR">\n'
                                    '\t\t\t<value hexValue="'+WADDR+'"/>\n'
                                  '\t\t</field>\n'
                                  '\t\t<field name="WDATA">\n'
                                    '\t\t\t<value hexValue="'+WDATA+'"/>\n'
                                  '\t\t</field>\n'
                                  '\t\t<field name="Parity">\n'
                                    '\t\t\t<value hexValue="'+c+'"/>\n'
                                  '\t\t</field>\n'
                                '\t</frame>\n')
    #========================================================================   
                    elif line[0]!=';' and line.find('Delay')!=-1:
                        cache=line[0:].split(',')
                        time=cache[2]
                        if line[6]=='u':
                            wait=int(time.strip(' '))/1000000
                        if line[6]=='n':
                            wait=int(time.strip(' '))/1000000000
                        str_wait="%.8f"%(wait)
                        str_wait1=str_wait.rstrip('0')
                        f.write('\t<wait time_in_seconds="'+str_wait1+'"/>\n')
    #========================================================================
                    elif line[0]!=';' and line.find('Sync')!=-1:
                        cache=line[0:].split(',')
                        waddr=cache[1]
                        wdata=cache[2]
                        channel=cache[3][-1]
                        f.write('\t<frame name="SYNC'+channel+'" execution_type="Default" mask="" repeat="false"> \n'
                                '\t</frame>\n')
    #========================================================================
                    elif line[0]!=';' and line.find('RxGain')!=-1:
                        RxGain='0'
                        cache=line[0:].split(',')
                        channel=cache[3][-1]
                        cache_short=line.split(',')
                        s=(cache_short[2].lstrip().rstrip().split(' '))
                        seq_Rx=RxGain+bin(int(s[0],16))[2:].zfill(1)+bin(int(s[1],16))[2:].zfill(3)+bin(int(s[2],16))[2:].zfill(3)+bin(int(s[3],16))[2:].zfill(4)+bin(int(s[4],16))[2:].zfill(4)
                        add_zero_Rx ="%-31s" %seq_Rx
                        trans1=add_zero_Rx.replace(' ','0')
                        trans2=hex(int(trans1,2))[2:].upper()
                        shortnumber=seq_Rx.count('1')
                        if (shortnumber % 2) == 0:
                                C='1'
                        else:
                                C='0'
                        print('\tRxGain:\t\t',line,end = '',file=DataRecord)
                        f.write('\t<frame name="SHORT_WR'+channel+'" execution_type="Default" mask="" repeat="false">\n'
                                    '\t\t<field name="SMSG">\n'
                                        '\t\t\t<value hexValue="'+trans2+'"/>\n'
                                    '\t\t</field>\n'
                                    '\t\t<field name="Parity">\n'
                                        '\t\t\t<value hexValue="'+C+'"/>\n'
                                    '\t\t</field>\n'
                                '\t</frame>\n')
    #========================================================================
                    elif line[0]!=';' and line.find('Reg_Read',0,10)>=0:
                        cache=line[0:].split(',')
                        channel=cache[3][-1]
                        waddr=cache[1]
                        wdata=cache[2]
                        WADDR=waddr.upper().lstrip( )
                        WDATA=wdata.upper().lstrip( ).lstrip('0')
                        if WDATA=='':
                            WDATA='0'
                        f.write('\t<frame name="SYNC'+channel+'" execution_type="Default" mask="" repeat="false">\n'
                                '\t</frame>\n'
                                '\t<frame name="MASTER_RD'+channel+'" execution_type="CaptureInCMEM" mask="" repeat="false"> \n'
                                    '\t\t<field name="RADDR">\n'
                                        '\t\t\t<value hexValue="'+WADDR+'"/>\n'
                                    '\t\t</field>\n'
                                    '\t\t<field name="Parity">\n'
                                        '\t\t\t<value hexValue="'+WDATA+'"/>\n'
                                    '\t\t</field>\n'
                                '\t</frame>\n'
                                )
    #========================================================================  
                    elif line[0]!=';' and line.find('Debug')!=-1:
                        Debug='111'
                        cache=line[0:].split(',')
                        channel=cache[3][-1]
                        cache_short=line.split(',')
                        s=(cache_short[2].lstrip().split(' '))
                        seq=Debug+bin(int(s[0],16))[2:].zfill(4)+bin(int(s[1],16))[2:].zfill(2)+bin(int(s[2],16))[2:].zfill(1)+bin(int(s[3],16))[2:].zfill(1)
                        add_zero ="%-31s" %seq
                        trans1=add_zero.replace(' ','0')
                        trans2=hex(int(trans1,2))[2:].upper()
                        shortnumber=seq.count('1')
                        if (shortnumber % 2) == 0:
                                C='1'
                        else:
                                C='0'
                        print('\tDebug:\t\t',line,end = '',file=DataRecord)
                        f.write('\t<frame name="SHORT_WR'+channel+'" execution_type="Default" mask="" repeat="false">\n'
                                    '\t\t<field name="SMSG">\n'
                                        '\t\t\t<value hexValue="'+trans2+'"/>\n'
                                    '\t\t</field>\n'
                                    '\t\t<field name="Parity">\n'
                                        '\t\t\t<value hexValue="'+C+'"/>\n'
                                    '\t\t</field>\n'
                                '\t</frame>\n')
    #========================================================================
                    elif line[0]!=';' and line.find('ModeControl')!=-1:
                        code='110'
                        cache=line[0:].split(',')
                        channel=cache[3][-1]
                        cache_short=line.split(',')
                        s=(cache_short[2].lstrip().split(' '))
                        seq=code+bin(int(s[0],16))[2:].zfill(1)+bin(int(s[1],16))[2:].zfill(1)+bin(int(s[2],16))[2:].zfill(1)+bin(int(s[3],16))[2:].zfill(3)+ bin(int(s[4],16))[2:].zfill(3)
                        add_zero ="%-31s" %seq
                        trans1=add_zero.replace(' ','0')
                        trans2=hex(int(trans1,2))[2:].upper()
                        shortnumber=seq.count('1')
                        if (shortnumber % 2) == 0:
                                C='1'
                        else:
                                C='0'
                        print('\tModeControl:\t',line,end = '',file=DataRecord)
                        f.write('\t<frame name="SHORT_WR'+channel+'" execution_type="Default" mask="" repeat="false">\n'
                                    '\t\t<field name="SMSG">\n'
                                        '\t\t\t<value hexValue="'+trans2+'"/>\n'
                                    '\t\t</field>\n'
                                    '\t\t<field name="Parity">\n'
                                        '\t\t\t<value hexValue="'+C+'"/>\n'
                                    '\t\t</field>\n'
                                '\t</frame>\n')
    #========================================================================
                    elif line[0]!=';' and line.find('TxGain')!=-1:
                        code='100'
                        cache=line[0:].split(',')
                        channel=cache[3][-1]
                        cache_short=line.split(',')
                        s=(cache_short[2].lstrip().split(' '))
                        seq=code+bin(int(s[0],16))[2:].zfill(1)+bin(int(s[1],16))[2:].zfill(5)+bin(int(s[2],16))[2:].zfill(8)+ bin(int(s[3],16))[2:].zfill(3)+bin(int(s[4],16))[2:].zfill(3)+bin(int(s[5],16))[2:].zfill(1)+bin(int(s[6],16))[2:].zfill(4)+bin(int(s[7],16))[2:].zfill(3)
                        add_zero ="%-31s" %seq
                        trans1=add_zero.replace(' ','0')
                        trans2=hex(int(trans1,2))[2:].upper()
                        shortnumber=seq.count('1')
                        if (shortnumber % 2) == 0:
                                C='1'
                        else:
                                C='0'
                        print('\tTxGain:\t\t',line,end = '',file=DataRecord)
                        f.write('\t<frame name="SHORT_WR'+channel+'" execution_type="Default" mask="" repeat="false">\n'
                                    '\t\t<field name="SMSG">\n'
                                        '\t\t\t<value hexValue="'+trans2+'"/>\n'
                                    '\t\t</field>\n'
                                    '\t\t<field name="Parity">\n'
                                        '\t\t\t<value hexValue="'+C+'"/>\n'
                                    '\t\t</field>\n'
                                '\t</frame>\n')
    #========================================================================
                    elif line[0]!=';' and line.find('DCOC')!=-1:
                        code='101'
                        cache=line[0:].split(',')
                        channel=cache[3][-1]
                        cache_short=line.split(',')
                        s=(cache_short[2].lstrip().split(' '))
                        seq=code+bin(int(s[0],16))[2:].zfill(2)+bin(int(s[1],16))[2:].zfill(2)+bin(int(s[2],16))[2:].zfill(8)+bin(int(s[3],16))[2:].zfill(8)
                        trans1=add_zero.replace(' ','0')
                        trans2=hex(int(trans1,2))[2:].upper()
                        shortnumber=seq.count('1')
                        if (shortnumber % 2) == 0:
                                C='1'
                        else:
                                C='0'
                        print('\tTxGain:\t\t',line,end = '',file=DataRecord)
                        f.write('\t<frame name="SHORT_WR'+channel+'" execution_type="Default" mask="" repeat="false">\n'
                                    '\t\t<field name="SMSG">\n'
                                        '\t\t\t<value hexValue="'+trans2+'"/>\n'
                                    '\t\t</field>\n'
                                    '\t\t<field name="Parity">\n'
                                        '\t\t\t<value hexValue="'+C+'"/>\n'
                                    '\t\t</field>\n'
                                '\t</frame>\n')
                    elif line[0]!=';' and line[0]!='' and line[0]!=',' and line[0]!='\n':
                        print (line)
                        print (line,end = '',file=DataRecord)
    #========================================================================
            f.write('\t</module>\n'
                '</module_file>\n')
            f.close()

    DataRecord.close()
    print('Total',total_files,'Files Finished!\nPlease check the DataRecord to see more details')

close=input("You Can Close the Window now")

