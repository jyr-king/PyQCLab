# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 01:27:14 2015

@author: jyr
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 02 18:02:44 2015

@author: Xmon-SC05
"""
from ctypes import *
import os,sys
#%%
dict_errorcode={}
dict_errorcode['ApiSuccess'] = 512
dict_errorcode['ApiFailed'] = 513
dict_errorcode['ApiAccessDenied'] = 514
dict_errorcode['ApiDmaChannelUnavailable'] = 515
dict_errorcode['ApiDmaChannelInvalid'] = 516
dict_errorcode['ApiDmaChannelTypeError'] = 517
dict_errorcode['ApiDmaInProgress'] = 518
dict_errorcode['ApiDmaDone'] = 519
dict_errorcode['ApiDmaPaused'] = 520
dict_errorcode['ApiDmaNotPaused'] = 521
dict_errorcode['ApiDmaCommandInvalid'] = 522
dict_errorcode['ApiDmaManReady'] = 523
dict_errorcode['ApiDmaManNotReady'] = 524
dict_errorcode['ApiDmaInvalidChannelPriority'] = 525
dict_errorcode['ApiDmaManCorrupted'] = 526
dict_errorcode['ApiDmaInvalidElementIndex'] = 527
dict_errorcode['ApiDmaNoMoreElements'] = 528
dict_errorcode['ApiDmaSglInvalid'] = 529
dict_errorcode['ApiDmaSglQueueFull'] = 530
dict_errorcode['ApiNullParam'] = 531
dict_errorcode['ApiInvalidBusIndex'] = 532
dict_errorcode['ApiUnsupportedFunction'] = 533
dict_errorcode['ApiInvalidPciSpace'] = 534
dict_errorcode['ApiInvalidIopSpace'] = 535
dict_errorcode['ApiInvalidSize'] = 536
dict_errorcode['ApiInvalidAddress	'] = 537
dict_errorcode['ApiInvalidAccessType'] = 538
dict_errorcode['ApiInvalidIndex'] = 539
dict_errorcode['ApiMuNotReady'] = 540
dict_errorcode['ApiMuFifoEmpty'] = 541
dict_errorcode['ApiMuFifoFull'] = 542
dict_errorcode['ApiInvalidRegister'] = 543
dict_errorcode['ApiDoorbellClearFailed'] = 544
dict_errorcode['ApiInvalidUserPin	'] = 545
dict_errorcode['ApiInvalidUserState'] = 546
dict_errorcode['ApiEepromNotPresent'] = 547
dict_errorcode['ApiEepromTypeNotSupported'] = 548
dict_errorcode['ApiEepromBlank'] = 549
dict_errorcode['ApiConfigAccessFailed'] = 550
dict_errorcode['ApiInvalidDeviceInfo'] = 551
dict_errorcode['ApiNoActiveDriver	'] = 552
dict_errorcode['ApiInsufficientResources'] = 553
dict_errorcode['ApiObjectAlreadyAllocated'] = 554
dict_errorcode['ApiAlreadyInitialized'] = 555
dict_errorcode['ApiNotInitialized	'] = 556
dict_errorcode['ApiBadConfigRegEndianMode'] = 557
dict_errorcode['ApiInvalidPowerState'] = 558
dict_errorcode['ApiPowerDown'] = 559
dict_errorcode['ApiFlybyNotSupported'] = 560
dict_errorcode['ApiNotSupportThisChannel'] = 561
dict_errorcode['ApiNoAction'] = 562
dict_errorcode['ApiHSNotSupported	'] = 563
dict_errorcode['ApiVPDNotSupported'] = 564
dict_errorcode['ApiVpdNotEnabled'] = 565
dict_errorcode['ApiNoMoreCap'] = 566
dict_errorcode['ApiInvalidOffset'] = 567
dict_errorcode['ApiBadPinDirection'] = 568
dict_errorcode['ApiPciTimeout'] = 569
dict_errorcode['ApiDmaChannelClosed'] = 570
dict_errorcode['ApiDmaChannelError'] = 571
dict_errorcode['ApiInvalidHandle'] = 572
dict_errorcode['ApiBufferNotReady	'] = 573
dict_errorcode['ApiInvalidData'] = 574
dict_errorcode['ApiDoNothing'] = 575
dict_errorcode['ApiDmaSglBuildFailed'] = 576
dict_errorcode['ApiPMNotSupported	'] = 577
dict_errorcode['ApiInvalidDriverVersion '] = 578
dict_errorcode['ApiWaitTimeout'] = 579
dict_errorcode['ApiWaitCanceled'] = 580
dict_errorcode['ApiBufferTooSmall	'] = 581
dict_errorcode['ApiBufferOverflow	'] = 582
dict_errorcode['ApiInvalidBuffer'] = 583
dict_errorcode['ApiInvalidRecordsPerBuffer'] = 584
dict_errorcode['ApiDmaPending'] = 585
dict_errorcode['ApiLockAndProbePagesFailed'] = 586
dict_errorcode['ApiWaitAbandoned'] = 587
dict_errorcode['ApiWaitFailed'] = 588
dict_errorcode['ApiTransferComplete'] = 589
dict_errorcode['ApiPllNotLocked'] = 590
dict_errorcode['ApiNotSupportedInDualChannelMode'] = 591
dict_errorcode['ApiNotSupportedInQuadChannelMode'] = 592
dict_errorcode['ApiFileIoError'] = 593
dict_errorcode['ApiInvalidClockFrequency'] = 594
#%%
"""--------------------------------------------------------------------------
# Board types
--------------------------------------------------------------------------"""
dict_boardtype={}
dict_boardtype['ATS_NONE']= 0
dict_boardtype['ATS850']= 1
dict_boardtype['ATS310']= 2
dict_boardtype['ATS330']= 3
dict_boardtype['ATS855']= 4
dict_boardtype['ATS315']= 5
dict_boardtype['ATS335']= 6
dict_boardtype['ATS460']= 7
dict_boardtype['ATS860']= 8
dict_boardtype['ATS660']= 9
dict_boardtype['ATS665']= 10
dict_boardtype['ATS9462']= 11
dict_boardtype['ATS9434']= 12
dict_boardtype['ATS9870']= 13
dict_boardtype['ATS9350']= 14
dict_boardtype['ATS9325']= 15
dict_boardtype['ATS9440']= 16
dict_boardtype['ATS9410']= 17
dict_boardtype['ATS9351']= 18
dict_boardtype['ATS9310']= 19
dict_boardtype['ATS9461']= 20
dict_boardtype['ATS9850']= 21
dict_boardtype['ATS9625']= 22
dict_boardtype['ATG6500'] = 23
dict_boardtype['ATS9626']= 24
dict_boardtype['ATS9360'] = 25
dict_boardtype['ATS_LAST']= 26
#%%
def hex2dec(string_num):
    return int(string_num.upper(), 16)
#%%

 #Clock Control

# Clock sources
dict_clocksource={}
dict_clocksource['INT']  =	hex2dec('00000001')
dict_clocksource['EXT']  =	hex2dec('00000002')
dict_clocksource['FAST_EXT']    =	hex2dec('00000002')
dict_clocksource['MED_EXT']     =	hex2dec('00000003')
dict_clocksource['SLOW_EXT']    =	hex2dec('00000004')
dict_clocksource['EXT_AC']      =	hex2dec('00000005')
dict_clocksource['EXT_DC']      =	hex2dec('00000006')
dict_clocksource['EXT_10MHz_REF']  =	hex2dec('00000007')
dict_clocksource['INT_DIV5']       =	hex2dec('000000010')
dict_clocksource['MASTER']         =	hex2dec('000000011')

# Internal sample rates,内部时钟改成一个字典数据结构
dict_samplerate={}
dict_samplerate['1ksps']    =hex2dec('00000001')
dict_samplerate['2ksps']    =hex2dec('00000002')
dict_samplerate['5ksps']    =hex2dec('00000004')
dict_samplerate['10ksps']   =hex2dec('00000008')
dict_samplerate['20ksps']   =hex2dec('0000000A')
dict_samplerate['50ksps']   =hex2dec('0000000C')
dict_samplerate['100ksps']  =hex2dec('0000000E')
dict_samplerate['200ksps']  =hex2dec('00000010')
dict_samplerate['500ksps']  =hex2dec('00000012')
dict_samplerate['1msps']    =hex2dec('00000014')
dict_samplerate['2msps']    =hex2dec('00000018')
dict_samplerate['5msps']    =hex2dec('0000001A')
dict_samplerate['10msps']   =hex2dec('0000001C')
dict_samplerate['20msps']   =hex2dec('0000001E')
dict_samplerate['25msps']   =hex2dec('00000021')
dict_samplerate['50msps']   =hex2dec('00000022')
dict_samplerate['100msps']  =hex2dec('00000024')
dict_samplerate['125msps']  =hex2dec('00000025')
dict_samplerate['160msps']  =hex2dec('00000026')
dict_samplerate['180msps']  =hex2dec('00000027')
dict_samplerate['200msps']  =hex2dec('00000028')
dict_samplerate['250msps']  =hex2dec('0000002B')
dict_samplerate['400msps']  =hex2dec('0000002D')
dict_samplerate['500msps']  =hex2dec('00000030')
dict_samplerate['800msps']  =hex2dec('00000032')
dict_samplerate['1000msps'] =hex2dec('00000035')
dict_samplerate['1200msps'] =hex2dec('00000037')
dict_samplerate['1500msps'] =hex2dec('0000003A')
dict_samplerate['1600msps'] =hex2dec('0000003B')
dict_samplerate['1800msps'] =hex2dec('0000003D')
dict_samplerate['2000msps'] =hex2dec('0000003F')
dict_samplerate['1gsps']    =hex2dec('00000035')
dict_samplerate['2gsps']    =hex2dec('0000003F')
dict_samplerate['userdef']  =hex2dec('00000040')


# Clock edges
dict_clkedge={}
dict_clkedge['RISING']           =	hex2dec('00000000')
dict_clkedge['FALLING']          =	hex2dec('00000001')

# Decimation
#DECIMATE_BY_8               =   hex2dec('00000008')
#DECIMATE_BY_64              =   hex2dec('00000040')
#%%
"""--------------------------------------------------------------------------
# Input Control
#--------------------------------------------------------------------------"""

# Input channels
dict_channels={}
dict_channels['CH_ALL']                 =   hex2dec('00000000')
dict_channels['CHA']                   =   hex2dec('00000001')
dict_channels['CHB']                   =   hex2dec('00000002')
dict_channels['CHC']                   =   hex2dec('00000004')
dict_channels['CHD']                   =   hex2dec('00000008')
dict_channels['CHE']                   =   hex2dec('00000010')
dict_channels['CHF']                   =   hex2dec('00000012')
dict_channels['CHG']                   =   hex2dec('00000014')
dict_channels['CHH']                   =   hex2dec('00000018')

# Input ranges
dict_inputrange={}
#9360只有一个输入范围档400mV。其他输入范围值待加入其他板卡后再添加。
dict_inputrange['400mV']         =   hex2dec('00000007')


# Input impedances
dict_impedance={}
dict_impedance['1M_OHM']            =	hex2dec('00000001')
dict_impedance['50_OHM']            =	hex2dec('00000002')
dict_impedance['75_OHM']            =	hex2dec('00000004')
dict_impedance['300_OHM']          =	hex2dec('00000008')
dict_impedance['600_OHM']           =	hex2dec('0000000A')

# Input coupling
dict_coupling={} 
dict_coupling['AC']                 =   hex2dec('00000001')
dict_coupling['DC']                 =	hex2dec('00000002')

"""--------------------------------------------------------------------------
# Trigger Control
#--------------------------------------------------------------------------"""

# Trigger engines
TRIG_ENGINE_J               =	hex2dec('00000000')
TRIG_ENGINE_K               =	hex2dec('00000001')

# Trigger engine operations
dict_trigengop={}
dict_trigengop['J']            =   hex2dec('00000000')
dict_trigengop['K']            =	hex2dec('00000001')
dict_trigengop['J_OR_K']		=   hex2dec('00000002')
dict_trigengop['J_AND_K']		=   hex2dec('00000003')
dict_trigengop['J_XOR_K']		=   hex2dec('00000004')
dict_trigengop['J_AND_NOT_K']	=   hex2dec('00000005')
dict_trigengop['NOT_J_AND_K']	=   hex2dec('00000006')

# Trigger engine sources
dict_trigsource={}
dict_trigsource['TRIG_CHA']                 =   hex2dec('00000000')
dict_trigsource['TRIG_CHB']                 =   hex2dec('00000001')
dict_trigsource['TRIG_EXT']               =   hex2dec('00000002')
dict_trigsource['TRIG_DISABLE']                =   hex2dec('00000003')
dict_trigsource['TRIG_CHC']                 =   hex2dec('00000004')
dict_trigsource['TRIG_CHD']                 =   hex2dec('00000005')

# Trigger slopes
dict_trigslope={}
dict_trigslope['POS']      =   hex2dec('00000001')
dict_trigslope['NEG']      =   hex2dec('00000002')

# External trigger ranges
dict_couplerange={}
dict_couplerange['DIV5']                    =   hex2dec('00000000')
dict_couplerange['X1']                      =   hex2dec('00000001')
dict_couplerange['5V']                      =   hex2dec('00000000')
dict_couplerange['1V']                      =   hex2dec('00000001')
dict_couplerange['TTL']                     =   hex2dec('00000002')
dict_couplerange['2V5']                     =   hex2dec('00000003')

#--------------------------------------------------------------------------
# Auxiliary I/O and LED Control
#--------------------------------------------------------------------------

# AUX outputs
dict_auxmode={}
dict_auxmode['OUT_TRIGGER']             =	0
dict_auxmode['OUT_PACER']               =	2
dict_auxmode['OUT_BUSY']                =	4
dict_auxmode['OUT_CLOCK']               =	6
dict_auxmode['OUT_RESERVED']            =	8
dict_auxmode['OUT_CAPTURE_ALMOST_DONE']	=	10
dict_auxmode['OUT_AUXILIARY']			=	12
dict_auxmode['OUT_SERIAL_DATA']		=	14
dict_auxmode['OUT_TRIGGER_ENABLE']		=	16

# AUX inputs
dict_auxmode['IN_TRIGGER_ENABLE']		=	1
dict_auxmode['IN_DIGITAL_TRIGGER']		=	3
dict_auxmode['IN_GATE']				=	5
dict_auxmode['IN_CAPTURE_ON_DEMAND']	=	7
dict_auxmode['IN_RESET_TIMESTAMP']		=	9
dict_auxmode['IN_SLOW_EXTERNAL_CLOCK']	=	11
dict_auxmode['IN_AUXILIARY']			=	13
dict_auxmode['IN_SERIAL_DATA']		=	15
dict_auxmode['INPUT_AUXILIARY']		=	13
dict_auxmode['INPUT_SERIAL_DATA']		=	15

# LED states
LED_OFF                     =	hex2dec('00000000')
LED_ON                      =	hex2dec('00000001')

#--------------------------------------------------------------------------
# Get/Set Parameters
#--------------------------------------------------------------------------

NUMBER_OF_RECORDS           =   hex2dec('10000001')
PRETRIGGER_AMOUNT           =   hex2dec('10000002')
RECORD_LENGTH               =   hex2dec('10000003')
TRIGGER_ENGINE              =   hex2dec('10000004')
TRIGGER_DELAY               =   hex2dec('10000005')
TRIGGER_TIMEOUT             =   hex2dec('10000006')
SAMPLE_RATE                 =   hex2dec('10000007')
CONFIGURATION_MODE          =   hex2dec('10000008') 
DATA_WIDTH                  =   hex2dec('10000009') 
SAMPLE_SIZE                 =   DATA_WIDTH
AUTO_CALIBRATE              =   hex2dec('1000000A')
TRIGGER_XXXXX               =   hex2dec('1000000B')
CLOCK_SOURCE                =   hex2dec('1000000C')
CLOCK_SLOPE                 =   hex2dec('1000000D')
IMPEDANCE                   =   hex2dec('1000000E')
INPUT_RANGE                 =   hex2dec('1000000F')
COUPLING                    =   hex2dec('10000010')
MAX_TIMEOUTS_ALLOWED        =   hex2dec('10000011')
ATS_OPERATING_MODE          =   hex2dec('10000012') 
CLOCK_DECIMATION_EXTERNAL   =   hex2dec('10000013')
LED_CONTROL                 =   hex2dec('10000014')
ATTENUATOR_RELAY            =   hex2dec('10000018')
EXT_TRIGGER_COUPLING        =   hex2dec('1000001A')
EXT_TRIGGER_ATTENUATOR_RELAY    =  hex2dec('1000001C')
TRIGGER_ENGINE_SOURCE       =   hex2dec('1000001E')
TRIGGER_ENGINE_SLOPE        =   hex2dec('10000020')
SEND_DAC_VALUE              =   hex2dec('10000021')
SLEEP_DEVICE                =   hex2dec('10000022')
GET_DAC_VALUE               =   hex2dec('10000023')
GET_SERIAL_NUMBER           =   hex2dec('10000024')
GET_FIRST_CAL_DATE          =   hex2dec('10000025')
GET_LATEST_CAL_DATE         =   hex2dec('10000026')
GET_LATEST_TEST_DATE        =   hex2dec('10000027')
SEND_RELAY_VALUE            =   hex2dec('10000028')
GET_LATEST_CAL_DATE_MONTH   =   hex2dec('1000002D')
GET_LATEST_CAL_DATE_DAY     =   hex2dec('1000002E')
GET_LATEST_CAL_DATE_YEAR    =   hex2dec('1000002F')
GET_PCIE_LINK_SPEED         =   hex2dec('10000030')
GET_PCIE_LINK_WIDTH         =   hex2dec('10000031')
SETGET_ASYNC_BUFFCOUNT      =   hex2dec('10000040')
SET_DATA_FORMAT             =   hex2dec('10000041')
GET_DATA_FORMAT             =   hex2dec('10000042')
DATA_FORMAT_UNSIGNED        =   0
DATA_FORMAT_SIGNED          =   1
SET_SINGLE_CHANNEL_MODE     =   hex2dec('10000043')
MEMORY_SIZE                 =   hex2dec('1000002A')
BOARD_TYPE                  =   hex2dec('1000002B')
ASOPC_TYPE                  =   hex2dec('1000002C')
GET_BOARD_OPTIONS_LOW       =   hex2dec('10000037')
GET_BOARD_OPTIONS_HIGH      =   hex2dec('10000038')
OPTION_STREAMING_DMA        =   int(2**0)
OPTION_AVERAGE_INPUT        =   int(2**1)
OPTION_EXTERNAL_CLOCK       =   int(2**1)
OPTION_DUAL_PORT_MEMORY 	=   int(2**2)
OPTION_180MHZ_OSCILLATOR    =   int(2**3)
OPTION_LVTTL_EXT_CLOCK      =   int(2**4)
OPTION_SW_SPI				=	int(2**5)
OPTION_ALT_INPUT_RANGES		= 	int(2**6)
OPTION_VARIABLE_RATE_10MHZ_PLL	= 	int(2**7)

TRANSFER_OFFET              =   hex2dec('10000030')
TRANSFER_LENGTH             =   hex2dec('10000031')
TRANSFER_RECORD_OFFSET      =   hex2dec('10000032')
TRANSFER_NUM_OF_RECORDS     =   hex2dec('10000033')
TRANSFER_MAPPING_RATIO      =   hex2dec('10000034')
TRIGGER_ADDRESS_AND_TIMESTAMP = hex2dec('10000035')
MASTER_SLAVE_INDEPENDENT    =   hex2dec('10000036')
TRIGGERED                   =   hex2dec('10000040')
BUSY                        =   hex2dec('10000041')
WHO_TRIGGERED               =   hex2dec('10000042')
SET_DATA_FORMAT				=   hex2dec('10000041')
GET_DATA_FORMAT				=   hex2dec('10000042')
DATA_FORMAT_UNSIGNED		=   0
DATA_FORMAT_SIGNED			=   1
SET_SINGLE_CHANNEL_MODE		=   hex2dec('10000043')
GET_SAMPLES_PER_TIMESTAMP_CLOCK	=   hex2dec('10000044')
GET_RECORDS_CAPTURED		=   hex2dec('10000045')
GET_MAX_PRETRIGGER_SAMPLES	=   hex2dec('10000046')
SET_ADC_MODE				=   hex2dec('10000047')
ECC_MODE					=   hex2dec('10000048')
ECC_DISABLE					=   0
ECC_ENABLE					=   1
GET_AUX_INPUT_LEVEL			=   hex2dec('10000049')
AUX_INPUT_LOW				=   0
AUX_INPUT_HIGH				=   1
GET_ASYNC_BUFFERS_PENDING   =   hex2dec('10000050')
GET_ASYNC_BUFFERS_PENDING_FULL =    hex2dec('10000051')
GET_ASYNC_BUFFERS_PENDING_EMPTY =   hex2dec('10000052')
ACF_SAMPLES_PER_RECORD      =   hex2dec('10000060')
ACF_RECORDS_TO_AVERAGE      =   hex2dec('10000061')
EXT_TRIGGER_IMPEDANCE		=   hex2dec('10000065')
EXT_TRIG_50_OHMS			= 	0
EXT_TRIG_300_OHMS			= 	1
GET_CHANNELS_PER_BOARD 		= 	hex2dec('10000070')
GET_CPF_DEVICE 				= 	hex2dec('10000071')
CPF_DEVICE_UNKNOWN 			= 	0
CPF_DEVICE_EP3SL50 			= 	1
CPF_DEVICE_EP3SE260 		= 	2
PACK_MODE 					= 	hex2dec('10000072')
PACK_DEFAULT 				= 	0
PACK_8_BITS_PER_SAMPLE 		= 	1
GET_FPGA_TEMPERATURE		=	hex2dec('10000080')

# Master/Slave Configuration
BOARD_IS_INDEPENDENT        =   hex2dec('00000000')
BOARD_IS_MASTER             =	hex2dec('00000001')
BOARD_IS_SLAVE              =	hex2dec('00000002')
BOARD_IS_LAST_SLAVE         =	hex2dec('00000003')

# Attenuator Relay
AR_X1                       =   hex2dec('00000000')
AR_DIV40                    =   hex2dec('00000001')

# Device Sleep state
dict_devicestate={
    'POWER_OFF':hex2dec('00000000'),
    'POWER_ON':hex2dec('00000001')
    }
#POWER_OFF                   =   hex2dec('00000000')
#POWER_ON                    =   hex2dec('00000001')

# Software Events control
SW_EVENTS_OFF               =   hex2dec('00000000')
SW_EVENTS_ON                =   hex2dec('00000001')

# TimeStamp Value Reset Control
TIMESTAMP_RESET_FIRSTTIME_ONLY	= hex2dec('00000000')
TIMESTAMP_RESET_ALWAYS			= hex2dec('00000001')

# DAC Names used by API AlazarDACSettingAdjust 
#ATS460_DAC_A_GAIN			=   hex2dec('00000001')
#ATS460_DAC_A_OFFSET			=   hex2dec('00000002')
#ATS460_DAC_A_POSITION		=   hex2dec('00000003')
#ATS460_DAC_B_GAIN			=   hex2dec('00000009')
#ATS460_DAC_B_OFFSET			=   hex2dec('0000000A')
#ATS460_DAC_B_POSITION		=   hex2dec('0000000B')
#ATS460_DAC_EXTERNAL_CLK_REF	=   hex2dec('00000007')

# DAC Names Specific to the ATS660
#ATS660_DAC_A_GAIN			=   hex2dec('00000001')
#ATS660_DAC_A_OFFSET			=   hex2dec('00000002')
#ATS660_DAC_A_POSITION		=   hex2dec('00000003')
#ATS660_DAC_B_GAIN			=   hex2dec('00000009')
#ATS660_DAC_B_OFFSET			=   hex2dec('0000000A')
#ATS660_DAC_B_POSITION		=   hex2dec('0000000B')
#ATS660_DAC_EXTERNAL_CLK_REF	=   hex2dec('00000007')

# DAC Names Specific to the ATS665
#ATS665_DAC_A_GAIN			=   hex2dec('00000001')
#ATS665_DAC_A_OFFSET			=   hex2dec('00000002')
#ATS665_DAC_A_POSITION		=   hex2dec('00000003')
#ATS665_DAC_B_GAIN			=   hex2dec('00000009')
#ATS665_DAC_B_OFFSET			=   hex2dec('0000000A')
#ATS665_DAC_B_POSITION		=   hex2dec('0000000B')
#ATS665_DAC_EXTERNAL_CLK_REF	=   hex2dec('00000007')

# Error return values
SETDAC_INVALID_SETGET       = 660
SETDAC_INVALID_CHANNEL      = 661
SETDAC_INVALID_DACNAME      = 662
SETDAC_INVALID_COUPLING     = 663
SETDAC_INVALID_RANGE        = 664
SETDAC_INVALID_IMPEDANCE    = 665
SETDAC_BAD_GET_PTR          = 667
SETDAC_INVALID_BOARDTYPE    = 668

# Constants to be used in the Application when dealing with Custom FPGAs
FPGA_GETFIRST               =   hex2dec('FFFFFFFF')
FPGA_GETNEXT                =   hex2dec('FFFFFFFE')
FPGA_GETLAST                =   hex2dec('FFFFFFFC')

#--------------------------------------------------------------------------
# AutoDMA Control 
#--------------------------------------------------------------------------

# AutoDMA flags 
ADMA_EXTERNAL_STARTCAPTURE  =   hex2dec('00000001')
ADMA_ENABLE_RECORD_HEADERS  =   hex2dec('00000008')
ADMA_SINGLE_DMA_CHANNEL     =   hex2dec('00000010')
ADMA_ALLOC_BUFFERS          =   hex2dec('00000020')
ADMA_TRADITIONAL_MODE       =   hex2dec('00000000')
ADMA_CONTINUOUS_MODE        =   hex2dec('00000100')
ADMA_NPT                    =   hex2dec('00000200')
ADMA_TRIGGERED_STREAMING    =   hex2dec('00000400')
ADMA_FIFO_ONLY_STREAMING    =   hex2dec('00000800')
ADMA_INTERLEAVE_SAMPLES     =   hex2dec('00001000')
ADMA_GET_PROCESSED_DATA     =   hex2dec('00002000')

# AutoDMA header constants
ADMA_CLOCKSOURCE            =   hex2dec('00000001')
ADMA_CLOCKEDGE              =   hex2dec('00000002')
ADMA_SAMPLERATE             =   hex2dec('00000003')
ADMA_INPUTRANGE             =   hex2dec('00000004')
ADMA_INPUTCOUPLING          =   hex2dec('00000005')
ADMA_IMPUTIMPEDENCE         =   hex2dec('00000006')
ADMA_EXTTRIGGERED           =   hex2dec('00000007')
ADMA_CHA_TRIGGERED          =   hex2dec('00000008')
ADMA_CHB_TRIGGERED          =   hex2dec('00000009')
ADMA_TIMEOUT                =   hex2dec('0000000A')
ADMA_THISCHANTRIGGERED      =   hex2dec('0000000B')
ADMA_SERIALNUMBER           =   hex2dec('0000000C')
ADMA_SYSTEMNUMBER           =   hex2dec('0000000D')
ADMA_BOARDNUMBER            =   hex2dec('0000000E')
ADMA_WHICHCHANNEL           =   hex2dec('0000000F')
ADMA_SAMPLERESOLUTION       =   hex2dec('00000010')
ADMA_DATAFORMAT             =   hex2dec('00000011')

#--------------------------------------------------------------------------
# AlazarSetClockSwitchOver
#--------------------------------------------------------------------------

CSO_DUMMY_CLOCK_DISABLE				= 0
CSO_DUMMY_CLOCK_TIMER				= 1
CSO_DUMMY_CLOCK_EXT_TRIGGER			= 2
CSO_DUMMY_CLOCK_TIMER_ON_TIMER_OFF	= 3

#--------------------------------------------------------------------------
# User-programmable FPGA
#--------------------------------------------------------------------------

# AlazarCoprocessorDownload
CPF_OPTION_DMA_DOWNLOAD	 		= 1

# User-programmable FPGA device types
CPF_DEVICE_UNKNOWN				= 0
CPF_DEVICE_EP3SL50				= 1
CPF_DEVICE_EP3SE260				= 2

# Framework defined registers
CPF_REG_SIGNATURE				= 0
CPF_REG_REVISION				= 1
CPF_REG_VERSION					= 2
CPF_REG_STATUS					= 3

#--------------------------------------------------------------------------
# AlazarSetExternalTriggerOperationForScanning 
#--------------------------------------------------------------------------

STOS_OPTION_DEFER_START_CAPTURE	 = 1
