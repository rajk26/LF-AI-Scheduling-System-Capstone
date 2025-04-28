# streamlit_app.py
import streamlit as st
import pandas as pd
from ortools.sat.python import cp_model
import time

# Streamlit Page Settings 
st.set_page_config(page_title="📅 TA Scheduler", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    /* Background and Text */
    .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1f1f1f;
    }
    /* Headers */
    h1, h2, h3 {
        color: #8ab4f8;
    }
    /* Buttons */
    div.stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 8px;
        font-size: 1em;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #155a96;
    }
    /* File Uploader Box */
    section.main > div > div > div > div > div > div > div > div {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 8px;
    }
    /* Expander (Cards) */
    .streamlit-expanderHeader {
        font-weight: bold;
        color: #f9ab00;
        font-size: 1.1em;
    }
    </style>
""", unsafe_allow_html=True)

#Main Application
def main():
    time_slots = [
        "08:00am - 08:30am", "08:30am - 09:00am", "09:00am - 09:30am", "09:30am - 10:00am",
        "10:00am - 10:30am", "10:30am - 11:00am", "11:00am - 11:30am", "11:30am - 12:00pm",
        "12:00pm - 12:30pm", "12:30pm - 01:00pm", "01:00pm - 01:30pm", "01:30pm - 02:00pm",
        "02:00pm - 02:30pm", "02:30pm - 03:00pm", "03:00pm - 03:30pm", "03:30pm - 04:00pm",
        "04:00pm - 04:30pm", "04:30pm - 05:00pm", "05:00pm - 05:30pm", "05:30pm - 06:00pm",
        "06:00pm - 06:30pm", "06:30pm - 07:00pm", "07:00pm - 07:30pm", "07:30pm - 08:00pm",
        "08:00pm - 08:30pm", "08:30pm - 09:00pm", "09:00pm - 09:30pm", "09:30pm - 10:00pm"
    ]

    time_slot_order = {slot: i for i, slot in enumerate(time_slots)}

    st.title("🤖 AI Scheduling System")

    with st.sidebar:
        st.header("🛠️ Instructions")
        st.markdown("""
        - Upload your **TA Availability** (CSV or Excel).
        - Click **Generate Schedule**.
        - Download final schedule as **CSV** or **Excel**.
        """)
        uploaded_files = st.file_uploader(
            "Upload Availability Files",
            type=["csv", "xlsx"],
            accept_multiple_files=True
        )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Determine if this is a weekend or weekday file based on column headers
                if "Date / Time" in df.columns:
                    file_type = "weekday"
                elif "Date" in df.columns:
                    file_type = "weekend"
                else:
                    st.error("❌ Unrecognized file format. Please upload a valid Weekday or Weekend file.")
                    return

                st.session_state["file_type"] = file_type    

                with st.expander(f"📄 {uploaded_file.name} (Preview)", expanded=False):
                    st.dataframe(df, height=450, use_container_width=True)

                # Save last uploaded dataframe
                st.session_state['last_df'] = df

                # Create TA label list like "TA 1", "TA 2", ...
                ta_labels = [f"TA {i+1}" for i in range(len(df))]
                st.session_state['ta_labels'] = ta_labels


            except Exception as e:
                st.error(f"⚠️ Error loading file: {e}")

    else:
        st.info("Please upload a file to continue.")

    st.sidebar.markdown("### ❌ TA Incompatibility")

    ta_labels = st.session_state.get("ta_labels", [])

    # Initialize incompatibility list in session_state
    if "incompatible_TA_pairs" not in st.session_state:
        st.session_state["incompatible_TA_pairs"] = []

    # Two dropdowns to pick incompatible TAs
    col1, col2 = st.sidebar.columns(2)
    with col1:
        ta1 = st.selectbox("TA A", ta_labels, key="ta1_select")
    with col2:
        ta2 = st.selectbox("TA B", ta_labels, key="ta2_select")

    # Add button
    if st.sidebar.button("➕ Add Incompatible Pair"):
        idx1 = ta_labels.index(ta1)
        idx2 = ta_labels.index(ta2)
        pair = tuple(sorted((idx1, idx2)))
        if idx1 != idx2 and pair not in st.session_state["incompatible_TA_pairs"]:
            st.session_state["incompatible_TA_pairs"].append(pair)

    # Show current incompatible pairs
    if st.session_state["incompatible_TA_pairs"]:
        st.sidebar.markdown("**Current Incompatible Pairs:**")
        for pair in st.session_state["incompatible_TA_pairs"]:
            st.sidebar.markdown(f"- TA {pair[0]+1} ❌ TA {pair[1]+1}")

    # Clear all
    if st.sidebar.button("🔁 Reset All Incompatible Pairs"):
        st.session_state["incompatible_TA_pairs"] = []

    st.sidebar.markdown("### ⏱️ Custom Weekly Hour Goals (Optional)")

    if "custom_hours" not in st.session_state:
        st.session_state["custom_hours"] = {}  # key = TA index, value = slot count

    ta_labels = st.session_state.get("ta_labels", [])

    col1, col2 = st.sidebar.columns(2)
    with col1:
        selected_ta = st.selectbox("Select TA", ta_labels, key="custom_hour_ta")
    with col2:
        selected_hours = st.number_input(
            "Hours", min_value=1.5, max_value=20.0, value=10.0, step=0.5, key="custom_hour_value"
        )

    if st.sidebar.button("➕ Set Custom Hours"):
        ta_idx = ta_labels.index(selected_ta)
        slot_goal = int(selected_hours * 2)
        st.session_state["custom_hours"][ta_idx] = slot_goal

    if st.session_state["custom_hours"]:
        st.sidebar.markdown("**Current TA Hour Overrides:**")
        for ta_idx, slots in st.session_state["custom_hours"].items():
            hours = slots / 2
            st.sidebar.markdown(f"- {ta_labels[ta_idx]} → {hours:.1f} hrs")

    if st.sidebar.button("🔁 Reset All Custom Hours"):
        st.session_state["custom_hours"] = {}

    st.sidebar.markdown("### 👥 TA Coverage Targets")

    peak_target = st.sidebar.selectbox(
        "Peak hours – required # of TAs:",
        options=[3, 4, 5, 6],
        index=2,  # default to 5
        key="peak_target"
    )

    nonpeak_target = st.sidebar.selectbox(
        "Non-peak hours – required # of TAs:",
        options=[3, 4, 5, 6],
        index=0,  # default to 3
        key="nonpeak_target"
    )

    st.sidebar.markdown("### ⏲️ Customize Peak Time Slots")

    col1, col2 = st.sidebar.columns(2)
    peak_start = col1.selectbox("Peak Start (24h)", list(range(8, 23)), index=0)
    peak_end = col2.selectbox("Peak End (24h)", list(range(9, 24)), index=10)

    # Sanity check
    if peak_end <= peak_start:
        st.sidebar.error("End time must be after start time.")
        st.stop()

    custom_peak_range = (peak_start, peak_end)

    

    st.sidebar.markdown("### 📅 Weeks with No Schedule (Spring Break, Holidays)")

    spring_break_weeks = st.sidebar.text_input(
        "Enter Week Numbers (comma separated)", 
        placeholder="e.g., 9,12", 
        help="Enter week numbers where no schedule should be generated, separated by commas."
    )



    # --- Generate Button ---
    if 'last_df' in st.session_state:
        if st.button("🚀 Generate TA Schedule", use_container_width=True):
            with st.spinner('🧠 Solving optimization... please wait...'):
                time.sleep(0.5)  # fake load to show spinner
                df = st.session_state['last_df']
                file_type = st.session_state.get("file_type", "weekday")

                # 🔁 Step 2: Convert peak hour range to time slot indices
                start_peak, end_peak = custom_peak_range
                all_times = [
                    "08:00am", "08:30am", "09:00am", "09:30am",
                    "10:00am", "10:30am", "11:00am", "11:30am",
                    "12:00pm", "12:30pm", "01:00pm", "01:30pm",
                    "02:00pm", "02:30pm", "03:00pm", "03:30pm",
                    "04:00pm", "04:30pm", "05:00pm", "05:30pm",
                    "06:00pm", "06:30pm", "07:00pm", "07:30pm",
                    "08:00pm", "08:30pm", "09:00pm", "09:30pm"
                ]
                hour_from_slot = {
                    i: int(t.split(":")[0]) + (12 if "pm" in t and "12" not in t else 0)
                    for i, t in enumerate(all_times)
                }
                peak_slots = [i for i, hr in hour_from_slot.items() if start_peak <= hr < end_peak]

                # Read the spring break weeks input
                if spring_break_weeks:
                    try:
                        no_schedule_weeks = [int(w.strip()) for w in spring_break_weeks.split(",") if w.strip().isdigit()]
                    except Exception:
                        no_schedule_weeks = []
                        st.sidebar.error("Invalid week format! Please enter numbers separated by commas.")
                else:
                    no_schedule_weeks = []


                if file_type == "weekday":
                    shift_requests, all_TAs, all_days, all_30minIncrements, preference_map = parse_availability_schej(df)
                    incompat = st.session_state.get("incompatible_TA_pairs", [])
                    custom_hours = st.session_state.get("custom_hours", {})
                    schedule_df = run_solver(
                        shift_requests, all_TAs, all_days, all_30minIncrements,
                        incompat, custom_hour_goals=custom_hours,
                        peak_required=peak_target, nonpeak_required=nonpeak_target,
                        peak_slots=peak_slots
                    )


                elif file_type == "weekend":
                    shift_requests, all_TAs, all_weeks, all_shifts, preference_map = parse_weekend_availability_schej(df)

                    # Your weekend solver goes here instead of run_solver
                    schedule_df = run_weekend_solver(
                        shift_requests, all_TAs, all_weeks, all_shifts, no_schedule_weeks=no_schedule_weeks
                    )


                else:
                    st.error("❌ Unknown file type.")
                    return

                # print("\n🔍 TA availability per day:")
                # day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                # for d, day in enumerate(day_names):
                #     ta_available = sum(
                #         any(slot != -2 for slot in shift_requests[n][d])
                #         for n in all_TAs
                #     )
                #     print(f"{day}: {ta_available} TAs available")

                incompat = st.session_state.get("incompatible_TA_pairs", [])
                custom_hours = st.session_state.get("custom_hours", {})
                #schedule_df = run_solver(shift_requests, all_TAs, all_days, all_30minIncrements, incompat, custom_hour_goals=custom_hours, peak_required=peak_target, nonpeak_required=peak_target,)


            if "Error" in schedule_df.columns:
                st.error(schedule_df["Error"][0])
            else:
                st.success("✅ Schedule generated!")

                if file_type == "weekend":
                    st.subheader("📋 Final Weekend Schedule")

                    week_nums = sorted(schedule_df["Week"].unique())
                    for w in week_nums:
                        week_df = schedule_df[schedule_df["Week"] == w]
                        with st.expander(f"🗓️ Week {w}"):
                            # Group shifts → then sort Friday, Saturday, Sunday
                            grouped = (
                                week_df.groupby("Shift")
                                .apply(lambda g: ", ".join(sorted(g["TA"].tolist(), key=lambda x: int(x.split()[1]))))
                                .reset_index()
                                .rename(columns={0: "TAs"})
                            )

                            # # Optional: sort TA numerically (TA 1, TA 2, ..., TA 28)
                            # grouped["TA_num"] = grouped["TA"].str.extract(r'TA (\d+)').astype(int)
                            # grouped = grouped.sort_values("TA_num").drop(columns="TA_num").reset_index(drop=True)


                            # Sort Friday → Saturday → Sunday
                            shift_order = {"Friday (6–10pm)": 0, "Saturday (12–4pm)": 1, "Sunday (12–4pm)": 2}
                            grouped["ShiftOrder"] = grouped["Shift"].map(shift_order)
                            grouped = grouped.sort_values("ShiftOrder").drop(columns="ShiftOrder").reset_index(drop=True)

                            st.dataframe(grouped, use_container_width=True, height=300)

                            csv_bytes = grouped.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label=f"⬇️ Download Week {w} Schedule as CSV",
                                data=csv_bytes,
                                file_name=f"Week_{w}_Weekend_Schedule.csv",
                                mime="text/csv",
                                use_container_width=True
                            )


                if file_type == "weekday":
                    st.subheader("📋 Final Schedule (Per Day View & Downloads)")

                    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                    for day in days:
                        day_df = schedule_df[schedule_df["Day"] == day]
                        with st.expander(f"📅 {day}"):
                            if day_df.empty:
                                st.markdown("❌ No TAs scheduled on this day.")
                            else:
                                # (existing logic to group by TA and show time slots)
                                grouped = (
                                    day_df.groupby("TA")["Time Slot"]
                                    .apply(lambda x: ", ".join(sorted(x, key=lambda t: time_slot_order[t.replace(" (If Needed)", "")])))
                                    .reset_index()
                                    .rename(columns={"Time Slot": "Time Slots"})
                                )

                            # Sort TAs by number (e.g., TA 1, TA 2, ..., TA 10) so the display is ordered
                            grouped["TA_num"] = grouped["TA"].str.extract(r'TA (\d+)').astype(int)
                            grouped = grouped.sort_values("TA_num").drop(columns="TA_num").reset_index(drop=True)


                            st.dataframe(grouped, use_container_width=True, height=500)

                            # Download CSV
                            csv_bytes = grouped.to_csv(index=False).encode('utf-8')
                            st.download_button(
                                label=f"⬇️ Download {day} Schedule as CSV",
                                data=csv_bytes,
                                file_name=f"{day}_Schedule.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                            # Download Excel
                            excel_file = f"{day}_Schedule.xlsx"
                            excel_buffer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
                            grouped.to_excel(excel_buffer, index=False, sheet_name=day)
                            excel_buffer.close()
                            with open(excel_file, 'rb') as f:
                                st.download_button(
                                    label=f"⬇️ Download {day} Schedule as Excel",
                                    data=f,
                                    file_name=excel_file,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )




                # Download Buttons
                csv = schedule_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=csv,
                    file_name="TA_Schedule.csv",
                    mime="text/csv",
                    use_container_width=True
                )

                excel_buffer = pd.ExcelWriter('schedule.xlsx', engine='xlsxwriter')
                schedule_df.to_excel(excel_buffer, index=False, sheet_name='Schedule')
                excel_buffer.close()
                with open('schedule.xlsx', 'rb') as f:
                    st.download_button(
                        label="⬇️ Download as Excel",
                        data=f,
                        file_name="TA_Schedule.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

from datetime import datetime

def parse_availability_schej(df):
    all_TAs = list(range(len(df.columns) - 1))  # Exclude 'Date / Time' column
    all_days = list(range(7))  # Monday=0 to Sunday=6
    all_30minIncrements = list(range(28))  # 8:00 AM to 10:00 PM

    shift_requests = [[[ -2 for _ in all_30minIncrements] for _ in all_days] for _ in all_TAs]
    preference_map = {}  # ⬅️ NEW dictionary to store preference labels

    time_slots = [
        "08:00am", "08:30am", "09:00am", "09:30am",
        "10:00am", "10:30am", "11:00am", "11:30am",
        "12:00pm", "12:30pm", "01:00pm", "01:30pm",
        "02:00pm", "02:30pm", "03:00pm", "03:30pm",
        "04:00pm", "04:30pm", "05:00pm", "05:30pm",
        "06:00pm", "06:30pm", "07:00pm", "07:30pm",
        "08:00pm", "08:30pm", "09:00pm", "09:30pm"
    ]
    time_slot_index = {t: i for i, t in enumerate(time_slots)}

    for index, row in df.iterrows():
        dt_str = row["Date / Time"]
        try:
            dt = datetime.strptime(dt_str, "%m/%d/%Y, %I:%M:%S %p")
        except ValueError:
            continue

        day_index = dt.weekday()
        hour = dt.hour
        minute = dt.minute
        am_pm = "am" if hour < 12 else "pm"
        hour_display = hour if 1 <= hour <= 12 else (hour - 12 if hour > 12 else 12)
        if hour_display < 10:
            hour_display = f"0{hour_display}"
        minute_display = f"{minute:02d}"
        slot_key = f"{hour_display}:{minute_display}{am_pm}"

        if slot_key not in time_slot_index:
            continue

        slot_idx = time_slot_index[slot_key]

        for ta_idx, value in enumerate(row[1:]):
            if pd.isna(value):
                score = -2
            elif "available" in str(value).lower():
                score = 4
                preference_map[(ta_idx, day_index, slot_idx)] = "Available"
            elif "if needed" in str(value).lower():
                score = 2
                preference_map[(ta_idx, day_index, slot_idx)] = "If Needed"
            else:
                score = -2

            shift_requests[ta_idx][day_index][slot_idx] = score

    return shift_requests, all_TAs, all_days, all_30minIncrements, preference_map


def parse_weekend_availability_schej(df):
    """
    Parse weekend Schej availability.
    Input df: DataFrame with columns: 'Date', TA1, TA2, ..., TAn
    Rows: Each date (Friday, Saturday, Sunday), values: 'Available', 'If needed', or blank
    Output: 
        - shift_requests[n][w][s]: score for TA n, week w, shift s
        - all_TAs, all_weeks, all_shifts
        - preference_map (optional)
    """

    # Identify TAs
    ta_cols = [c for c in df.columns if c.startswith("TA")]
    all_TAs = list(range(len(ta_cols)))
    
    # Map date to week/shift (Friday=0, Saturday=1, Sunday=2)
    # Make a sorted list of unique weekend dates
    date_objs = [datetime.strptime(d, "%m/%d/%Y") for d in df["Date"]]
    unique_weeks = sorted(set([(d.year, d.isocalendar()[1]) for d in date_objs]))
    week_lookup = {wk: i for i, wk in enumerate(unique_weeks)}
    num_weeks = len(unique_weeks)
    num_shifts = 3  # Fri evening, Sat, Sun
    
    # Set up
    shift_requests = [[[ -2 for _ in range(num_shifts)] for _ in range(num_weeks)] for _ in all_TAs]
    preference_map = {}
    
    for idx, row in df.iterrows():
        d = datetime.strptime(row["Date"], "%m/%d/%Y")
        week_id = week_lookup[(d.year, d.isocalendar()[1])]
        # Map day to shift index: Friday=0, Saturday=1, Sunday=2
        dow = d.weekday()
        if dow == 4: shift_idx = 0  # Friday
        elif dow == 5: shift_idx = 1  # Saturday
        elif dow == 6: shift_idx = 2  # Sunday
        else: continue  # skip unexpected days

        for ta_idx, col in enumerate(ta_cols):
            value = str(row[col]).lower() if not pd.isna(row[col]) else ""
            if "available" in value:
                score = 4
                preference_map[(ta_idx, week_id, shift_idx)] = "Available"
            elif "if needed" in value:
                score = 2
                preference_map[(ta_idx, week_id, shift_idx)] = "If Needed"
            else:
                score = -2
            shift_requests[ta_idx][week_id][shift_idx] = score

    all_weeks = list(range(num_weeks))
    all_shifts = list(range(num_shifts))

    return shift_requests, all_TAs, all_weeks, all_shifts, preference_map



# #Availability Parsing
# def parse_availability(df):
#     all_TAs = list(range(len(df)))
#     all_days = list(range(7))
#     all_30minIncrements = list(range(28))

#     shift_requests = [[[ -2 for _ in all_30minIncrements] for _ in all_days] for _ in all_TAs]

#     time_slots = [
#         "08:00am - 08:30am", "08:30am - 09:00am", "09:00am - 09:30am", "09:30am - 10:00am",
#         "10:00am - 10:30am", "10:30am - 11:00am", "11:00am - 11:30am", "11:30am - 12:00pm",
#         "12:00pm - 12:30pm", "12:30pm - 01:00pm", "01:00pm - 01:30pm", "01:30pm - 02:00pm",
#         "02:00pm - 02:30pm", "02:30pm - 03:00pm", "03:00pm - 03:30pm", "03:30pm - 04:00pm",
#         "04:00pm - 04:30pm", "04:30pm - 05:00pm", "05:00pm - 05:30pm", "05:30pm - 06:00pm",
#         "06:00pm - 06:30pm", "06:30pm - 07:00pm", "07:00pm - 07:30pm", "07:30pm - 08:00pm",
#         "08:00pm - 08:30pm", "08:30pm - 09:00pm", "09:00pm - 09:30pm", "09:30pm - 10:00pm"
#     ]

#     day_columns = ["Monday Question", "Tuesday Question", "Wednesday Question", "Thursday Question", "Friday Question", "Saturday Question", "Sunday Question"]

#     for n, row in df.iterrows():
#         for d, day in enumerate(day_columns):
#             available_times = str(row[day])
#             for s, slot in enumerate(time_slots):
#                 if slot in available_times:
#                     shift_requests[n][d][s] = 4
#                 else:
#                     shift_requests[n][d][s] = -2

#     return shift_requests, all_TAs, all_days, all_30minIncrements

#Solver
def run_solver(shift_requests, all_TAs, all_days, all_30minIncrements,
               incompatible_TA_pairs=[], custom_hour_goals={},
               peak_required=5, nonpeak_required=3, peak_slots=None):

    num_TAs = len(all_TAs)
    mon_thu = [0, 1, 2, 3]
    friday = 4
    if peak_slots is None:
        peak_slots = list(range(20))  # fallback default

    all_slots = list(range(28))
    offpeak_slots = [s for s in all_slots if s not in peak_slots]

    max_peakTAs = 6
    max_nonpeakTAs = 3
    min_week = 10
    max_week = 30
    min_day = 0
    max_day = 8
    friday_day = 4
    saturday_day = 5
    sunday_day = 6

    # Weekend shifts: 12:00pm to 4:00pm
    weekend_slots = list(range(16, 20))

    # Friday evening shift: 6:00pm to 10:00pm
    friday_evening_slots = list(range(20, 28))

    model = cp_model.CpModel()

    shifts = {}
    for n in all_TAs:
        for d in all_days:
            for s in all_30minIncrements:
                shifts[(n, d, s)] = model.new_bool_var(f"shift_n{n}_d{d}_s{s}")
                if shift_requests[n][d][s] == -2:
                    model.Add(shifts[(n, d, s)] == 0)

    # Ensure minimum 1.5-hour (3-slot) shift per day per TA if working that day
    for n in all_TAs:
        for d in all_days:
            assigned = [shifts[(n, d, s)] for s in all_30minIncrements]

            # If TA works at least once on day d...
            works_today = model.NewBoolVar(f"works_n{n}_d{d}")
            model.Add(sum(assigned) >= 1).OnlyEnforceIf(works_today)
            model.Add(sum(assigned) == 0).OnlyEnforceIf(works_today.Not())

            # Constraint: if working that day, must have at least one 3-slot block
            at_least_one_block = []
            for start in range(0, len(all_30minIncrements) - 2):
                block = model.NewBoolVar(f"block_n{n}_d{d}_s{start}")
                model.AddBoolAnd([
                    shifts[(n, d, start)],
                    shifts[(n, d, start + 1)],
                    shifts[(n, d, start + 2)]
                ]).OnlyEnforceIf(block)
                model.AddBoolOr([
                    shifts[(n, d, start)].Not(),
                    shifts[(n, d, start + 1)].Not(),
                    shifts[(n, d, start + 2)].Not()
                ]).OnlyEnforceIf(block.Not())
                at_least_one_block.append(block)

            # If they work today, require at least one valid block
            model.AddBoolOr(at_least_one_block).OnlyEnforceIf(works_today)

    
    # Incompatible TA constraints: no overlap OR adjacent overlap
    for (ta1, ta2) in incompatible_TA_pairs:
        for d in all_days:
            for s in all_30minIncrements:
                # TA1 works at s => TA2 cannot work at s-1, s, s+1
                neighbors = [s]
                if s > 0:
                    neighbors.append(s - 1)
                if s < len(all_30minIncrements) - 1:
                    neighbors.append(s + 1)

                for neighbor_s in neighbors:
                    model.Add(shifts[(ta1, d, s)] + shifts[(ta2, d, neighbor_s)] <= 1)

    for n in all_TAs:
        for s in offpeak_slots:
            model.Add(shifts[(n, friday, s)] == 0)

    #print("🛠️ Checking available TA counts for required coverage...\n")

    for d in mon_thu:
        for s in peak_slots:
            available = [n for n in all_TAs if shift_requests[n][d][s] != -2]
            #print(f"Mon-Thu Day {d}, Slot {s}: Available TAs = {len(available)}")

    for s in peak_slots:
        available = [n for n in all_TAs if shift_requests[n][friday][s] != -2]
        #print(f"Friday, Slot {s}: Available TAs = {len(available)}")

    for d in mon_thu:
        for s in offpeak_slots:
            available = [n for n in all_TAs if shift_requests[n][d][s] != -2]
            #print(f"Mon-Thu Day {d}, Offpeak Slot {s}: Available TAs = {len(available)}")


    for s in peak_slots:
        model.Add(sum(shifts[(n, friday, s)] for n in all_TAs) <= max_peakTAs)

    # Friday evening shift: max 6 TAs
    for s in friday_evening_slots:
        model.Add(sum(shifts[(n, friday_day, s)] for n in all_TAs) <= max_peakTAs)

    # Saturday and Sunday (12pm–4pm): max 4 TAs each
    for s in weekend_slots:
        model.Add(sum(shifts[(n, saturday_day, s)] for n in all_TAs) <= 4)
        model.Add(sum(shifts[(n, sunday_day, s)] for n in all_TAs) <= 4)


    DEFAULT_GOAL = 10 * 2  # 10 hours = 20 slots

    for n in all_TAs:
        goal = custom_hour_goals.get(n, DEFAULT_GOAL)
        weekly_sum = sum(shifts[(n, d, s)] for d in all_days for s in all_30minIncrements)

        model.Add(weekly_sum <= goal)
        model.Add(weekly_sum >= min(goal - 4, goal))  # allow 2-hour slack (4 slots)

    model.Maximize(
        # Respect TA preferences
        sum(shifts[(n, d, s)] * shift_requests[n][d][s]
            for n in all_TAs for d in all_days for s in all_30minIncrements)

        # Bonus: Reward any assignments in peak slots
        + sum(shifts[(n, d, s)] * 10
            for n in all_TAs for d in mon_thu + [friday] for s in peak_slots)

        # Bonus: Encourage using Monday and Friday overall
        + sum(shifts[(n, d, s)] * 2
            for n in all_TAs for d in [0, 4] for s in all_30minIncrements)
    )


    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return pd.DataFrame({"Error": ["No feasible schedule found."]})

    output = []
    preference_map = {
        (n, d, s): shift_requests[n][d][s]
        for n in all_TAs for d in all_days for s in all_30minIncrements
    }

    time_slots = [
        "08:00am - 08:30am", "08:30am - 09:00am", "09:00am - 09:30am", "09:30am - 10:00am",
        "10:00am - 10:30am", "10:30am - 11:00am", "11:00am - 11:30am", "11:30am - 12:00pm",
        "12:00pm - 12:30pm", "12:30pm - 01:00pm", "01:00pm - 01:30pm", "01:30pm - 02:00pm",
        "02:00pm - 02:30pm", "02:30pm - 03:00pm", "03:00pm - 03:30pm", "03:30pm - 04:00pm",
        "04:00pm - 04:30pm", "04:30pm - 05:00pm", "05:00pm - 05:30pm", "05:30pm - 06:00pm",
        "06:00pm - 06:30pm", "06:30pm - 07:00pm", "07:00pm - 07:30pm", "07:30pm - 08:00pm",
        "08:00pm - 08:30pm", "08:30pm - 09:00pm", "09:00pm - 09:30pm", "09:30pm - 10:00pm"
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for n in all_TAs:
        for d in all_days:
            for s in all_30minIncrements:
                if solver.Value(shifts[(n, d, s)]) == 1:
                    status = preference_map.get((n, d, s), -2)
                    label = " (If Needed)" if status == 2 else ""  # Only mark if it's "If Needed"
                    output.append({
                        "TA": f"TA {n+1}",
                        "Day": days[d],
                        "Time Slot": f"{time_slots[s]}{label}"
                    })



    # print("\n🧪 === CONSTRAINT CHECK SUMMARY ===")

    # # 1. Check hours per TA vs goal
    # print("\n📏 Weekly Hours per TA:")
    # for n in all_TAs:
    #     assigned = sum(solver.Value(shifts[(n, d, s)]) for d in all_days for s in all_30minIncrements)
    #     goal = custom_hour_goals.get(n, 20)  # default 10 hrs = 20 slots
    #     print(f"TA {n+1}: assigned {assigned/2:.1f} hrs ({assigned} slots), goal = {goal/2:.1f} hrs")

    # # 2. Check incompatible TAs
    # if incompatible_TA_pairs:
    #     print("\n🚫 Incompatible TA Pair Conflicts:")
    #     conflict_found = False
    #     for ta1, ta2 in incompatible_TA_pairs:
    #         for d in all_days:
    #             for s in all_30minIncrements:
    #                 if solver.Value(shifts[(ta1, d, s)]) + solver.Value(shifts[(ta2, d, s)]) > 1:
    #                     print(f"❌ TA {ta1+1} and TA {ta2+1} both scheduled on Day {d}, Slot {s}")
    #                     conflict_found = True
    #     if not conflict_found:
    #         print("✅ No conflicts detected")

    # # 3. Peak & Non-peak slot summary
    # print("\n📊 Slot Assignment Summary (Coverage):")
    # for d in all_days:
    #     for s in all_30minIncrements:
    #         count = sum(solver.Value(shifts[(n, d, s)]) for n in all_TAs)
    #         slot_type = "Peak" if s in peak_slots else "Non-peak"
    #         print(f"Day {d} Slot {s} ({slot_type}): {count} TAs")


    return pd.DataFrame(output)


def run_weekend_solver(shift_requests, all_TAs, all_weeks, all_shifts, no_schedule_weeks=[]):
    from ortools.sat.python import cp_model

    num_TAs = len(all_TAs)
    max_friday_TAs = 3
    max_satsun_TAs = 2
    target_shifts_x2 = 5  # 2.5 shifts × 2 because of integer math

    model = cp_model.CpModel()

    shifts = {}
    for n in all_TAs:
        for w in all_weeks:
            for s in all_shifts:
                shifts[(n, w, s)] = model.NewBoolVar(f"shift_n{n}_w{w}_s{s}")
                if shift_requests[n][w][s] == -2 or (w+1) in no_schedule_weeks:
                    model.Add(shifts[(n, w, s)] == 0)


    # Coverage constraints
    for w in all_weeks:
        if (w+1) in no_schedule_weeks:
            continue  # ⬅️ Skip this week!
        for s in [0, 1, 2]:
            available_tas = [n for n in all_TAs if shift_requests[n][w][s] != -2]
            if not available_tas:
                continue  # skip shift if no TA is available
            if s == 0:
                model.Add(sum(shifts[(n, w, s)] for n in available_tas) == max_friday_TAs)
            else:
                model.Add(sum(shifts[(n, w, s)] for n in available_tas) == max_satsun_TAs)


    # Even distribution
    diffs = []
    for n in all_TAs:
        total = sum(shifts[(n, w, s)] for w in all_weeks for s in all_shifts)
        diff = model.NewIntVar(0, len(all_weeks)*3, f"diff_{n}")
        delta = model.NewIntVar(-100, 100, f"delta_{n}")
        model.Add(delta == total * 2 - target_shifts_x2)
        model.AddAbsEquality(diff, delta)
        diffs.append(diff)

    max_diff = model.NewIntVar(0, len(all_weeks)*3, "max_diff")
    model.AddMaxEquality(max_diff, diffs)

    # Objective: prefer assignments based on availability and balance
    model.Maximize(
        sum(shifts[(n, w, s)] * shift_requests[n][w][s] for n in all_TAs for w in all_weeks for s in all_shifts)
        - max_diff * num_TAs
    )

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return pd.DataFrame({"Error": ["No feasible weekend schedule found."]})

    # Convert results to DataFrame
    output = []
    shift_names = ["Friday (6–10pm)", "Saturday (12–4pm)", "Sunday (12–4pm)"]

    for n in all_TAs:
        for w in all_weeks:
            for s in all_shifts:
                if solver.Value(shifts[(n, w, s)]) == 1:
                    output.append({
                        "TA": f"TA {n+1}",
                        "Week": w + 1,
                        "Shift": shift_names[s]
                    })

    return pd.DataFrame(output)



#Run app
if __name__ == "__main__":
    main()
