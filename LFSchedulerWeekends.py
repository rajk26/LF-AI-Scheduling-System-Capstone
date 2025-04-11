"""
IMPORTANT Notes:

This is a test program for the Learning Factory TA Scheduler
where a 3 weekend schedule is built for 38 TAs. All input is hard-coded in program.

PLEASE COMMENT ALL CODE FOR EASY UNDERSTANDING

"""

from ortools.sat.python import cp_model


def main() -> None:
    # This program tries to find an optimal assignment of TAs to shifts
    # (28 30min increments per day, for 5 days), subject to some constraints (see below).

    # PREEXISTING Don't copy
    num_TAs = 38
    all_TAs = range(num_TAs)
    max_nonpeakTAs = 3








    
    # Number of shifts in a weekend
    WEEKEND_num_shifts = 3
    
    # Number of work weekends
    WEEKEND_num_weeks = 15
    
    # Weekend Ranges for easy looping
    WEEKEND_all_shifts = range(WEEKEND_num_shifts)
    WEEKEND_all_weeks = range(WEEKEND_num_weeks)
    WEEKEND_Friday = 0
    WEEKEND_SatSun = range(1, WEEKEND_num_shifts)


    # Weekend weekly max for every TA (Work only 1 weekend day every week?)
    WEEKEND_max_shifts_per_week = 2


    # Weekend target number of shifts in a semester
    WEEKEND_min_shifts_per_TA = 2
    WEEKEND_max_shifts_per_TA = 3


    # The maximum number of TAs at a time during Saturday and Sunday
    max_SatSunTAs = 2


    # TA requests for each WEEKEND shift, 4 means can work, 1 means prefers not to, 0 means cannot
    WEEKEND_shift_requests = [[[0 for _ in WEEKEND_all_shifts] for _ in WEEKEND_all_weeks] for _ in all_TAs]

    WEEKEND_TA_Input = [[0 for _ in WEEKEND_all_shifts] for _ in all_TAs]


    WEEKEND_TA_String = "January 31st;February 7th,February 1st;February 8th;February 15th,February 2nd;February 9th;February 16th\nJanuary 17th;January 24th;February 7th;February 21st;February 28th;April 4th;April 11th;April 18th;April 25th;May 2nd,February 15th;February 22nd;March 1st;April 5th;April 12th;April 19th;April 26th,February 9th;February 16th;February 23rd;March 2nd;April 6th;April 13th;April 20th;April 27th\nMarch 28th;,March 1st;,March 2nd;\nJanuary 17th,January 18th;January 25;February 1st;February 8th;February 15th;February 22nd;March 1st;March 8th,January 19th;January 26th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 9th\nJanuary 24th;January 17th;February 7th;February 21st;,January 18th;January 25;February 8th;February 22nd;,January 26th;January 19th;February 9th;February 23rd;\nJanuary 17th;February 7th;March 7th;April 4th,January 18th;February 1st;March 1st;March 8th,January 19th;February 2nd;February 23rd\nFebruary 28th;February 21st;March 21st;April 4th;April 11th;April 18th;April 25th;January 31st;February 7th;January 24th;,January 18th;January 25;March 22nd;March 1st;February 22nd;February 15th;February 8th;February 1st;March 29th;April 5th;April 12th;April 26th;April 19th;,March 2nd;February 23rd;February 16th;February 9th;February 2nd;January 26th;January 19th;April 27th;April 20th;April 13th;April 6th;March 23rd;\nJanuary 17th;January 24th;January 31st;February 7th;February 14th;February 21st;March 7th;February 28th;March 21st;March 28th;April 4th;April 18th;April 11th;April 25th;,January 18th;January 25;February 1st;February 8th;February 15th;February 22nd;March 1st;April 19th;April 12th;April 5th;March 29th;April 26th;,January 19th;January 26th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 30th;April 6th;April 13th;April 20th;\nJanuary 17th;January 24th;January 31st;February 7th;February 14th;February 21st;February 28th;March 7th;March 28th;April 4th;April 11th;April 18th;April 25th;May 2nd;March 21st;,January 18th;January 25;February 1st;February 8th;February 15th;February 22nd;March 1st;March 8th;March 22nd;March 29th;April 5th;April 12th;April 19th;April 26th;May 3rd;,January 19th;January 26th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 9th;March 23rd;March 30th;April 6th;April 13th;April 20th;April 27th;\nJanuary 17th;January 24th;January 31st;February 7th;February 14th;February 21st;February 28th;March 7th;March 21st;March 28th;April 4th;April 11th;April 18th;April 25th;May 2nd;,January 18th;January 25;February 1st;February 8th;February 15th;February 22nd;March 1st;March 8th;March 22nd;March 29th;April 5th;April 12th;April 19th;April 26th;May 3rd;,January 26th;January 19th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 9th;March 23rd;March 30th;April 6th;April 13th;April 20th;April 27th;\nJanuary 24th;February 21st;February 7th;January 17th;March 7th;February 28th;March 28th;April 4th;April 11th;,January 18th;January 25;February 8th;February 22nd;March 1st;March 22nd;March 29th;April 5th;,January 19th;January 26th;February 2nd;February 9th;February 23rd;March 9th;March 2nd;April 6th;March 30th;\nJanuary 17th;January 24th;January 31st;February 7th;February 14th;February 21st;February 28th;March 21st;March 28th;April 4th;April 11th;April 18th,January 18th;January 25;February 1st;February 8th;February 15th;February 22nd;March 1st;March 29th;April 5th;April 12th;April 19th,January 19th;January 26th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 30th;April 6th;April 13th;April 20th\nJanuary 24th;January 31st;March 21st;February 28th;February 21st;February 14th;February 7th;March 28th;April 4th;April 11th;April 18th;April 25th;May 2nd,January 25;March 22nd;March 1st;February 22nd;February 15th;February 8th;February 1st;March 29th;April 5th;April 12th;April 19th;April 26th;May 3rd,January 26th;February 2nd;February 16th;March 2nd;February 23rd;February 9th;March 23rd;March 30th;April 6th;April 13th;April 20th;April 27th\nJanuary 31st;January 24th;,February 1st;January 25;,February 2nd;January 26th;\nMay 2nd;,May 3rd;April 12th;April 5th;March 29th;March 22nd;March 1st;,January 19th;January 26th;March 2nd;March 30th;March 23rd;April 6th;\nJanuary 31st;,February 1st;,February 2nd;\nJanuary 24th;January 31st;February 7th;February 14th;February 21st;February 28th;March 21st;March 28th;,January 25;February 1st;February 8th;February 15th;February 22nd;March 1st;March 8th;,January 26th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 9th;\nJanuary 31st;February 7th;March 21st;March 28th;April 4th;April 11th;April 25th;,January 25;February 1st;February 8th;March 1st;March 29th;April 5th;April 26th;March 22nd;,February 2nd;February 16th;February 23rd;March 2nd;March 30th;April 27th;\nJanuary 17th;January 24th;January 31st;February 7th;February 21st;February 14th;February 28th;March 7th;March 21st;March 28th;April 4th;April 11th;April 18th;April 25th;May 2nd,January 18th;January 25;February 1st;February 8th;February 15th;February 22nd;March 1st;March 8th;March 22nd;March 29th;April 5th;April 12th;April 19th;April 26th;May 3rd,January 19th;January 26th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 9th;March 23rd;March 30th;April 6th;April 13th;April 20th;April 27th\nJanuary 17th;January 24th;January 31st;February 7th;February 14th;March 21st;May 2nd;,January 18th;January 25;February 1st;February 8th;February 15th;March 22nd;May 3rd;,March 9th;\nJanuary 24th;January 31st;February 7th;February 21st;February 28th;March 21st;March 28th;April 4th;April 11th;April 18th;April 25th,January 25;February 1st;February 8th;February 22nd;March 1st;March 22nd;March 29th;April 5th;April 12th;April 19th;April 26th,January 19th;February 9th;February 2nd;January 26th;February 23rd;March 2nd;March 23rd;March 30th;April 6th;April 27th;April 20th;April 13th\nJanuary 31st;,February 1st;,February 2nd;\nJanuary 17th;January 31st;February 14th;,January 18th;,April 27th;\nJanuary 17th;January 24th;January 31st;February 7th;February 14th;February 21st;February 28th;March 7th;March 21st;March 28th;April 4th;April 11th;April 18th;April 25th;May 2nd;,January 18th;February 1st;February 8th;January 25;February 15th;March 1st;February 22nd;March 8th;March 22nd;March 29th;April 5th;April 12th;April 19th;May 3rd;,January 19th;January 26th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 9th;March 23rd;March 30th;April 6th;April 13th;April 20th;April 27th;\nFebruary 7th;February 21st;January 17th;January 24th;April 18th;April 4th;March 28th,February 22nd;May 3rd;April 26th;April 19th;April 12th;April 5th;March 1st;February 1st;January 25;January 18th,January 19th;January 26th;February 2nd;February 9th;February 16th;February 23rd;March 30th;April 6th;April 13th;April 20th;April 27th\nJanuary 31st;,February 1st;,February 2nd;\nJanuary 17th;February 7th;,January 18th;February 8th;,January 19th;February 9th;\nJanuary 24th,April 26th,January 19th;January 26th;February 2nd;February 9th;February 16th;February 23rd\nJanuary 17th;January 24th;January 31st;April 4th;April 11th;April 18th;April 25th;,January 18th;January 25;April 5th;April 12th;April 19th;April 26th;May 3rd;,April 27th;\nJanuary 24th;January 31st;February 7th;February 14th;February 21st;February 28th;March 7th;March 21st;March 28th;April 4th;April 11th;April 18th;April 25th;,January 25;February 1st;February 8th;February 15th;February 22nd;April 26th;April 19th;April 12th;April 5th;March 29th;March 22nd;March 8th;March 1st;,January 26th;February 2nd;February 9th;April 20th;April 13th;April 27th;April 6th;March 30th;March 23rd;March 9th;March 2nd;February 23rd;February 16th;\nJanuary 24th;January 31st;February 7th;February 14th;January 17th;February 21st;February 28th;March 7th;March 21st;March 28th;April 4th;April 11th;April 18th;April 25th;May 2nd;,January 25;February 8th;February 1st;February 15th;February 22nd;March 1st;March 8th;March 22nd;March 29th;April 5th;April 12th;April 19th;April 26th;May 3rd;,January 26th;February 2nd;February 9th;February 16th;February 23rd;March 2nd;March 9th;March 23rd;March 30th;April 6th;April 13th;April 20th;April 27th;\nJanuary 24th;February 7th;February 21st;March 21st;April 18th;April 4th;May 2nd;,January 25;February 8th;February 22nd;March 22nd;April 5th;April 19th;,January 26th;February 9th;March 2nd;March 23rd;April 6th;April 20th;\nJanuary 24th;January 31st;January 17th;February 7th;April 11th;April 4th,January 25;February 1st;February 8th;February 22nd;March 1st;April 5th;April 12th,January 19th;January 26th;February 2nd;February 23rd;March 2nd;April 6th;April 13th\nJanuary 31st;February 7th;February 14th;February 21st;January 24th;,February 1st;February 8th;February 15th;February 22nd;March 1st;January 25;,February 2nd;February 9th;February 16th;February 23rd;March 2nd;\nJanuary 17th;February 7th;February 14th;March 28th;April 4th;April 11th;April 18th;April 25th;March 21st;,January 18th;February 8th;February 15th;March 22nd;March 29th;April 5th;April 12th;April 19th;April 26th;,January 19th;February 9th;February 16th;March 23rd;March 30th;April 6th;April 13th;April 20th;April 27th;\nJanuary 17th;January 24th;January 31st;February 7th;February 14th;February 21st;February 28th;March 28th;March 21st;April 4th;April 11th;April 18th;April 25th;,January 18th;January 25;February 1st;February 8th;February 15th;February 22nd;March 1st;March 22nd;March 29th;April 5th;April 19th;April 12th;April 26th;,January 19th;February 2nd;January 26th;February 9th;February 16th;February 23rd;March 2nd;March 23rd;March 30th;April 6th;April 13th;April 20th;\nJanuary 17th;February 28th;February 21st;,January 18th;February 1st;February 8th;February 15th;February 22nd;March 1st;March 29th;April 5th;April 12th;,January 19th;\nJanuary 31st;February 7th;February 14th;February 28th;March 7th;March 21st;March 28th;April 4th;April 11th;April 18th;April 25th;May 2nd,January 18th;February 1st;February 8th;February 15th;March 1st;March 8th;March 22nd;March 29th;April 5th;April 12th;April 19th;May 3rd;April 26th,January 19th;February 2nd;February 9th;February 16th;March 2nd;March 9th;March 23rd;March 30th;April 13th;April 6th;April 20th;April 27th"

    WEEKEND_TA_String_Inter = WEEKEND_TA_String.splitlines()
    for n in all_TAs:
        WEEKEND_TA_Input[n] = WEEKEND_TA_String_Inter[n].split(',')


    for n in all_TAs:
        if "January 17th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][0][0] = 4
        else:
            WEEKEND_shift_requests[n][0][0] = 0

        if "January 18th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][0][1] = 4
        else:
            WEEKEND_shift_requests[n][0][1] = 0

        if "January 19th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][0][2] = 4
        else:
            WEEKEND_shift_requests[n][0][2] = 0






        if "January 24th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][1][0] = 4
        else:
            WEEKEND_shift_requests[n][1][0] = 0

        if "January 25" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][1][1] = 4
        else:
            WEEKEND_shift_requests[n][1][1] = 0

        if "January 26th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][1][2] = 4
        else:
            WEEKEND_shift_requests[n][1][2] = 0





        if "January 31st" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][2][0] = 4
        else:
            WEEKEND_shift_requests[n][2][0] = 0

        if "February 1st" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][2][1] = 4
        else:
            WEEKEND_shift_requests[n][2][1] = 0

        if "February 2nd" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][2][2] = 4
        else:
            WEEKEND_shift_requests[n][2][2] = 0








        if "February 7th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][3][0] = 4
        else:
            WEEKEND_shift_requests[n][3][0] = 0

        if "February 8th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][3][1] = 4
        else:
            WEEKEND_shift_requests[n][3][1] = 0

        if "February 9th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][3][2] = 4
        else:
            WEEKEND_shift_requests[n][3][2] = 0








        if "February 14th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][4][0] = 4
        else:
            WEEKEND_shift_requests[n][4][0] = 0

        if "February 15th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][4][1] = 4
        else:
            WEEKEND_shift_requests[n][4][1] = 0

        if "February 16th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][4][2] = 4
        else:
            WEEKEND_shift_requests[n][4][2] = 0






        if "February 21st" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][5][0] = 4
        else:
            WEEKEND_shift_requests[n][5][0] = 0

        if "February 22nd" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][5][1] = 4
        else:
            WEEKEND_shift_requests[n][5][1] = 0

        if "February 23rd" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][5][2] = 4
        else:
            WEEKEND_shift_requests[n][5][2] = 0






        if "February 28th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][6][0] = 4
        else:
            WEEKEND_shift_requests[n][6][0] = 0

        if "March 1st" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][6][1] = 4
        else:
            WEEKEND_shift_requests[n][6][1] = 0

        if "March 2nd" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][6][2] = 4
        else:
            WEEKEND_shift_requests[n][6][2] = 0





        if "March 7th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][7][0] = 4
        else:
            WEEKEND_shift_requests[n][7][0] = 0

        if "March 8th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][7][1] = 4
        else:
            WEEKEND_shift_requests[n][7][1] = 0

        if "March 9th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][7][2] = 4
        else:
            WEEKEND_shift_requests[n][7][2] = 0





        if "March 21st" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][8][0] = 4
        else:
            WEEKEND_shift_requests[n][8][0] = 0

        if "March 22nd" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][8][1] = 4
        else:
            WEEKEND_shift_requests[n][8][1] = 0

        if "March 23rd" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][8][2] = 4
        else:
            WEEKEND_shift_requests[n][8][2] = 0





        if "March 28th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][9][0] = 4
        else:
            WEEKEND_shift_requests[n][9][0] = 0

        if "March 29th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][9][1] = 4
        else:
            WEEKEND_shift_requests[n][9][1] = 0

        if "March 30th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][9][2] = 4
        else:
            WEEKEND_shift_requests[n][9][2] = 0






        if "April 4th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][10][0] = 4
        else:
            WEEKEND_shift_requests[n][10][0] = 0

        if "April 5th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][10][1] = 4
        else:
            WEEKEND_shift_requests[n][10][1] = 0

        if "April 6th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][10][2] = 4
        else:
            WEEKEND_shift_requests[n][10][2] = 0





        if "April 11th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][11][0] = 4
        else:
            WEEKEND_shift_requests[n][11][0] = 0

        if "April 12th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][11][1] = 4
        else:
            WEEKEND_shift_requests[n][11][1] = 0

        if "April 13th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][11][2] = 4
        else:
            WEEKEND_shift_requests[n][11][2] = 0





        if "April 18th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][12][0] = 4
        else:
            WEEKEND_shift_requests[n][12][0] = 0

        if "April 19th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][12][1] = 4
        else:
            WEEKEND_shift_requests[n][12][1] = 0

        if "April 20th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][12][2] = 4
        else:
            WEEKEND_shift_requests[n][12][2] = 0





        if "April 25th" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][13][0] = 4
        else:
            WEEKEND_shift_requests[n][13][0] = 0

        if "April 26th" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][13][1] = 4
        else:
            WEEKEND_shift_requests[n][13][1] = 0

        if "April 27th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][13][2] = 4
        else:
            WEEKEND_shift_requests[n][13][2] = 0





        if "May 2nd" in WEEKEND_TA_Input[n][0]:
            WEEKEND_shift_requests[n][14][0] = 4
        else:
            WEEKEND_shift_requests[n][14][0] = 0

        if "May 3rd" in WEEKEND_TA_Input[n][1]:
            WEEKEND_shift_requests[n][14][1] = 4
        else:
            WEEKEND_shift_requests[n][14][1] = 0

        if "May 4th" in WEEKEND_TA_Input[n][2]:
            WEEKEND_shift_requests[n][14][2] = 4
        else:
            WEEKEND_shift_requests[n][14][2] = 0





    for n in all_TAs:
        for w in WEEKEND_all_weeks:
            for s in WEEKEND_all_shifts:
                if WEEKEND_shift_requests[n][w][s] == 0:
                    WEEKEND_shift_requests[n][w][s] = -2





    # Creates the model.
    WEEKENDmodel = cp_model.CpModel()


    # Creates decision variables for each TA for 30min increment for each day.
    # shifts[(n, d, s)]: TA 'n' works 30_min_increment 's' on day 'd'.
    # If TA n cannot work during a time slot (d, s), immediately mark shifts[(n, d, s)] == 0
    WEEKENDshifts = {}
    for n in all_TAs:
        for w in WEEKEND_all_weeks:
            for s in WEEKEND_all_shifts:
                WEEKENDshifts[(n, w, s)] = WEEKENDmodel.new_bool_var(f"shift_n{n}_w{w}_s{s}")
                if WEEKEND_shift_requests[n][w][s] == -2:
                    WEEKENDmodel.Add(WEEKENDshifts[(n, w, s)] == 0)



    # Last Sunday is not worked(???)

    
    # Add constraints so that:
    # Each shift is assigned to at most 3 TAs during Friday and 2 TAs during Sat/Sun
    for w in WEEKEND_all_weeks:
        WEEKENDmodel.Add(sum(WEEKENDshifts[(n, w, WEEKEND_Friday)] for n in all_TAs) == max_nonpeakTAs)
        for s in WEEKEND_SatSun:
            if w != 14 or s != 2:
                WEEKENDmodel.Add(sum(WEEKENDshifts[(n, w, s)] for n in all_TAs) == max_SatSunTAs)

    

    # Add constraints so that:
    # Each TA doesn't work more than the specified weekly max for Weekends
    for n in all_TAs:
        for w in WEEKEND_all_weeks:
            WEEKENDmodel.Add(sum(WEEKENDshifts[(n, w, s)] for s in WEEKEND_all_shifts) <= WEEKEND_max_shifts_per_week)


    # Add constraints so that:
    # Each TA works either 2 or 3 weekend shifts in a semester
    for n in all_TAs:
        WEEKENDmodel.Add(sum(WEEKENDshifts[(n, w, s)] for w in WEEKEND_all_weeks for s in WEEKEND_all_shifts) >= WEEKEND_min_shifts_per_TA)
        WEEKENDmodel.Add(sum(WEEKENDshifts[(n, w, s)] for w in WEEKEND_all_weeks for s in WEEKEND_all_shifts) <= WEEKEND_max_shifts_per_TA)




    # Add constraints so that:
    # No 2 TAs can work together if they are marked on the Incompatability Matrix

    # for w in WEEKEND_all_weeks:
    #     for s in WEEKEND_all_shifts:
    #         for n1 in all_TAs:
    #             for n2 in all_TAs:
    #                 if incompatibility[n1][n2] == 1:
    #                     WEEKENDmodel.Add(WEEKENDshifts[(n1, w, s)] + WEEKENDshifts[(n2, w, s)] <= 1)


    # Objective: Maximize TA preferences while ensuring coverage, and ensure weekend shift even-ness
    WEEKENDmodel.Maximize(
        sum(WEEKENDshifts[(n, w, s)] * WEEKEND_shift_requests[n][w][s] for n in all_TAs for w in WEEKEND_all_weeks for s in WEEKEND_all_shifts) 
    )

    # Solve model
    WEEKENDsolver = cp_model.CpSolver()
    WEEKENDstatus = WEEKENDsolver.Solve(WEEKENDmodel)

    # Display results
    if WEEKENDstatus in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("\nWeekend Solution Found: TA Shift Assignments\n")

        print(f"Weekend Objective Value: {WEEKENDsolver.objective_value}\n")

        for n in all_TAs:
            WEEKEND_assigned_shifts = [
                (w, s) for w in WEEKEND_all_weeks for s in WEEKEND_all_shifts if WEEKENDsolver.Value(WEEKENDshifts[(n, w, s)]) == 1
            ]
            print(f"TA {n}: {len(WEEKEND_assigned_shifts)} shifts -> {WEEKEND_assigned_shifts}")

        for w in WEEKEND_all_weeks:
            for s in WEEKEND_all_shifts:
                print(f"Week {w} shift {s}: {sum(WEEKENDsolver.Value(WEEKENDshifts[(n, w, s)]) for n in all_TAs)}")

    else:
        print("\nNo feasible solution found for weekend. Try relaxing constraints further.")

    
    

    



if __name__ == "__main__":
    main()
