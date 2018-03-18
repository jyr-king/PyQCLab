#
# **************************************************************************
#
# simple_rec_fifo.py                            (c) Spectrum GmbH , 11/2009
#
# **************************************************************************
#
# Example for all SpcMDrv based (M2i/M3i/M4i) analog acquisition cards. 
# Shows a simple FIFO mode example using only the few necessary commands
#  
# Feel free to use this source for own projects and modify it in any kind
#
# **************************************************************************
#

import sys

# import spectrum driver functions
from pyspcm import *

#
# **************************************************************************
# szTypeToName: doing name translation
# **************************************************************************
#

def szTypeToName (lCardType):
    sName = ''
    lVersion = (lCardType & TYP_VERSIONMASK)
    if (lCardType & TYP_SERIESMASK) == TYP_M2ISERIES:
        sName = 'M2i.%04x'%lVersion
    elif (lCardType & TYP_SERIESMASK) == TYP_M2IEXPSERIES:
        sName = 'M2i.%04x-Exp'%lVersion
    elif (lCardType & TYP_SERIESMASK) == TYP_M3ISERIES:
        sName = 'M3i.%04x'%lVersion
    elif (lCardType & TYP_SERIESMASK) == TYP_M3IEXPSERIES:
        sName = 'M3i.%04x-Exp'%lVersion
    elif (lCardType & TYP_SERIESMASK) == TYP_M4IEXPSERIES:
        sName = 'M4i.%04x-x8'%lVersion
    elif (lCardType & TYP_SERIESMASK) == TYP_M4XEXPSERIES:
        sName = 'M4x.%04x-x4'%lVersion
    else:
        sName = 'unknown type'
    return sName



#
# **************************************************************************
# main 
# **************************************************************************
#

szErrorTextBuffer = create_string_buffer (ERRORTEXTLEN)
dwError = uint32 ();
lStatus = int32 ()
lAvailUser = int32 ()
lPCPos = int32 ()
qwTotalMem = uint64 (0);
qwToTransfer = uint64 (MEGA_B(8));

# settings for the FIFO mode buffer handling
qwBufferSize = uint64 (MEGA_B(4));
lNotifySize = int32 (KILO_B(16));


# open card
hCard = spcm_hOpen (create_string_buffer (b'/dev/spcm0'))
if hCard == None:
    sys.stdout.write("no card found...\n")
    exit ()


# read type, function and sn and check for A/D card
lCardType = int32 (0)
spcm_dwGetParam_i32 (hCard, SPC_PCITYP, byref (lCardType))
lSerialNumber = int32 (0)
spcm_dwGetParam_i32 (hCard, SPC_PCISERIALNO, byref (lSerialNumber))
lFncType = int32 (0)
spcm_dwGetParam_i32 (hCard, SPC_FNCTYPE, byref (lFncType))

sCardName = szTypeToName (lCardType.value)
if lFncType.value == SPCM_TYPE_AI:
    sys.stdout.write("Found: {0} sn {1:05d}\n".format(sCardName,lSerialNumber.value))
else:
    sys.stdout.write("Card: {0} sn {1:05d} not supported by example\n".format(sCardName,lSerialNumber.value))
    exit () 


# do a simple standard setup
spcm_dwSetParam_i32 (hCard, SPC_CHENABLE,       1)                      # just 1 channel enabled
spcm_dwSetParam_i32 (hCard, SPC_PRETRIGGER,     1024)                   # 1k of pretrigger data at start of FIFO mode
spcm_dwSetParam_i32 (hCard, SPC_CARDMODE,       SPC_REC_FIFO_SINGLE)    # single FIFO mode
spcm_dwSetParam_i32 (hCard, SPC_TIMEOUT,        5000)                   # timeout 5 s
spcm_dwSetParam_i32 (hCard, SPC_TRIG_ORMASK,    SPC_TMASK_SOFTWARE)     # trigger set to software
spcm_dwSetParam_i32 (hCard, SPC_TRIG_ANDMASK,   0)                      # ...
spcm_dwSetParam_i32 (hCard, SPC_CLOCKMODE,      SPC_CM_INTPLL)          # clock mode internal PLL

# we try to set the samplerate to 100 kHz (M2i) or 20 MHz (M3i/M4i) on internal PLL, no clock output
if ((lCardType.value & TYP_SERIESMASK) == TYP_M2ISERIES) or ((lCardType.value & TYP_SERIESMASK) == TYP_M2IEXPSERIES):
    spcm_dwSetParam_i64 (hCard, SPC_SAMPLERATE, KILO(100))
else:
    spcm_dwSetParam_i64 (hCard, SPC_SAMPLERATE, MEGA(20))

spcm_dwSetParam_i32 (hCard, SPC_CLOCKOUT, 0)                            # no clock output


# define the data buffer
# we try to use continuous memory if available and big enough
pvBuffer = c_void_p ()
qwContBufLen = uint64 (0)
spcm_dwGetContBuf_i64 (hCard, SPCM_BUF_DATA, byref(pvBuffer), byref(qwContBufLen))
sys.stdout.write ("ContBuf length: {0:d}\n".format(qwContBufLen.value))
if qwContBufLen.value >= qwBufferSize.value:
    sys.stdout.write("Using continuous buffer\n")
else:
    pvBuffer = create_string_buffer (qwBufferSize.value)
    sys.stdout.write("Using buffer allocated by user program\n")
    

spcm_dwDefTransfer_i64 (hCard, SPCM_BUF_DATA, SPCM_DIR_CARDTOPC, lNotifySize, pvBuffer, uint64 (0), qwBufferSize)

# start everything
dwError = spcm_dwSetParam_i32 (hCard, SPC_M2CMD, M2CMD_CARD_START | M2CMD_CARD_ENABLETRIGGER | M2CMD_DATA_STARTDMA)


# check for error
if dwError != 0: # != ERR_OK
    spcm_dwGetErrorInfo_i32 (hCard, None, None, szErrorTextBuffer)
    sys.stdout.write("{0}\n".format(szErrorTextBuffer.value))
    spcm_vClose (hCard)
    exit ()

# run the FIFO mode and loop through the data
else:
    lMin = int (32767)  # normal python type
    lMax = int (-32768) # normal python type
    while qwTotalMem.value < qwToTransfer.value:
        dwError = spcm_dwSetParam_i32 (hCard, SPC_M2CMD, M2CMD_DATA_WAITDMA)
        if dwError != ERR_OK:
            if dwError == ERR_TIMEOUT:
                sys.stdout.write ("... Timeout\n")
            else:
                sys.stdout.write ("... Error: {0:d}\n".format(dwError))
                break;

        else:
            spcm_dwGetParam_i32 (hCard, SPC_M2STATUS,            byref (lStatus))
            spcm_dwGetParam_i32 (hCard, SPC_DATA_AVAIL_USER_LEN, byref (lAvailUser))
            spcm_dwGetParam_i32 (hCard, SPC_DATA_AVAIL_USER_POS, byref (lPCPos))

            if lAvailUser.value >= lNotifySize.value:
                qwTotalMem.value += lNotifySize.value
                sys.stdout.write ("Stat:{0:08x} Pos:{1:08x} Avail:{2:08x} Total:{3:.2f}MB/{4:.2f}MB\n".format(lStatus.value, lPCPos.value, lAvailUser.value, c_double (qwTotalMem.value).value / MEGA_B(1), c_double (qwToTransfer.value).value / MEGA_B(1)))

                # this is the point to do anything with the data
                # e.g. calculate minimum and maximum of the acquired data
                pnData = cast  (pvBuffer, ptr16) # cast to pointer to 16bit integer
                for i in range (0, lNotifySize.value - 1, 1):
                    if pnData[i] < lMin:
                        lMin = pnData[i]
                    if pnData[i] > lMax:
                        lMax = pnData[i]

                spcm_dwSetParam_i32 (hCard, SPC_DATA_AVAIL_CARD_LEN,  lNotifySize)

#            # check for escape = abort
#            if (bKbhit())
#                if (cGetch() == 27)
#                    break;


# send the stop command
dwError = spcm_dwSetParam_i32 (hCard, SPC_M2CMD, M2CMD_CARD_STOP | M2CMD_DATA_STOPDMA)

sys.stdout.write ("Finished...\n");
sys.stdout.write ("Minimum: {0:d}\n".format(lMin));
sys.stdout.write ("Maximum: {0:d}\n".format(lMax));


# clean up
spcm_vClose (hCard)


