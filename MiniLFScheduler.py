"""
IMPORTANT Notes:

This is an early "mini" test program for the Learning Factory TA Scheduler
where a 1 weekday schedule is built for 15 TAs. All input is hard-coded in program.

PLEASE COMMENT ALL CODE FOR EASY UNDERSTANDING

"""

from ortools.sat.python import cp_model


def main() -> None:
    # This program tries to find an optimal assignment of TAs to shifts
    # (28 30min increments per day, for 1 day), subject to some constraints (see below).

    # Change num_days to 60 later (or however many TAs there are)
    num_TAs = 15
    
    # Number of 30-minute increments per day (14 hours, 8 AM - 10 PM)
    num_30minIncrements = 28

    # Number of work weekdays in a week, change to 5 later
    num_days = 1
    
    # Ranges for easy looping
    all_TAs = range(num_TAs)
    all_30minIncrements = range(num_30minIncrements)
    all_days = range(num_days)
    # Peak hours: 8 AM - 6 PM (20 slots), Off-peak: 6 PM - 10 PM (8 slots)
    peak_slots = range(20)
    offpeak_slots = range(20, num_30minIncrements)


    # The maximum amount of time (increments of 30min) each TA can work in a day/week
    min_30minIncrements_per_day = 0
    max_30minIncrements_per_day = 16
    min_30minIncrements_per_week = 3
    max_30minIncrements_per_week = 16 # FOR NOW (example with only 1 day in a week), CHANGE max_30minIncrements_per_week TO 32 later 



    # The maximum number of TAs at a time during peak and non-peak hours
    max_peakTAs = 6
    max_nonpeakTAs = 3


    # The target number of 30min increments for each TA to work weekly (only including weekdays): 
    # Sponsor wants 20 (10hrs), but that doesn't make sense, should be (total number of 30min increments that need to be worked) / (number of TAs)
    target_30minIncrements_per_TA = 9


    
    # TA requests for each 30min increment, 4 means can work, 1(?) means prefers not to, -4(?) means cannot
    # [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
    # shift_requests = [
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    #     [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]],
    # ]
    shift_requests = [[[4 for _ in all_30minIncrements] for _ in all_days] for _ in all_TAs]

    # Incompatability Matrix: NxN Matrix (where N is TA count)
    # If element is 0, the two respective TAs can work together. If element is 1, the two respective TAs can NOT work together.
    incompatibility = [[0] * num_TAs for _ in range(num_TAs)]
    incompatibility[0][14] = 1  # Example: TA 0 and TA 14 cannot work together
    incompatibility[14][0] = 1  # Ensure symmetry

    # Ensure all TAs are able to work with themselves
    for i in all_TAs:
        incompatibility[i][i] = 0
            


    





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

    
    # THE NEW FRIDAY INFO MAKES THE WEEKDAY SCHEDULER A LITTLE MORE COMPLICATED:
    # SINCE WE CAN'T HAVE A DIFFERENT AMOUNT OF HOURS IN A DAY,
    # JUST SET "MAX" OF 0 TA's DURING NON-PEAK HOURS FRIDAY,
    # AND SET ALL DECISION VARIABLES DURING THAT SPAN TO 0 AS WELL

    # Add constraints so that:
    # Each 30min increment is assigned to at most 6 TAs during peak hours (8AM to 6PM) and at most 3 TAs during non-peak hours (6PM to 10PM).
    for d in all_days:
        for s in peak_slots:
            model.Add(sum(shifts[(n, d, s)] for n in all_TAs) <= max_peakTAs)
        for s in offpeak_slots:
            model.Add(sum(shifts[(n, d, s)] for n in all_TAs) <= max_nonpeakTAs)


    # Add constraints so that:
    # Each TA doesn't work more or less than the specified weekly min/maxes
    for n in all_TAs:
        model.Add(sum(shifts[(n, d, s)] for d in all_days for s in all_30minIncrements) >= min_30minIncrements_per_week)
        model.Add(sum(shifts[(n, d, s)] for d in all_days for s in all_30minIncrements) <= max_30minIncrements_per_week)


    # Add constraints so that:
    # Each TA doesn't work more or less than the specified daily min/maxes
    for n in all_TAs:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_30minIncrements) >= min_30minIncrements_per_day)
            model.Add(sum(shifts[(n, d, s)] for s in all_30minIncrements) <= max_30minIncrements_per_day)
    
    # Add constraints so that:
    # No 2 TAs can work together if they are marked on the Incompatability Matrix
    for d in all_days:
        for s in all_30minIncrements:
            for n1 in all_TAs:
                for n2 in all_TAs:
                    if incompatibility[n1][n2] == 1:
                        model.Add(shifts[(n1, d, s)] + shifts[(n2, d, s)] <= 1)
                    # It could also be done like this below, but it would be way slower (honestly just keeping it for reference)
                    # model.Add(shifts[(n1, d, s)] + shifts[(n2, d, s)] <= 1).only_enforce_if(incompatability[n1][n2] == 1)


    
    # Add constraints to:
    # ENFORCE MINIMUM LENGTH OF SHIFT (3 30min increments)

    # Any TA working during 8:00AM-8:30AM must also be working 8:30AM-9:30AM
    for n in all_TAs:
        for d in all_days:
            model.Add(shifts[(n, d, 0)] + shifts[(n, d, 1)] + shifts[(n, d, 2)] == 3).only_enforce_if(shifts[(n, d, 0)])
    
    # Any TA starting a shift during a 30min increment from 8:30AM to 9:00PM, must also be working the next 2 subsequent 30min increments
    for n in all_TAs:
        for d in all_days:
            for s in range(1, 26):
                model.Add(shifts[(n, d, s)] + shifts[(n, d, s + 1)] + shifts[(n, d, s + 2)] == 3).only_enforce_if(shifts[(n, d, s)], ~shifts[(n, d, s - 1)])

    # Any TA working during 9:00PM-10:00PM must not be starting their shift during a 30min increment from 9:00PM-10:00PM
    for n in all_TAs:
        for d in all_days:
            for s in range(26, 28):
                model.Add(shifts[(n, d, s)] == 0).only_enforce_if(~shifts[(n, d, s - 1)])
    
    

    # Create IntVars for objective function to ensure shift even-ness between all TAs. 
    # We want to minimize, for each TA:
    #                                  The difference between (target_30minIncrements_per_TA),
    #                                  and the total number of 30min increments they work in a week
    difference_from_target_for_TAs = {}
    for n in all_TAs:
        difference_from_target_for_TAs[(n)] = model.new_int_var(0, max(max_30minIncrements_per_week - target_30minIncrements_per_TA, target_30minIncrements_per_TA), f"difference_from_target_for_TA_{n}")
        model.AddAbsEquality(difference_from_target_for_TAs[(n)], sum(shifts[(n, d, s)] for d in all_days for s in all_30minIncrements) - target_30minIncrements_per_TA)


    print("OK\n")

    # Objective: Maximize TA preferences while ensuring coverage, and ensure shift even-ness
    model.Maximize(
        sum(shifts[(n, d, s)] * shift_requests[n][d][s] for n in all_TAs for d in all_days for s in all_30minIncrements) 
        - sum(difference_from_target_for_TAs[(n)] for n in all_TAs)
    )

    # Solve model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Display results
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("\nSolution Found: TA Shift Assignments\n")

        print(f"Objective Value: {solver.objective_value}\n")
        for n in all_TAs:
            assigned_shifts = [
                (d, s) for d in all_days for s in all_30minIncrements if solver.Value(shifts[(n, d, s)]) == 1
            ]
            print(f"TA {n}: {len(assigned_shifts)} shifts -> {assigned_shifts}")
            #print(f"difference_from_target_for_TA_{n} = {solver.value(difference_from_target_for_TAs[(n)])}")
            # USED FOR DUBUGGING print(f"Actual difference from target for TA {n}: {target_30minIncrements_per_TA - sum(solver.Value(shifts[(n, d, s)]) for d in all_days for s in all_30minIncrements)}")
    else:
        print("\nNo feasible solution found. Try relaxing constraints further.")

    



if __name__ == "__main__":
    main()




"""
Mini Test Program for Learning Factory TA Scheduler
This script assigns TAs to shifts while considering:
- TA availability & preferences
- Minimum/maximum shift lengths
- Coverage constraints for peak/off-peak hours
- TA incompatibilities

"""
