class ApplicationCode():
    # Login code
    LOGIN_REQUEST = '10'
    LOGIN_SUCCESS = '100'
    LOGIN_ERR_INCORRECT = '101'
    LOGIN_ERR_ALREADY_LOGGED_IN = '102'

    # Room codes
    ROOM_JOIN_REQUEST = '21'
    ROOM_JOIN_SUCCESS = '210'
    ROOM_JOIN_ERR = '211'

    # Game Request codes
    WAIT_TIME_REQUEST = '30'
    START_WAITING = '300'
    GAME_START_REQUEST = '31'
    GAME_ASSIGN_ROLE = '310'
    CONTINUE_WAITING = '311'
