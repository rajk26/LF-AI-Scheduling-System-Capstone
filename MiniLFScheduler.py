"""
IMPORTANT Notes:

This is an early "mini" test program for the Learning Factory TA Scheduler
where a 1 weekday schedule is built for 15 TAs. All input is hard-coded in program.

PLEASE COMMENT ALL CODE FOR EASY UNDERSTANDING

"""
# from typing import Union

from ortools.sat.python import cp_model


def main() -> None:
    # This program tries to find an optimal assignment of TAs to shifts
    # (28 30min increments per day, for 1 day), subject to some constraints (see below).

    # Change num_days to 60 later (or however many TAs there are)
    num_TAs = 15
    
    # Number of 30 minute increments in one day (14 hours, 8AM to 10PM)
    num_30minIncrements = 28

    # Number of work weekdays in a week, change to 4 later
    num_days = 1
    
    # Ranges for easy looping
    all_TAs = range(num_TAs)
    all_30minIncrements = range(num_30minIncrements)
    all_days = range(num_days)
    
    # TA requests for each 30min increment, 4 means can work, 1(?) means prefers not to, -4(?) means cannot
    # [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
    shift_requests = [
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
        [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    ]


    # Incompatability Matrix: NxN Matrix (where N is TA count)
    # If element is 0, the two respective TAs can work together. If element is 1, the two respective TAs can NOT work together.
    incompatability = [
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # Ensure all TAs are able to work with themselves
    for i in all_TAs:
        incompatability[i][i] = 0
            


    # The maximum amount of time (increments of 30min) each TA can work in a day/week
    # min_30minIncrements_per_day = 0
    # max_30minIncrements_per_day = ?
    min_30minIncrements_per_week = 3
    max_30minIncrements_per_week = 16 # FOR NOW (example with only 1 day in a week), CHANGE max_30minIncrements_per_week TO 20 later 





    # daily targets for number of TAs per 30min increments (from 8AM to 10PM) 
    # for each day of the week starting on Monday.
    # NOT SURE IF THESE ARE NEEDED
    #weekly_cover_targets = [
    #    (5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 3, 3, 3)  # Monday
    #    # Note: should be same for all other weekdays
    #]

    # daily maximums for number of TAs per 30min increments (from 8AM to 10PM) 
    # for each day of the week starting on Monday.
    # NOT SURE IF THESE ARE NEEDED
    #weekly_cover_maxs = [
    #    (6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 3, 3, 3, 3, 3, 3, 3)  # Monday
    #    # Note: should be same for all other weekdays
    #]

    # Penalties for being under the target or exceeding the maximum coverage constraint per 30 min increment.
    # WHAT SHOULD THESE BE??? ASK TEAM/STEVE?
    # ALSO NOT SURE IF THESE ARE NEEDED
    # under_target_cover_penalties = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # excess_max_cover_penalties = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


    




    # Creates the model.
    model = cp_model.CpModel()

    # Creates decision variables for each TA for 30min increment for each day.
    # shifts[(n, d, s)]: TA 'n' works 30_min_increment 's' on day 'd'.
    shifts = {}
    for n in all_TAs:
        for d in all_days:
            for s in all_30minIncrements:
                shifts[(n, d, s)] = model.new_bool_var(f"shift_n{n}_d{d}_s{s}")

    
    
    # Add constraints so that:
    # Each 30min increment is assigned to at most 6 TAs during peak hours (8AM to 6PM) and at most 3 TAs during non-peak hours (6PM to 10PM).
    for d in all_days:
        for s in range(20):
            model.Add(sum(shifts[(n, d, s)] for n in all_TAs) <= 6)

    for d in all_days:
        for s in range(20, 28):
            model.Add(sum(shifts[(n, d, s)] for n in all_TAs) <= 3)


    # Add constraints so that:
    # Each TA doesn't work more or less than the specified weekly min/maxes 
    for n in all_TAs:
        model.Add(sum(shifts[(n, d, s)] for d in all_days for s in all_30minIncrements) <= max_30minIncrements_per_week)

    for n in all_TAs:
        model.Add(sum(shifts[(n, d, s)] for d in all_days for s in all_30minIncrements) >= min_30minIncrements_per_week)
    
    # Add constraints so that:
    # No 2 TAs can work together if they are marked on the Incompatability Matrix
    for d in all_days:
        for s in all_30minIncrements:
            for n1 in all_TAs:
                for n2 in all_TAs:
                    if incompatability[n1][n2] == 1:
                        model.Add(shifts[(n1, d, s)] + shifts[(n2, d, s)] <= 1)
                    # It could also be done like this below, but it would be way slower (honestly just keeping it for reference)
                    # model.Add(shifts[(n1, d, s)] + shifts[(n2, d, s)] <= 1).only_enforce_if(incompatability[n1][n2] == 1)



    ####### NEED SOME WAY TO ENFORCE MINIMUM LENGTH OF SHIFT (3 30min increments)

    print("OK\n")


    



if __name__ == "__main__":
    main()