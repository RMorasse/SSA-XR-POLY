# contstants for ISY Nodeserver interface

_ISY_BOOL_UOM = 2 # Used for reporting status values for Controller node
_ISY_INDEX_UOM = 25 # Index UOM for custom states (must match editor/NLS in profile):

# constants from nodeserver profile

_XR_NODE_STATUS             = 'ST'
_XR_CTL_ALARM_STATE         = 'GV0'

_XR_CTL_ALARM_STATE_OFFLINE     =  0
_XR_CTL_ALARM_STATE_DISARMED    =  1
_XR_CTL_ALARM_STATE_ARMEDAWAY   =  2
_XR_CTL_ALARM_STATE_ALARM       =  3
_XR_CTL_ALARM_STATE_FIRE        =  4
_XR_CTL_ALARM_STATE_CO          =  5
_XR_CTL_ALARM_STATE_ARMEDSTAY   =  6
_XR_CTL_ALARM_STATE_ARMEDSLEEP  =  7
_XR_CTL_ALARM_STATE_SUPERVISORY =  8

# Must Match above
_XR_CTL_CMD = ['BUSY',
                'DOF',
                'DON',
                'DON3',
                'DON4',
                'DON5',
                'DOF3',
                'DOF4',
                'DOF5',]

_XR_CTL_TYPE_AREAS          =  1
_XR_CTL_TYPE_ALL_PERIMETER  =  2
_XR_CTL_TYPE_HSA            =  3
_XR_CTL_TYPE_HSA_GUEST      =  4




_XR_CTL_LAST_MESSAGE    = 'GV1'
_XR_CTL_LAST_MESSAGE_OK = 0
_XR_CTL_AC_STATE        = 'GV2'
_XR_CTL_BATTERY_STATE   = 'GV3'
_XR_CTL_TAMPER_STATE    = 'GV4'
_XR_CTL_WIRELESS_STATE  = 'GV5'
_XR_CTL_ARM_OPTION      = 'GV20'

_XR_AREA_STATUS          = 'ST'
_XR_AREA_STATUS_OFFLINE  = 0
_XR_AREA_STATUS_ARMED    = 1
_XR_AREA_STATUS_DISARMED = 2

_XR_AREA_ARM_DELAY       = 'GV19'
_XR_ARM_DELAY_NORMAL     = 0
_XR_ARM_DELAY_INSTANT    = 1
_XR_ARM_OPTION_INSTANT   = 2

_XR_AREA_ARM_BYPASS      = 'GV20'
_XR_ARM_BYPASS_NORMAL    = 0
_XR_ARM_BYPASS_FORCE     = 1
_XR_ARM_BYPASS_BYPASS    = 2

_XR_AREA_ARM_AREAS       = 'GV18'
_XR_ARM_AWAY             = 0
_XR_ARM_HOME             = 1
_XR_ARM_SLEEP            = 2

_XR_SET_OUTPUT              = 'GV1'
_XR_SET_OFF                 = 1
_XR_SET_STEADY              = 2
_XR_SET_PULSE               = 3
_XR_SET_MOMENTARY           = 4
_XR_SET_TEMPORAL3           = 5



_XR_ZONE_STATUS             = 'ST'
_XR_ZONE_STATUS_OFFLINE      = 0
_XR_ZONE_STATUS_NORMAL       = 1
_XR_ZONE_STATUS_FAULTED      = 2
_XR_ZONE_STATUS_SHORT        = 3
_XR_ZONE_STATUS_BYPASSED     = 4
_XR_ZONE_STATUS_LOWBATTERY   = 5
_XR_ZONE_STATUS_MISSING      = 6
_XR_ZONE_STATUS_TROUBLE      = 7
_XR_ZONE_STATUS_TAMPER       = 8
_XR_ZONE_STATUS_ALARM        = 9
_XR_ZONE_STATUS_ARMED        = 10

# Must Match above
_XR_ZONE_CMD = ['BUSY',
                '*',
                '*',
                '*',
                '*',
                '*',
                '*',
                '*',
                '*',
                'DON3',
                'DOF3',]

_XR_ZONE_CMD_OPEN           = 'DON'
_XR_ZONE_CMD_CLOSED         = 'DOF'
_XR_ZONE_CMD_RESTORED       = 'DOF3'





_XR_ZONE_BYPASS             = 'GV0'

_XR_ZONE_TYPE               = 'GV1'
_XR_ZONE_TYPE_BLANK         = 0
_XR_ZONE_TYPE_NIGHT         = 1
_XR_ZONE_TYPE_INSTANT       = 2
_XR_ZONE_TYPE_DAY           = 3
_XR_ZONE_TYPE_EXIT          = 4
_XR_ZONE_TYPE_FIRE          = 5
_XR_ZONE_TYPE_PANIC         = 6
_XR_ZONE_TYPE_EMERGENCY     = 7
_XR_ZONE_TYPE_SUPERVISORY   = 8
_XR_ZONE_TYPE_AUX1          = 9
_XR_ZONE_TYPE_AUX2          = 10
_XR_ZONE_TYPE_FIREVERIFY    = 11
_XR_ZONE_TYPE_ARMING        = 12
_XR_ZONE_TYPE_CARBONMONOXIDE= 13
_XR_ZONE_TYPE_DOORBELL      = 14

_XR_ZONE_STATE             ='GV2'
_XR_ZONE_STATE_CLOSED      = 0
_XR_ZONE_STATE_OPEN        = 1

_XR_AREA_CMD_OFFINE         = 'BUSY'
_XR_AREA_CMD_ARMED          = 'DON'
_XR_AREA_CMD_DISARMED       = 'DOF'

_XR_OUTPUT_STATUS           = 'ST'
_XR_OUTPUT_STATUS_OFFLINE   = 0
_XR_OUTPUT_STATUS_OFF       = 1
_XR_OUTPUT_STATUS_PULSE     = 2
_XR_OUTPUT_STATUS_STEADY    = 3
_XR_OUTPUT_STATUS_TEMPORAL3 = 4
_XR_OUTPUT_STATUS_WINK      = 5
_XR_OUTPUT_STATUS_PANIC     = 6
_XR_OUTPUT_STATUS_PANICTEST = 7

# Must Match above
_XR_OUTPUT_CMD  = ['BUSY',
                   'DOF',
                   'DON3',
                   'DON',
                   'DON5',
                   '*',
                   '*',
                   '*',
                ]


_XR_OUTPUT_OPTIONS          = 'GV1'
_XR_OUTPUT_OPTIONS_OFF      = 0
_XR_OUTPUT_OPTIONS_PULSE    = 1
_XR_OUTPUT_OPTIONS_STEADY   = 2
_XR_OUTPUT_OPTIONS_MOMENTARY= 3
_XR_OUTPUT_OPTIONS_TEMPORAL3= 4

_XR_AREA_NODE           = 'area'
_XR_ZONE_NODE           = 'zone'
_XR_OUTPUT_NODE         = 'output'

_XR_ZONE_STATUS_VALUE   =  b' NOSXLM'
_XR_AREA_STATUS_VALUE   =  b' AD'
_XR_OUTPUT_STATUS_VALUE =  b' OPSTWat'


#XR Commands
_CMD_CONFIG_REQUEST = b'?WB' 
_CMD_CONFIG_REQUEST_DATA = b' *Y001'  #Request Zones & Areas
_CMD_AREA_STATUS = b'?WA'             #Request Areas
_CMD_BYPASS_ZONE = b'!X'
_CMD_UNBYPASS_ZONE = b'!Y'
_CMD_ARM_AREA = b'!C'
_CMD_DISARM_AREA = b'!O'
_CMD_STATUS_REQUEST = b'?WS'
_CMD_ZONE_CONFIG_REQUEST = b'?Zl'
_CMD_SENSOR_RESET = b'!E001'
_CMD_OUTPUT_REQUEST = b'?WQ'
_CMD_OPTION_REQUEST = b'?Zo'
_CMD_OUTPUT_SET = b'!Q'


#XR Command Responses
_ACK_BYPASS_ZONE = b'+X'
_NAK_BYPASS_ZONE = b'+X'
_ACK_UNBYPASS_ZONE = b'+Y'
_NAK_UNBYPASS_ZONE = b'-Y'
_ACK_ARM_AREA = b'+C'
_NAK_ARM_AREA = b'-C'
_ACK_DISARM_AREA = b'+O'
_NAK_DISARM_AREA = b'+O'
_ACK_SENSOR_RESET = b'+E'
_NAK_SENSOR_RESET = b'-E'
_ACK_OUTPUT_SET = b'+Q'
_NAK_OUTPUT_SET = b'-Q'

#XR Response messages codes
_MSG_PANEL_CONFIG = b'*WB'
_MSG_SYSTEM_STATUS = b'*WS'
_MSG_ZONE_CONFIG = b'*Zl'
_MSG_AREA_STATUS = b'*WA'
_MSG_OUTPUT_CONFIG = b'*WQ'
_MSG_OPTION_CONFIG = b'*Zo'

_MSG_ACK = b'\06'

_MSG_EVENT_ZONE_ALARM   = b'Za'
_MSG_EVENT_ZONE_FORCE   = b'Zb'
_MSG_EVENT_DEVICE_STATUS= b'Zc'
_MSG_EVENT_ZONE_LOWBAT  = b'Zd'
_MSG_EVENT_ZONE_FAIL    = b'Zf'
_MSG_EVENT_ZONE_MISSING = b'Zh'
_MSG_EVENT_ZONE_TAMPER  = b'Zi'
_MSG_EVENT_ARMING       = b'Zq'
_MSG_EVENT_ZONE_RESTORE = b'Zr'
_MSG_EVENT_SYSTEM_MSG   = b'Zs'
_MSG_EVENT_ZONE_TROUBLE = b'Zt'
_MSG_EVENT_ZONE_BYPASS  = b'Zx'
_MSG_EVENT_ZONE_RESET   = b'Zy'
_MSG_EVENT_DOOR_ACCESS  = b'Zj'
_MSG_EVENT_ZONE_FAULT   = b'Zw'


# These are not events from the XR, but used by our state table
_MSG_EVENT_ZONE_OPEN     = b'*O'
_MSG_EVENT_ZONE_CLOSE    = b'*C'
_MSG_EVENT_ARMED         = b'*A'
_MSG_EVENT_DISARMED      = b'*D'