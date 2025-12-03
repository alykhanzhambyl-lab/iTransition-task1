pattrns = [
    # ISO с миллисекундами: 2024-08-09 16:02:42.627
    "%Y-%m-%d %H:%M:%S.%f",

    # ISO без миллисекунд: 2025-10-20 16:25:20
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",

    # MM/DD/YY date first (с AM/PM и без)
    # 10/01/24 10:38:08 AM, 11/11/24 10:55:32 PM
    "%m/%d/%y %I:%M:%S %p",
    "%m/%d/%y %H:%M:%S",
    "%m/%d/%y %H:%M",

    # time first + MM/DD/YY
    # 05:41:37 05/11/24, 19:46 10/03/24
    "%H:%M:%S %m/%d/%y",
    "%H:%M %m/%d/%y",

    # time first + MM/DD/YY + AM/PM
    # 02:59:55 AM 04/06/25, 01:51:01 AM 09/03/24, 04:17:28 AM 01/18/25
    "%I:%M:%S %p %m/%d/%y",

    # time first + YYYY-MM-DD
    # 22:13:35 2025-07-02, 00:44 2024-05-22, 21:35:15 2025-07-28
    "%H:%M:%S %Y-%m-%d",
    "%H:%M %Y-%m-%d",

    # time first + YYYY-MM-DD + AM/PM
    # 03:49:29 PM 2024-09-03, 06:51:44 PM 2025-04-02
    "%I:%M:%S %p %Y-%m-%d",

    # date first + DD-Mon-YYYY
    # 30-Oct-2024 15:56, 6-Aug-2024 11:49
    "%d-%b-%Y %H:%M",
    "%d-%b-%Y %H:%M:%S",

    # time first + DD-Mon-YYYY
    # 03:37 2-Apr-2025, 10:30:26 1-Nov-2024
    "%H:%M %d-%b-%Y",
    "%H:%M:%S %d-%b-%Y",

    # HH:MM DD-Mon-YYYY (типа 18:33 28-Aug-2024)
    "%H:%M %d-%b-%Y",

    # date first + DD-Month-YYYY
    # 18-December-2024 11:23:08
    "%d-%B-%Y %H:%M:%S",
    "%d-%B-%Y %H:%M",

    # time first + DD-Month-YYYY
    # 09:16:50 AM 24-December-2024
    "%I:%M:%S %p %d-%B-%Y",

    # time first + DD-Month-YYYY + AM/PM через запятую раньше были, но мы запятую убрали
    # 12:23:47 AM 23-September-2024, 08:48:47 AM 28-August-2024
    "%I:%M:%S %p %d-%B-%Y",

    # time first + DD-Mon-YYYY + AM/PM
    # 10:05:25 AM 5-AUG-2024
    "%I:%M:%S %p %d-%b-%Y",
]
