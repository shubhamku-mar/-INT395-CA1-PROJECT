import os
import base64
import importlib.util
import json
from datetime import datetime, timedelta

import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from assets.frontend_theme import inject_lpu_theme, render_top_banner, render_cinematic_footer, get_lpu_logo_url, get_lpu_campus_url


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Services - ShuttleLyze",
    page_icon="🚌",
    layout="wide",
)

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)


def first_existing_path(*paths):
    for path in paths:
        if path and os.path.exists(path):
            return path
    return None


def get_svg_data_url(svg_path):
    if not os.path.exists(svg_path):
        return None

    with open(svg_path, "r", encoding="utf-8") as file:
        svg_content = file.read()

    encoded = base64.b64encode(
        svg_content.encode("utf-8")
    ).decode("utf-8")

    return f"data:image/svg+xml;base64,{encoded}"


# ============================================================
# 2. LOCATION DATA
# ============================================================
logo_path = os.path.join(PROJECT_ROOT, "lpu-logo.svg")
logo_svg_url = get_svg_data_url(logo_path)

excel_path = first_existing_path(
    os.path.join(PROJECT_ROOT, "LPU_All_Locations.xlsx"),
    os.path.join(os.path.dirname(__file__), "LPU_All_Locations.xlsx"),
    os.path.expanduser("~/Downloads/LPU_All_Locations.xlsx"),
)


def load_location_options(path):
    fallback = [
        "1 — School of Fashion Design",
        "34 — Block 34 (CSE Dept)",
    ]

    if not path:
        return fallback

    options = []

    try:
        blocks = pd.read_excel(
            path,
            sheet_name="LPU Locations",
        )
        named = pd.read_excel(
            path,
            sheet_name="Named Locations",
        )

        if "Block / Location ID" in blocks.columns:
            blocks = blocks.rename(
                columns={"Block / Location ID": "ID"}
            )

        if "Location ID" in named.columns:
            named = named.rename(
                columns={"Location ID": "ID"}
            )

        for frame in (blocks, named):
            if {"ID", "Location Name"}.issubset(frame.columns):
                for _, row in frame.iterrows():
                    loc_id = str(row["ID"]).strip()
                    loc_name = str(row["Location Name"]).strip()

                    if (
                        loc_id.lower() != "nan"
                        and loc_name.lower() != "nan"
                    ):
                        option = f"{loc_id} — {loc_name}"

                        if option not in options:
                            options.append(option)

        return sorted(options, key=str.casefold) if options else fallback

    except Exception:
        return fallback


location_options = load_location_options(excel_path)


# ============================================================
# 3. LOAD MODEL, DATASET AND MATRICES
# ============================================================
@st.cache_resource
def load_backend_artifacts():
    model_path = first_existing_path(
        os.path.join(
            PROJECT_ROOT,
            "demand_prediction_pipeline.pkl",
        ),
        os.path.join(
            os.path.dirname(__file__),
            "demand_prediction_pipeline.pkl",
        ),
        os.path.expanduser("~/Downloads/demand_prediction_pipeline.pkl"),
    )

    master_path = first_existing_path(
        os.path.join(
            PROJECT_ROOT,
            "LPU_Transportation_Master_Dataset_10000.xlsx",
        ),
        os.path.join(
            os.path.dirname(__file__),
            "LPU_Transportation_Master_Dataset_10000.xlsx",
        ),
        os.path.expanduser(
            "~/Downloads/LPU_Transportation_Master_Dataset_10000.xlsx"
        ),
        os.path.expanduser(
            "~/Downloads/LPU_Transportation_Master_Dataset_10000 (1).xlsx"
        ),
    )

    matrix_path = first_existing_path(
        os.path.join(PROJECT_ROOT, "lpu_travel_time_model.pkl"),
        os.path.join(os.path.dirname(__file__), "lpu_travel_time_model.pkl"),
        os.path.expanduser("~/Downloads/lpu_travel_time_model.pkl"),
        os.path.join(os.path.dirname(__file__), "INT395-CA1-PROJECT", "lpu_travel_time_model.pkl"),
    )

    pipeline = None
    master_df = None
    matrices = None

    if model_path:
        try:
            pipeline = joblib.load(model_path)
        except Exception:
            pass

    if master_path:
        try:
            master_df = pd.read_excel(
                master_path,
                sheet_name="Ride Records",
            )
        except Exception:
            pass

    if matrix_path:
        try:
            matrices = joblib.load(matrix_path)
        except Exception:
            pass

    return pipeline, master_df, matrices


demand_pipeline, master_df, travel_matrices = load_backend_artifacts()


# ============================================================
# 4. DESIGN — LPU BLACK & DARK ORANGE THEME
# ============================================================
inject_lpu_theme()
render_top_banner()

st.markdown('''
<style>
.analysis-card {
    box-sizing: border-box;
    width: 100%;
    min-height: 86px;
    height: 100%;
    background: #141414;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 3px solid #FF6A00;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 0 0 10px 0;
    font-size: 13px;
    line-height: 1.55;
    color: #FFFFFF;
    overflow-wrap: anywhere;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    transition: all 0.25s ease;
}
.analysis-card b {
    display: inline-block;
    color: #FF6A00;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 3px;
}
.analysis-card:hover {
    border-color: rgba(255, 106, 0, 0.5);
    border-left-color: #FF6A00;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 106, 0, 0.15);
}
.route-badge {
    background-color: rgba(255, 106, 0, 0.12);
    color: #FF6A00;
    padding: 3px 8px;
    border: 1px solid rgba(255, 106, 0, 0.3);
    border-radius: 4px;
    font-weight: bold;
}
</style>
''', unsafe_allow_html=True)

# Floating Header Navigation
srv_logo_url = get_lpu_logo_url()
header_brand, header_spacer, header_nav = st.columns([3.2, 0.6, 6.2], gap="small", vertical_alignment="center")

with header_brand:
    srv_logo_html = f'<img src="{srv_logo_url}" style="height: 44px; width: 44px; margin-right: 14px; object-fit: contain; filter: drop-shadow(0 0 10px rgba(255,106,0,0.5));" alt="LPU Logo">' if srv_logo_url else ''
    st.markdown(f'''
    <div style="display: flex; align-items: center; height: 65px; box-sizing: border-box; padding-left: 10px;">
        {srv_logo_html}
        <div>
            <span style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 800; letter-spacing: 1.5px; line-height: 1;">
                SHUTTLE<span style="color: #FF6A00;">LYZE</span>
            </span>
            <div style="color: #B3B3B3; font-size: 10px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;">Services & Predictive AI</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

with header_nav:
    nav1, nav2, nav3, nav4, nav5 = st.columns([1.0, 1.3, 1.3, 0.9, 0.9], gap="small", vertical_alignment="center")
    with nav1:
        if st.button("Home", key="srv_nav_home", use_container_width=True):
            st.switch_page("app.py")
    with nav2:
        if st.button("Safety Hub", key="srv_nav_safety", use_container_width=True):
            if os.path.exists("pages/Safety.py"):
                st.switch_page("pages/Safety.py")
    with nav3:
        if st.button("News & Alerts", key="srv_nav_news", use_container_width=True):
            if os.path.exists("pages/News.py"):
                st.switch_page("pages/News.py")
    with nav4:
        if st.button("About", key="srv_nav_about", use_container_width=True):
            if os.path.exists("pages/About.py"):
                st.switch_page("pages/About.py")
    with nav5:
        if st.button("Contact", key="srv_nav_contact", use_container_width=True):
            if os.path.exists("pages/Contact.py"):
                st.switch_page("pages/Contact.py")

st.markdown('''
<div style="margin: 15px 0 25px 0; border-bottom: 1px solid rgba(255, 106, 0, 0.25); padding-bottom: 15px;">
    <div class="lpu-pill-badge" style="margin-bottom: 8px;">AI Transit Diagnostics & Fleet Orchestration</div>
    <h1 style="color: #FFFFFF; font-family: 'Space Grotesk', sans-serif; font-size: 30px; font-weight: 800; margin: 0; letter-spacing: -0.5px;">
        Campus Services & <span style="color: #FF6A00;">Route Analytics</span>
    </h1>
    <p style="color: #B3B3B3; font-size: 14px; margin: 8px 0 0 0; max-width: 850px;">
        Select any pickup station and destination to compute machine learning demand forecasts, travel duration estimates, operational road routing, and suggested shuttle allocation.
    </p>
</div>
''', unsafe_allow_html=True)

# ============================================================
# 6. PICKUP AND DROP INPUTS
# ============================================================
sel_col1, sel_col2 = st.columns(2, gap="medium")

with sel_col1:
    st.markdown(
        "<span style='font-size:12px;font-weight:bold;color:#333;'>"
        " Select Pickup Location</span>",
        unsafe_allow_html=True,
    )

    pickup_location = st.selectbox(
        "Pickup Location",
        location_options,
        label_visibility="collapsed",
        key="pickup_location",
    )

with sel_col2:
    st.markdown(
        "<span style='font-size:12px;font-weight:bold;color:#333;'>"
        " Select Drop Location</span>",
        unsafe_allow_html=True,
    )

    drop_location = st.selectbox(
        "Drop Location",
        location_options,
        label_visibility="collapsed",
        key="drop_location",
    )

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

run_analysis = st.button(
    " Run Complete Shuttle & Route Analysis",
    use_container_width=True,
)

st.markdown(
    f"""
    <div style="background-color:#ffffff;
                border:1px solid #e0e0e0;
                border-radius:6px;
                padding:12px 18px;
                margin-top:10px;
                margin-bottom:15px;
                font-size:12px;
                color:#333;">
        <b>Route Overview:</b>
        <span class="route-badge">{pickup_location}</span>
        →
        <span class="route-badge">{drop_location}</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 7. HELPER FUNCTIONS
# ============================================================
def split_location(option):
    parts = option.split(" — ", 1)

    return (
        parts[0].strip(),
        parts[1].strip() if len(parts) > 1 else parts[0].strip(),
    )


def numeric_mean(frame, column, default=None):
    """Calculate a real numeric mean; never replace missing data with a report value."""
    if frame is None or column not in frame.columns:
        return default

    values = pd.to_numeric(frame[column], errors="coerce").dropna()
    if values.empty:
        return default

    return float(values.mean())


def mode_value(frame, column, default="Unavailable"):
    if frame is None or column not in frame.columns:
        return default

    values = frame[column].dropna()
    if values.empty:
        return default

    return str(values.mode().iloc[0])


def infer_location_type(location_id, side, default="Academic"):
    if master_df is None:
        return default

    id_column = (
        "Pickup_Block" if side == "pickup" else "Drop_Block"
    )
    type_column = (
        "Pickup_Location_Type"
        if side == "pickup"
        else "Drop_Location_Type"
    )

    if (
        id_column in master_df.columns
        and type_column in master_df.columns
    ):
        matches = master_df[
            master_df[id_column].astype(str).str.strip()
            == str(location_id).strip()
        ][type_column].dropna()

        if not matches.empty:
            return str(matches.mode().iloc[0])

    return default


def make_demand_input(
    pickup,
    drop,
    distance_m=500.0,
    travel_time_min=3.0,
    traffic_level="Medium",
    weather="Normal",
    peak_hour="Yes",
    vehicle_capacity=None,
):
    now = datetime.now()
    hour = now.hour

    if 6 <= hour < 12:
        time_slot = "Morning"
    elif 12 <= hour < 17:
        time_slot = "Afternoon"
    elif 17 <= hour < 21:
        time_slot = "Evening"
    else:
        time_slot = "Night"

    return pd.DataFrame([{
        "Pickup_Block": str(pickup["ID"]),
        "Pickup_Location_Name": str(pickup["Name"]),
        "Pickup_Location_Type": str(pickup["Type"]),
        "Drop_Block": str(drop["ID"]),
        "Drop_Location_Name": str(drop["Name"]),
        "Drop_Location_Type": str(drop["Type"]),
        "Route": f"{pickup['ID']} → {drop['ID']}",
        "Day_of_Week": now.strftime("%A"),
        "Is_Weekend": "Yes" if now.weekday() >= 5 else "No",
        "Month": now.strftime("%B"),
        "Week_Number": int(now.isocalendar().week),
        "Hour": int(hour),
        "Start_Time": now.strftime("%H:%M"),
        "Time_Slot": (
            "Morning" if 6 <= hour < 12 else
            "Afternoon" if 12 <= hour < 17 else
            "Evening" if 17 <= hour < 21 else "Night"
        ),
        "Weather": str(weather),
        "Traffic_Level": str(traffic_level),
        "Peak_Hour": str(peak_hour),
        "Demand_Level": "High",
        "Distance_m": float(distance_m),
        "Travel_Time_Min": float(travel_time_min),
        "Vehicle_Capacity": vehicle_capacity,
        "Vehicle_ID": "V001",
    }])


def predict_route_demand(
    pickup,
    drop,
    distance_m=500.0,
    travel_time_min=3.0,
    traffic_level="Medium",
    weather="Normal",
    peak_hour="Yes",
    vehicle_capacity=None,
):
    """Return only the saved model's prediction; do not substitute historical averages."""
    if demand_pipeline is None:
        return None, "Saved demand model could not be loaded"

    try:
        model_input = make_demand_input(
            pickup, drop, distance_m, travel_time_min,
            traffic_level, weather, peak_hour, vehicle_capacity
        )
        result = demand_pipeline.predict(model_input)[0]
        return max(0.0, float(result)), "Saved demand_prediction_pipeline.pkl"
    except Exception as exc:
        return None, f"Model prediction failed: {type(exc).__name__}: {exc}"


def resolve_matrix_location(location_id, location_name, matrix):
    """Match the selected dropdown option to a saved matrix index/column."""
    if matrix is None:
        return None

    keys = list(matrix.index)
    normalized = {str(key).strip().casefold(): key for key in keys}

    candidates = [str(location_id).strip(), str(location_name).strip()]
    for candidate in candidates:
        if candidate.casefold() in normalized:
            return normalized[candidate.casefold()]

    # Some workbooks use numeric-looking IDs with a .0 suffix.
    for candidate in candidates:
        candidate_clean = candidate.removesuffix(".0").casefold()
        for key in keys:
            key_clean = str(key).strip().removesuffix(".0").casefold()
            if candidate_clean == key_clean:
                return key

    return None


def get_matrix_travel_result(pickup_id, pickup_name, drop_id, drop_name, matrices):
    """Read the actual saved distance and travel-time matrices."""
    if not isinstance(matrices, dict):
        return None, None, "Saved travel-time matrices could not be loaded."

    distance_matrix = matrices.get("distance_matrix")
    time_matrix = matrices.get("travel_time_matrix")

    if distance_matrix is None or time_matrix is None:
        return None, None, "The saved file does not contain both required matrices."

    pickup_distance_key = resolve_matrix_location(
        pickup_id, pickup_name, distance_matrix
    )
    drop_distance_key = resolve_matrix_location(
        drop_id, drop_name, distance_matrix.T
    )
    pickup_time_key = resolve_matrix_location(
        pickup_id, pickup_name, time_matrix
    )
    drop_time_key = resolve_matrix_location(
        drop_id, drop_name, time_matrix.T
    )

    if any(value is None for value in (
        pickup_distance_key, drop_distance_key, pickup_time_key, drop_time_key
    )):
        return None, None, (
            "One or both selected locations are not present in the saved matrices. "
            "Check that the selected location IDs/names match the matrix labels."
        )

    try:
        distance = float(distance_matrix.loc[pickup_distance_key, drop_distance_key])
        travel_time = float(time_matrix.loc[pickup_time_key, drop_time_key])
    except (KeyError, TypeError, ValueError, IndexError):
        return None, None, "Distance or travel time could not be read for this route."

    if pd.isna(distance) or pd.isna(travel_time) or distance < 0 or travel_time < 0:
        return None, None, "Distance or travel time is unavailable for this route."

    return distance, travel_time, None


def load_routefinder():
    candidates = [
        os.path.join(
            PROJECT_ROOT,
            "Route_Recommendation",
            "routefinder.py",
        ),
        os.path.join(
            os.path.dirname(__file__),
            "Route_Recommendation",
            "routefinder.py",
        ),
        os.path.join(PROJECT_ROOT, "routefinder.py"),
    ]

    script = next(
        (path for path in candidates if os.path.exists(path)),
        None,
    )

    if not script:
        return None

    spec = importlib.util.spec_from_file_location(
        "shuttlelyze_routefinder",
        script,
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if excel_path and hasattr(module, "EXCEL_FILE"):
        module.EXCEL_FILE = excel_path

    return module


# ============================================================
# 8. RUN ANALYSIS — MODEL OUTPUT + THE RUNNER'S 10 REPORT VALUES
# ============================================================
if run_analysis:

    if pickup_location == drop_location:
        st.warning("Please select two different pickup and drop locations.")
        st.stop()

    pickup_id, pickup_name = split_location(pickup_location)
    drop_id, drop_name = split_location(drop_location)
    route_str = f"{pickup_id} → {drop_id}"

    # Find history for the selected route. If the route has no matching
    # rows, use the actual campus dataset, as the original runner does.
    route_data = None
    if master_df is not None:
        if "Route" in master_df.columns:
            route_data = master_df[
                master_df["Route"].astype(str).str.strip() == route_str
            ].copy()

        if (
            (route_data is None or route_data.empty)
            and {"Pickup_Block", "Drop_Block"}.issubset(master_df.columns)
        ):
            route_data = master_df[
                (master_df["Pickup_Block"].astype(str).str.strip() == pickup_id)
                & (master_df["Drop_Block"].astype(str).str.strip() == drop_id)
            ].copy()

    route_match_count = len(route_data) if route_data is not None else 0
    report_data = (
        route_data if route_data is not None and not route_data.empty
        else master_df
    )

    # Actual data-derived values for the runner's report. No hardcoded
    # 9.74 / 2.97 / 513.91 / 7208 / 2792 / 89.09 substitutions.
    historical_records = len(report_data) if report_data is not None else None
    avg_passengers = numeric_mean(report_data, "Passengers")
    avg_travel_time = numeric_mean(report_data, "Travel_Time_Min")
    avg_distance = numeric_mean(report_data, "Distance_m")
    traffic = mode_value(report_data, "Traffic_Level")
    weather = mode_value(report_data, "Weather")
    avg_utilization = numeric_mean(report_data, "Vehicle_Utilization_Percent")
    peak_day = mode_value(report_data, "Day_of_Week")

    if report_data is not None and "Peak_Hour" in report_data.columns:
        peak_values = report_data["Peak_Hour"].astype(str).str.strip().str.casefold()
        peak_yes_count = int(peak_values.isin(["yes", "true", "1"]).sum())
        peak_no_count = int(peak_values.isin(["no", "false", "0"]).sum())
    else:
        peak_yes_count = None
        peak_no_count = None

    # Determine the operational tier from actual dataset demand labels when
    # available; otherwise compare the passenger average with data-derived
    # quartiles instead of using a fixed passenger threshold.
    traffic_tier = "Unavailable — passenger data missing"
    if report_data is not None and "Demand_Level" in report_data.columns:
        demand_labels = report_data["Demand_Level"].dropna().astype(str).str.strip()
        if not demand_labels.empty:
            label = demand_labels.mode().iloc[0].casefold()
            if "critical" in label or "very high" in label:
                traffic_tier = "High Demand (Critical)"
            elif "high" in label:
                traffic_tier = "High Demand"
            elif "low" in label:
                traffic_tier = "Low Demand"
            elif "moderate" in label or "medium" in label or "normal" in label:
                traffic_tier = "Moderate Demand (Normal)"
            else:
                traffic_tier = str(demand_labels.mode().iloc[0])

    if traffic_tier == "Unavailable — passenger data missing" and avg_passengers is not None:
        passenger_values = (
            pd.to_numeric(report_data["Passengers"], errors="coerce").dropna()
            if report_data is not None and "Passengers" in report_data.columns
            else pd.Series(dtype=float)
        )
        if not passenger_values.empty:
            low_cutoff = float(passenger_values.quantile(0.25))
            high_cutoff = float(passenger_values.quantile(0.75))
            if avg_passengers <= low_cutoff:
                traffic_tier = "Low Demand"
            elif avg_passengers >= high_cutoff:
                traffic_tier = "High Demand (Critical)"
            else:
                traffic_tier = "Moderate Demand (Normal)"
        else:
            traffic_tier = "Unavailable — passenger data missing"

    def show_number(value, suffix="", decimals=2):
        if value is None or pd.isna(value):
            return "Unavailable"
        return f"{value:,.{decimals}f}{suffix}"

    # Fixed values are used only as model-input defaults when no historical
    # value exists. They are never shown as historical report results.
    model_distance = avg_distance if avg_distance is not None else 500.0
    model_travel_time = avg_travel_time if avg_travel_time is not None else 3.0
    model_traffic = traffic if traffic != "Unavailable" else "Medium"
    model_weather = weather if weather != "Unavailable" else "Normal"
    model_peak = (
        "Yes" if peak_yes_count and peak_yes_count > 0
        else "No" if peak_no_count and peak_no_count > 0
        else "Yes"
    )

    # Use an observed capacity value from the loaded dataset for model input;
    # do not assume a fixed 30-passenger shuttle. If unavailable, let prediction
    # fail safely and use route-specific historical demand for the recommendation.
    model_vehicle_capacity = numeric_mean(master_df, "Vehicle_Capacity")

    route_demand, route_demand_source = predict_route_demand(
        {
            "ID": pickup_id,
            "Name": pickup_name,
            "Type": infer_location_type(pickup_id, "pickup"),
        },
        {
            "ID": drop_id,
            "Name": drop_name,
            "Type": infer_location_type(drop_id, "drop"),
        },
        distance_m=model_distance,
        travel_time_min=model_travel_time,
        traffic_level=model_traffic,
        weather=model_weather,
        peak_hour=model_peak,
        vehicle_capacity=model_vehicle_capacity,
    )

    # --------------------------------------------------------
    # Route map / OSRM results
    # THIS MAP/OSRM BLOCK IS KEPT UNCHANGED.
    # --------------------------------------------------------
    routes = []
    shortest = None
    fastest = None
    route_map_html = None
    route_map_error = None

    try:
        routefinder = load_routefinder()

        if routefinder is None:
            route_map_error = "Route finder script not found."
        else:
            route_locations = routefinder.load_locations()

            start = routefinder.find_location(
                pickup_id,
                route_locations,
            )
            end = routefinder.find_location(
                drop_id,
                route_locations,
            )

            routes = routefinder.get_routes(start, end)

            campus_map, shortest, fastest = (
                routefinder.create_map(start, end, routes)
            )

            map_path = os.path.join(
                PROJECT_ROOT,
                "lpu_route_map.html",
            )

            campus_map.save(map_path)

            with open(map_path, "r", encoding="utf-8") as map_file:
                route_map_html = map_file.read()

    except Exception as exc:
        route_map_error = str(exc)

    # --------------------------------------------------------
    # Distance and travel-time matrices
    # THIS MATRIX/MAP SUPPORT BLOCK IS KEPT UNCHANGED.
    # --------------------------------------------------------
    matrix_distance = None
    matrix_time = None

    if travel_matrices:
        try:
            distance_matrix = travel_matrices.get("distance_matrix")
            time_matrix = travel_matrices.get("travel_time_matrix")

            if distance_matrix is not None and time_matrix is not None:
                distance_keys = {
                    str(value).strip(): value for value in distance_matrix.index
                }
                time_keys = {
                    str(value).strip(): value for value in time_matrix.index
                }
                distance_columns = {
                    str(value).strip(): value for value in distance_matrix.columns
                }
                time_columns = {
                    str(value).strip(): value for value in time_matrix.columns
                }

                if pickup_id in distance_keys and drop_id in distance_columns:
                    matrix_distance = float(
                        distance_matrix.loc[
                            distance_keys[pickup_id], distance_columns[drop_id]
                        ]
                    )

                if pickup_id in time_keys and drop_id in time_columns:
                    matrix_time = float(
                        time_matrix.loc[
                            time_keys[pickup_id], time_columns[drop_id]
                        ]
                    )

        except Exception:
            matrix_distance = None
            matrix_time = None

    if (
        matrix_distance is not None
        and pd.notna(matrix_distance)
        and matrix_distance >= 0
    ):
        distance_used = matrix_distance
        distance_source = "Saved distance matrix"
    elif fastest is not None:
        distance_used = float(fastest["distance"])
        distance_source = "OSRM route result"
    else:
        distance_used = avg_distance if avg_distance is not None else 500.0
        distance_source = (
            "Historical dataset" if avg_distance is not None
            else "Default used for map-related fallback only"
        )

    if (
        matrix_time is not None
        and pd.notna(matrix_time)
        and matrix_time >= 0
    ):
        travel_time_used = matrix_time
        time_source = "Saved travel-time matrix"
    elif fastest is not None:
        travel_time_used = float(fastest["duration"]) / 60.0
        time_source = "OSRM fastest-route estimate"
    else:
        travel_time_used = (
            avg_travel_time if avg_travel_time is not None else 3.0
        )
        time_source = (
            "Historical dataset" if avg_travel_time is not None
            else "Default used for map-related fallback only"
        )

    # --------------------------------------------------------
    # DISPLAY ONLY THE SAVED MODEL PREDICTION, THE 10 REPORT
    # VALUES FROM THE RUNNER, AND THE EXISTING MAP.
    # --------------------------------------------------------

    analytics_col, map_col = st.columns([1.15, 1], gap="large")

    with analytics_col:
        st.caption(f"{pickup_name} → {drop_name}")

        # New travel-time model output. This reads the saved matrices directly;
        # it does not train a model or use hardcoded travel results.
        matrix_distance_result, matrix_time_result, matrix_result_error = (
            get_matrix_travel_result(
                pickup_id,
                pickup_name,
                drop_id,
                drop_name,
                travel_matrices,
            )
        )

        if matrix_result_error:
            st.warning(matrix_result_error)
        else:
            travel_result_columns = st.columns(2, gap="small")
            with travel_result_columns[0]:
                st.markdown(
                    '<div class="analysis-card"><b>Pickup Location</b><br>'
                    f'{pickup_name}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="analysis-card"><b>Distance</b><br>'
                    f'{matrix_distance_result:,.2f} meters<br>'
                    f'{matrix_distance_result / 1000:.3f} km</div>',
                    unsafe_allow_html=True,
                )
            with travel_result_columns[1]:
                st.markdown(
                    '<div class="analysis-card"><b>Drop Location</b><br>'
                    f'{drop_name}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    '<div class="analysis-card"><b>Estimated Travel Time</b><br>'
                    f'{matrix_time_result:.2f} minutes</div>',
                    unsafe_allow_html=True,
                )


        if master_df is None:
            st.error(
                "The transportation Excel dataset could not be loaded. "
                "Historical report values are shown as Unavailable. "
                "Check the dataset path and the 'Ride Records' sheet."
            )
        elif report_data is master_df and route_match_count == 0:
            st.info(
                "No historical rows matched this exact route. "
                "The report below uses the loaded campus-wide dataset."
            )

        report_items = [
            (
                "1. Total Historical Trips Recorded",
                f"{historical_records:,} ride records"
                if historical_records is not None else "Unavailable",
            ),
            (
                "2. Average Passenger Load per Trip",
                show_number(avg_passengers, " passengers"),
            ),
            (
                "3. Peak Hour Distribution (Yes/No)",
                (
                    f"{peak_yes_count:,} Peak vs {peak_no_count:,} Off-Peak trips"
                    if peak_yes_count is not None and peak_no_count is not None
                    else "Unavailable"
                ),
            ),
            (
                "4. Average Transit Travel Time",
                show_number(avg_travel_time, " minutes"),
            ),
            (
                "5. Average Route Distance",
                show_number(avg_distance, " meters"),
            ),
            (
                "6. Dominant Traffic Level Condition",
                traffic,
            ),
            (
                "7. Most Common Weather Condition",
                weather,
            ),
            (
                "8. Average Vehicle Capacity Utilization",
                show_number(avg_utilization, "%"),
            ),
            (
                "9. Peak Demand Day of the Week",
                peak_day,
            ),
            (
                "10. Operational Traffic Tier",
                traffic_tier,
            ),
        ]

        report_columns = st.columns(2, gap="small")
        for index, (title, value) in enumerate(report_items):
            with report_columns[index % 2]:
                st.markdown(
                    f'<div class="analysis-card"><b>{title}</b><br>{value}</div>',
                    unsafe_allow_html=True,
                )

        # --------------------------------------------------------
        # NEW: ROUTE-SPECIFIC HISTORICAL ANALYTICS
        # Use only records matching this pickup/drop pair. Even if there
        # are just a few matching records, report those actual records;
        # do not replace them with campus-wide values.
        # --------------------------------------------------------
        route_history = (
            route_data.copy()
            if route_data is not None and not route_data.empty
            else None
        )

        if route_history is None:
            route_history_count_text = "No historical trips found for this route"
            route_history_avg_time = None
            route_history_avg_distance = None
            route_history_traffic = "Unavailable"
            route_peak_count = 0
            route_offpeak_count = 0
            route_peak_trend = "Unavailable — no matching route records"
        else:
            route_history_count_text = f"{len(route_history):,} trips"
            route_history_avg_time = numeric_mean(route_history, "Travel_Time_Min")
            route_history_avg_distance = numeric_mean(route_history, "Distance_m")
            route_history_traffic = mode_value(route_history, "Traffic_Level")

            if "Peak_Hour" in route_history.columns:
                route_peak_values = (
                    route_history["Peak_Hour"]
                    .astype(str).str.strip().str.casefold()
                )
                route_peak_count = int(
                    route_peak_values.isin(["yes", "true", "1"]).sum()
                )
                route_offpeak_count = int(
                    route_peak_values.isin(["no", "false", "0"]).sum()
                )
                if route_peak_count > route_offpeak_count:
                    route_peak_trend = "Peak hours dominate traffic"
                elif route_offpeak_count > route_peak_count:
                    route_peak_trend = "Off-peak hours dominate traffic"
                elif route_peak_count == route_offpeak_count and route_peak_count > 0:
                    route_peak_trend = "No hours dominate traffic"
                else:
                    route_peak_trend = "Unavailable — Peak_Hour values missing"
            else:
                route_peak_count = None
                route_offpeak_count = None
                route_peak_trend = "Unavailable — Peak_Hour column missing"

        historical_route_items = [
            ("Total Historical Records for Route", route_history_count_text),
            ("Average Historical Travel Time", show_number(route_history_avg_time, " mins")),
            (
                "Peak vs Off-Peak Trend",
                (
                    f"{route_peak_count:,} peak vs {route_offpeak_count:,} off-peak trips — "
                    f"{route_peak_trend}"
                    if route_peak_count is not None and route_offpeak_count is not None
                    else route_peak_trend
                ),
            ),
        ]

        historical_route_columns = st.columns(2, gap="small")
        for index, (title, value) in enumerate(historical_route_items):
            with historical_route_columns[index % 2]:
                st.markdown(
                    f'<div class="analysis-card"><b>{title}</b><br>{value}</div>',
                    unsafe_allow_html=True,
                )

        # --------------------------------------------------------
        # RESOURCE ALLOCATION RECOMMENDATION
        # Uses predicted demand together with this route's actual distance,
        # travel time, location types, and historical traffic/peak patterns.
        # Does not assume a fixed passenger capacity per shuttle.
        # --------------------------------------------------------
        recommendation_basis = None
        if route_demand is not None and pd.notna(route_demand):
            recommendation_basis = float(route_demand)
            recommendation_source = "Saved demand model prediction"
        elif route_history is not None:
            route_avg_passengers = numeric_mean(route_history, "Passengers")
            if route_avg_passengers is not None:
                recommendation_basis = route_avg_passengers
                recommendation_source = "Average passengers in matching route records"

        pickup_type = infer_location_type(pickup_id, "pickup", default="Unknown")
        drop_type = infer_location_type(drop_id, "drop", default="Unknown")
        route_distance_m = distance_used if distance_used is not None else None
        route_time_min = travel_time_used if travel_time_used is not None else None

        route_factors = []
        if route_distance_m is not None and pd.notna(route_distance_m):
            route_factors.append(f"route distance {route_distance_m:,.0f} m")
        if route_time_min is not None and pd.notna(route_time_min):
            route_factors.append(f"estimated travel time {route_time_min:.2f} min")
        route_factors.append(f"pickup: {pickup_name} ({pickup_type})")
        route_factors.append(f"drop: {drop_name} ({drop_type})")

        if recommendation_basis is None:
            shuttle_recommendation = (
                "A reliable allocation recommendation is unavailable because neither "
                "the demand model nor matching-route passenger history returned a usable estimate. "
                "Use the route distance, travel time, and live passenger queue to plan dispatch."
            )
        else:
            # Compare demand with route history where available rather than
            # translating passenger count into an assumed vehicle capacity.
            route_avg_passengers = (
                numeric_mean(route_history, "Passengers")
                if route_history is not None else None
            )
            campus_avg_passengers = numeric_mean(master_df, "Passengers")
            comparison_value = route_avg_passengers if route_avg_passengers is not None else campus_avg_passengers
            if comparison_value is not None and comparison_value > 0:
                demand_ratio = recommendation_basis / comparison_value
                if demand_ratio >= 1.25:
                    demand_advice = (
                        "Demand is notably above the available historical baseline. "
                        "Prioritize this route during the predicted period and consider a shorter "
                        "dispatch interval or an additional trip if live queues confirm the increase."
                    )
                elif demand_ratio <= 0.75:
                    demand_advice = (
                        "Demand is below the available historical baseline. Keep the existing "
                        "service pattern initially and consider reducing trip frequency only if "
                        "live passenger counts and waiting times remain low."
                    )
                else:
                    demand_advice = (
                        "Demand is close to the available historical baseline. Maintain the "
                        "current service pattern and adjust dispatch frequency using live queues."
                    )
            elif recommendation_basis >= 20:
                demand_advice = (
                    "The predicted passenger demand is relatively high. Prioritize availability "
                    "during the predicted period and review queues before adding trips."
                )
            elif recommendation_basis <= 10:
                demand_advice = (
                    "The predicted passenger demand is relatively low. Keep current service "
                    "initially and consider a lower frequency only if live counts support it."
                )
            else:
                demand_advice = (
                    "The predicted passenger demand is moderate. Maintain current service and "
                    "adjust frequency according to observed queues and waiting times."
                )

            if route_time_min is not None and pd.notna(route_time_min):
                if route_time_min >= 10:
                    time_advice = (
                        "The trip has a longer estimated travel time, so allow more vehicle "
                        "turnaround time and avoid scheduling back-to-back departures too tightly."
                    )
                else:
                    time_advice = (
                        "The estimated trip time is relatively short; use it to plan turnaround "
                        "and dispatch intervals, while allowing for campus traffic variation."
                    )
            else:
                time_advice = "Use the route's observed travel time to set realistic dispatch intervals."

            if route_distance_m is not None and pd.notna(route_distance_m):
                if route_distance_m >= 1500:
                    distance_advice = (
                        "The route is relatively long; account for travel distance when assigning "
                        "vehicles and planning the return leg."
                    )
                else:
                    distance_advice = (
                        "The route is relatively short; balance this route with nearby routes "
                        "only when their demand and schedules allow."
                    )
            else:
                distance_advice = "Confirm route distance before finalizing vehicle assignment."

            shuttle_recommendation = (
                f"Estimated demand: {recommendation_basis:.1f} passengers. "
                f"{demand_advice} {time_advice} {distance_advice}"
            )

        st.markdown(
            f'<div class="analysis-card"><b>Recommendation</b><br>'
            f'{shuttle_recommendation}<br>'
            f'<span style="color:#777;font-size:11px;">'
            f'Inputs considered: {"; ".join(route_factors)}. '
            f'Basis: {recommendation_source if recommendation_basis is not None else "No usable demand data"}. '
            f'Operational guidance — verify with live passenger counts, queues, and traffic.</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ========================================================
    # 11. ROUTE MAP
    # MAP DISPLAY CODE IS KEPT UNCHANGED.
    # ========================================================
    with map_col:

        if route_map_html:
            st.iframe(
                route_map_html,
                height=520,
            )

            st.download_button(
                " Download Route Map (HTML)",
                data=route_map_html,
                file_name="lpu_route_map.html",
                mime="text/html",
                use_container_width=True,
            )

            if shortest is not None:
                st.markdown(
                    '<div class="analysis-card">'
                    '<b>Shortest route</b><br>'
                    f'{shortest["distance"] / 1000:.3f} km · '
                    f'{shortest["duration"] / 60:.2f} minutes'
                    '</div>',
                    unsafe_allow_html=True,
                )

            if fastest is not None:
                st.markdown(
                    '<div class="analysis-card">'
                    '<b>Fastest route</b><br>'
                    f'{fastest["distance"] / 1000:.3f} km · '
                    f'{fastest["duration"] / 60:.2f} minutes'
                    '</div>',
                    unsafe_allow_html=True,
                )

        else:
            st.warning(
                "Route map could not be generated: "
                f"{route_map_error or 'Unknown route-map error'}"
            )

            st.caption(
                "Check LPU_All_Locations.xlsx, "
                "Route_Recommendation/routefinder.py, "
                "location IDs, and internet access."
            )

st.markdown(
    "<div style='height:35px;'></div>",
    unsafe_allow_html=True,
)



# ============================================================

# ============================================================
# LIVE DESTINATION TRACKING — isolated from existing analytics
# ============================================================
st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
st.markdown(
    '<div class="services-header">'
    '<h1 class="services-title">Live Destination Tracking</h1>'
    '</div>',
    unsafe_allow_html=True,
)
st.caption(
    "Choose any LPU campus location to follow the latest verified phone GPS device. "
    "The route and ETA are calculated from its current GPS position."
)

live_locations = []
try:
    _live_routefinder = load_routefinder()
    if _live_routefinder is not None:
        _live_frame = _live_routefinder.load_locations()
        for _, _row in _live_frame.iterrows():
            _lat = pd.to_numeric(_row.get("Latitude"), errors="coerce")
            _lon = pd.to_numeric(_row.get("Longitude"), errors="coerce")
            if pd.notna(_lat) and pd.notna(_lon):
                _live_locations.append({
                    "label": f"{str(_row['ID']).strip()} — {str(_row['Location Name']).strip()}",
                    "name": str(_row["Location Name"]).strip(),
                    "lat": float(_lat),
                    "lon": float(_lon),
                })
except Exception:
    live_locations = []

# Use the same workbook-backed campus locations as the existing route finder.
_live_unique = {}
for _loc in live_locations:
    _live_unique[(_loc["label"], _loc["lat"], _loc["lon"])] = _loc
live_locations = sorted(_live_unique.values(), key=lambda item: item["label"].casefold())

if live_locations:
    _live_locations_json = json.dumps(live_locations, ensure_ascii=False).replace("</", "<\\/")
    _live_tracker_html = r"""
<!doctype html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;color:#f8fafc;background:#101010}
.panel{background:#171717;border:1px solid #343434;border-left:3px solid #ff6a00;border-radius:12px;padding:16px;margin-bottom:12px}
.controls{display:grid;grid-template-columns:1.3fr 1fr auto;gap:10px;align-items:end}
label{display:block;color:#ff9a52;font-size:12px;font-weight:bold;margin-bottom:6px}
input,select,button{width:100%;padding:12px;border-radius:8px;border:1px solid #555;background:#101010;color:white;font-size:14px}
button{background:#ff6a00;color:#111;border:0;font-weight:bold;cursor:pointer}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}
.metric{background:#101010;padding:13px;border-radius:9px;color:#bbb;font-size:12px}
.metric strong{display:block;color:#ff8a35;font-size:21px;margin-top:6px}
#map{height:430px;border-radius:10px;overflow:hidden}
#status{font-size:13px;color:#ddd;margin-top:10px;line-height:1.5}
.small{color:#aaa;font-size:12px;line-height:1.5}
@media(max-width:700px){.controls{grid-template-columns:1fr}.metrics{grid-template-columns:1fr 1fr}#map{height:360px}}
</style></head><body>
<div class="panel">
 <div class="controls">
  <div><label for="destination">LPU DESTINATION</label><select id="destination"></select></div>
  <div><label for="key">DASHBOARD ACCESS KEY</label><input id="key" type="password" placeholder="Enter dashboard key"></div>
  <div><button id="connect">CONNECT & TRACK</button></div>
 </div>
 <div id="status">Select a destination, enter your dashboard access key, and click CONNECT &amp; TRACK.</div>
 <div class="metrics">
  <div class="metric">ESTIMATED ARRIVAL<strong id="eta">--</strong></div>
  <div class="metric">ROAD DISTANCE LEFT<strong id="distance">--</strong></div>
  <div class="metric">DEVICE SPEED<strong id="speed">--</strong></div>
 </div>
 <p class="small" id="updated">Waiting for secure connection.</p>
</div>
<div class="panel"><div id="map"></div></div>
<p class="small">ETA uses the road route from OpenStreetMap routing and the latest GPS position. Actual arrival can vary with campus access, traffic, and GPS accuracy. Only the latest device currently reported by the secure GPS service is followed.</p>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const locations=__LOCATIONS__;
const API="https://shuttlelyze-gps-cloud.onrender.com";
const select=document.getElementById("destination");
locations.forEach((p,i)=>{const o=document.createElement("option");o.value=i;o.textContent=p.label;select.appendChild(o);});
let map=L.map("map").setView([31.255,75.705],15),deviceMarker=null,destMarker=null,routeLine=null,timer=null,lastRouteAt=0,lastDevice=null;
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:19,attribution:"© OpenStreetMap"}).addTo(map);
function status(t){document.getElementById("status").textContent=t;}
function destination(){return locations[Number(select.value)];}
function setMetric(id,value){document.getElementById(id).textContent=value;}
async function refresh(forceRoute=false){
 const key=document.getElementById("key").value.trim();
 if(!key)throw new Error("Enter the dashboard access key.");
 const r=await fetch(API+"/api/latest",{headers:{"X-Dashboard-Key":key},cache:"no-store"});
 const data=await r.json();if(!r.ok)throw new Error(data.error||("GPS service HTTP "+r.status));
 if(!data.latest){status("Connected, but no active GPS location is available. Start GPS tracking on the phone.");return;}
 const p=data.latest,from=[p.latitude,p.longitude],to=destination();
 const age=(Date.now()-new Date(p.recorded_at).getTime())/1000;
 if(!deviceMarker){deviceMarker=L.marker(from).addTo(map).bindPopup("Latest verified phone");}
 else deviceMarker.setLatLng(from);
 if(!destMarker){destMarker=L.marker([to.lat,to.lon]).addTo(map).bindPopup(to.name);}
 else destMarker.setLatLng([to.lat,to.lon]);
 setMetric("speed",p.speed==null?"--":(p.speed*3.6).toFixed(1)+" km/h");
 document.getElementById("updated").textContent="Device: "+(p.email||"verified user")+" · GPS update: "+new Date(p.recorded_at).toLocaleString()+" · "+(age>60?"GPS data is "+Math.round(age/60)+" min old":"GPS data is recent");
 const movedMeters=lastDevice?(()=>{const rad=x=>x*Math.PI/180;const dLat=rad(p.latitude-lastDevice.lat),dLon=rad(p.longitude-lastDevice.lon);const a=Math.sin(dLat/2)**2+Math.cos(rad(lastDevice.lat))*Math.cos(rad(p.latitude))*Math.sin(dLon/2)**2;return 6371000*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));})():Infinity;
 if(forceRoute||movedMeters>=20||Date.now()-lastRouteAt>20000){
  lastRouteAt=Date.now();lastDevice={lat:p.latitude,lon:p.longitude};
  const url="https://router.project-osrm.org/route/v1/driving/"+p.longitude+","+p.latitude+";"+to.lon+","+to.lat+"?overview=full&geometries=geojson";
  const rr=await fetch(url);const rd=await rr.json();
  if(rd.code!=="Ok"||!rd.routes||!rd.routes.length)throw new Error("A road route could not be found for this device and destination.");
  const route=rd.routes[0],coords=route.geometry.coordinates.map(c=>[c[1],c[0]]);
  if(routeLine)map.removeLayer(routeLine);
  routeLine=L.polyline(coords,{color:"#ff6a00",weight:6,opacity:.9}).addTo(map);
  setMetric("eta",Math.max(1,Math.round(route.duration/60))+" min");
  setMetric("distance",(route.distance>=1000?(route.distance/1000).toFixed(2)+" km":Math.round(route.distance)+" m"));
  map.fitBounds(routeLine.getBounds(),{padding:[35,35]});
  if(route.distance<=40){status("The tracked device has reached the selected destination (within approximately 40 metres).");}
  else{status("Live tracking active: "+(p.email||"verified device")+" is heading toward "+to.name+". Route ETA is updating.");}
 }
}
document.getElementById("connect").addEventListener("click",async()=>{
 if(timer)clearInterval(timer);
 status("Connecting securely and loading the live route...");
 try{await refresh(true);timer=setInterval(()=>refresh(false).catch(e=>status("Tracking error: "+e.message)),5000);}
 catch(e){status("Connection failed: "+e.message);}
});
select.addEventListener("change",()=>{if(timer)refresh(true).catch(e=>status("Route error: "+e.message));});
</script></body></html>
"""
    _live_tracker_html = _live_tracker_html.replace("__LOCATIONS__", _live_locations_json)
    components.html(_live_tracker_html, height=760, scrolling=True)
else:
    st.warning(
        "Live destination tracking needs the LPU location workbook with valid Latitude and Longitude columns. "
        "The existing route analytics above are not affected."
    )


# 12. WHAT-IF DEMAND SIMULATION
# One location + traffic + weather + peak-hour conditions.
# Uses the saved model directly; no baseline or manual demand adjustment.
# ============================================================
st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
st.markdown(
    '<div class="services-header">'
    '<h1 class="services-title">What-If Demand Simulation</h1>'
    '</div>',
    unsafe_allow_html=True,
)
st.caption(
    "Choose a campus location and operating conditions to estimate passenger demand. "
    "The saved model is used directly; no baseline comparison or assumed shuttle capacity is shown."
)

whatif_col1, whatif_col2, whatif_col3, whatif_col4 = st.columns(4, gap="medium")
with whatif_col1:
    whatif_location = st.selectbox(
        "Campus location",
        location_options,
        index=location_options.index(pickup_location) if pickup_location in location_options else 0,
        key="whatif_location_single",
    )
with whatif_col2:
    whatif_traffic = st.selectbox(
        "Traffic condition",
        ["Low", "Medium", "High"],
        index=1,
        key="whatif_traffic_single",
    )
with whatif_col3:
    whatif_weather = st.selectbox(
        "Weather condition",
        ["Normal", "Rainy", "Foggy", "Hot", "Stormy"],
        index=0,
        key="whatif_weather_single",
    )
with whatif_col4:
    whatif_peak = st.selectbox(
        "Peak hour",
        ["No", "Yes"],
        index=1,
        key="whatif_peak_single",
    )

whatif_location_id, whatif_location_name = split_location(whatif_location)
whatif_drop_id, whatif_drop_name = split_location(drop_location)

# The saved demand pipeline was trained on route-level features, including
# pickup and drop locations, distance and travel time. Therefore, the selected
# location is used as the pickup, and the current page's drop selection remains
# the route destination. This preserves the trained model's expected schema.
whatif_origin_type = infer_location_type(
    whatif_location_id, "pickup", default="Academic"
)
whatif_destination_type = infer_location_type(
    whatif_drop_id, "drop", default="Academic"
)
whatif_origin = {
    "ID": whatif_location_id,
    "Name": whatif_location_name,
    "Type": whatif_origin_type,
}
whatif_destination = {
    "ID": whatif_drop_id,
    "Name": whatif_drop_name,
    "Type": whatif_destination_type,
}

whatif_distance, whatif_time, whatif_matrix_error = get_matrix_travel_result(
    whatif_location_id,
    whatif_location_name,
    whatif_drop_id,
    whatif_drop_name,
    travel_matrices,
)

# Use matching historical route values only if the saved matrix has no match.
whatif_matching_history = None
if master_df is not None and {"Pickup_Block", "Drop_Block"}.issubset(master_df.columns):
    whatif_matching_history = master_df[
        (master_df["Pickup_Block"].astype(str).str.strip() == str(whatif_location_id).strip())
        & (master_df["Drop_Block"].astype(str).str.strip() == str(whatif_drop_id).strip())
    ]

if whatif_distance is None and whatif_matching_history is not None and not whatif_matching_history.empty:
    whatif_distance = numeric_mean(whatif_matching_history, "Distance_m")
if whatif_time is None and whatif_matching_history is not None and not whatif_matching_history.empty:
    whatif_time = numeric_mean(whatif_matching_history, "Travel_Time_Min")

if whatif_distance is None or whatif_time is None:
    st.warning(
        "A saved distance and travel-time estimate could not be found for this route. "
        "Choose another campus location or update the saved route matrix; a demand prediction "
        "is not generated using invented route values."
    )
else:
    whatif_vehicle_capacity = numeric_mean(master_df, "Vehicle_Capacity")
    whatif_demand, whatif_demand_source = predict_route_demand(
        whatif_origin,
        whatif_destination,
        distance_m=float(whatif_distance),
        travel_time_min=float(whatif_time),
        traffic_level=whatif_traffic,
        weather=whatif_weather,
        peak_hour=whatif_peak,
        vehicle_capacity=whatif_vehicle_capacity,
    )

    if whatif_demand is None:
        st.error(
            "The saved demand model could not produce a prediction for these inputs. "
            "Check that demand_prediction_pipeline.pkl is available and that its expected "
            "features match the input pipeline."
        )
        st.caption(f"Model status: {whatif_demand_source}")
    else:
        # Rule-based demand level from weather and operating conditions:
        # Rainy or Stormy weather always means High demand, regardless of other inputs.
        # Otherwise: High = peak hour AND high traffic; Medium = either one; Low = neither.
        is_extreme_weather = str(whatif_weather).strip().lower() in {"rainy", "stormy"}
        is_peak_hour = str(whatif_peak).strip().lower() == "yes"
        is_high_traffic = str(whatif_traffic).strip().lower() == "high"

        if is_extreme_weather:
            whatif_level = "High"
            whatif_advice = (
                "Rainy or stormy weather is selected, so demand is classified as High regardless "
                "of traffic or peak-hour settings. Prepare for disruption and review shuttle capacity."
            )
        elif is_peak_hour and is_high_traffic:
            whatif_level = "High"
            whatif_advice = (
                "Peak hour and high traffic are both present. Expect the highest demand pressure; "
                "monitor queues and consider allocating additional shuttle capacity."
            )
        elif is_peak_hour or is_high_traffic:
            whatif_level = "Medium"
            whatif_advice = (
                "Either peak hour or high traffic is present. Monitor passenger queues and "
                "adjust shuttle allocation if demand increases."
            )
        else:
            whatif_level = "Low"
            whatif_advice = (
                "Extreme weather, peak hour, and high traffic are not selected. Expected demand "
                "pressure is low; continue monitoring actual passenger counts."
            )

        result_cols = st.columns(2, gap="medium")
        with result_cols[0]:
            st.metric("Estimated demand level", whatif_level)
        with result_cols[1]:
            st.metric("Estimated travel time", f"{float(whatif_time):.2f} min")

        st.markdown(
            '<div class="analysis-card"><b>Scenario result</b><br>'
            f'<b>Location:</b> {whatif_location_name}<br>'
            f'<b>Route used by model:</b> {whatif_location_name} → {whatif_drop_name}<br>'
            f'<b>Distance:</b> {float(whatif_distance):,.2f} m<br>'
            f'<b>Conditions:</b> Traffic {whatif_traffic} · Weather {whatif_weather} · '
            f'Peak hour {whatif_peak}<br>'
            f'<b>Planning insight:</b> {whatif_advice}'
            '</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "This is a model estimate, not a live passenger count. The saved model uses route-level "
            "features, so the selected location is evaluated as the pickup and the page's current "
            "drop location is retained as the destination. Demand level is classified from the "
            "selected weather, peak-hour, and traffic conditions."
        )

st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)




render_cinematic_footer()
