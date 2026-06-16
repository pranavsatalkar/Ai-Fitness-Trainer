import streamlit as st
import json
import os
from datetime import datetime


def save_weight():
    with open("weight_log.json", "w") as f:
        json.dump(st.session_state.weight_log, f)


def settings_page():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    [data-testid="stAppViewContainer"] > [data-testid="stMain"] { background: #f2f2f7 !important; }
    [data-testid="block-container"] { padding-top: 1.2rem !important; max-width: 640px !important; margin: 0 auto !important; }

    .s-header {
        text-align: center;
        padding: 10px 0 24px 0;
    }
    .s-header-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #1c1c1e;
    }

    /* Profile card on top */
    .s-profile-card {
        background: white;
        border-radius: 16px;
        padding: 18px 20px;
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .s-avatar {
        width: 58px;
        height: 58px;
        border-radius: 50%;
        background: linear-gradient(135deg, #0d1b3e, #1a3a6b);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        flex-shrink: 0;
    }
    .s-profile-name {
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #1c1c1e;
        line-height: 1.2;
    }
    .s-profile-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        color: #8e8e93;
        margin-top: 2px;
    }
    .s-profile-arrow {
        margin-left: auto;
        color: #c7c7cc;
        font-size: 1.2rem;
    }

    /* Section label */
    .s-section-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        color: #8e8e93;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        padding: 0 4px;
        margin: 18px 0 6px 0;
    }

    /* Row group */
    .s-group {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        margin-bottom: 10px;
    }
    .s-row {
        display: flex;
        align-items: center;
        padding: 14px 18px;
        gap: 14px;
        border-bottom: 1px solid #f2f2f7;
    }
    .s-row:last-child { border-bottom: none; }
    .s-row-icon {
        width: 34px;
        height: 34px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        flex-shrink: 0;
    }
    .s-row-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.92rem;
        font-weight: 500;
        color: #1c1c1e;
        flex: 1;
    }
    .s-row-value {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: #8e8e93;
        margin-right: 4px;
    }
    .s-row-arrow {
        color: #c7c7cc;
        font-size: 1rem;
    }
    [data-testid="stVerticalBlock"]:has(.s-edit-title) {
        background: white;
        border-radius: 16px;
        padding: 22px 20px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .s-edit-title {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #1c1c1e;
        margin-bottom: 16px;
    }
    .s-field-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        color: #8e8e93;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 5px;
        margin-top: 12px;
    }

    /* Input overrides */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        background: #f2f2f7 !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stTextInput"] input {
        font-family: 'Inter', sans-serif !important;
        color: #1c1c1e !important;
        font-size: 0.9rem !important;
        background: #f2f2f7 !important;
    }
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background: #f2f2f7 !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stSelectbox"] > div > div {
        background: #f2f2f7 !important;
        border-radius: 10px !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        box-shadow: none !important;
    }

    /* Buttons */
    button[kind="primary"] {
        background: #0d1b3e !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    button[kind="secondary"] {
        background: white !important;
        border: 1.5px solid #e5e5ea !important;
        color: #1c1c1e !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
    }

    /* Toast */
    .s-toast {
        padding: 13px 18px;
        border-radius: 12px;
        margin-top: 10px;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .s-toast.success { background: #e8f5e9; color: #1b5e20; border: 1px solid #a5d6a7; }
    .s-toast.warning { background: #fff8e1; color: #f57f17; border: 1px solid #ffe082; }
    </style>
    """, unsafe_allow_html=True)

    profile = st.session_state.user_profile or {}
    name    = profile.get("name",   "Athlete")
    weight  = profile.get("weight", 0)
    level   = profile.get("level",  "Beginner")
    goal    = profile.get("goal",   "Stay Fit")
    initials = "".join([w[0].upper() for w in name.split()[:2]])

    if "s_panel" not in st.session_state:
        st.session_state.s_panel = None

    panel = st.session_state.s_panel

    # ══════════════════════════════════════════════════════════════════════════
    # MAIN LIST VIEW
    # ══════════════════════════════════════════════════════════════════════════
    if panel is None:

        st.markdown('<div class="s-header"><div class="s-header-title">Settings</div></div>', unsafe_allow_html=True)

        # Profile card
        st.markdown(f"""
        <div class="s-profile-card">
            <div class="s-avatar">{initials}</div>
            <div>
                <div class="s-profile-name">{name}</div>
                <div class="s-profile-sub">{level} &nbsp;·&nbsp; {goal}</div>
            </div>
            <div class="s-profile-arrow">›</div>
        </div>
        """, unsafe_allow_html=True)

        # Account rows
        st.markdown('<div class="s-section-label">Account</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="s-group">
            <div class="s-row">
                <div class="s-row-icon" style="background:#e8f4ff;">👨🏻‍💼</div>
                <div class="s-row-label">Name</div>
                <div class="s-row-value">{name}</div>
                <div class="s-row-arrow">›</div>
            </div>
            <div class="s-row">
                <div class="s-row-icon" style="background:#e8fff4;">⚖️</div>
                <div class="s-row-label">Weight</div>
                <div class="s-row-value">{weight} kg</div>
                <div class="s-row-arrow">›</div>
            </div>
            <div class="s-row">
                <div class="s-row-icon" style="background:#f5f0ff;">🎯</div>
                <div class="s-row-label">Fitness Goal</div>
                <div class="s-row-value">{goal}</div>
                <div class="s-row-arrow">›</div>
            </div>
            <div class="s-row">
                <div class="s-row-icon" style="background:#fff8e1;">📋</div>
                <div class="s-row-label">Activity Level</div>
                <div class="s-row-value">{level}</div>
                <div class="s-row-arrow">›</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Edit / Reset buttons
        c1, c2 = st.columns(2, gap="small")
        with c1:
            if st.button("✎ Edit Profile", use_container_width=True, type="primary"):
                st.session_state.s_panel = "edit"
                st.rerun()
        with c2:
            if st.button(" 🗑 Reset Details", use_container_width=True, type="secondary"):
                st.session_state.s_panel = "reset"
                st.rerun()

        # App info rows
        st.markdown('<div class="s-section-label">App Info</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="s-group">
            <div class="s-row">
                <div class="s-row-icon" style="background:#f0f4ff;">ℹ️</div>
                <div class="s-row-label">Version</div>
                <div class="s-row-value">1.0.0</div>
            </div>
            <div class="s-row">
                <div class="s-row-icon" style="background:#f0f4ff;">🤖</div>
                <div class="s-row-label">AI Model</div>
                <div class="s-row-value">Llama 3.1</div>
            </div>
            <div class="s-row">
                <div class="s-row-icon" style="background:#f0f4ff;">📍</div>
                <div class="s-row-label">Pose Engine</div>
                <div class="s-row-value">MediaPipe</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # EDIT PROFILE PANEL
    # ══════════════════════════════════════════════════════════════════════════
    elif panel == "edit":

        if st.button("← Back", type="secondary"):
            st.session_state.s_panel = None
            st.rerun()

        st.markdown('<div class="s-edit-panel">', unsafe_allow_html=True)
        st.markdown('<div class="s-edit-title">Edit Profile</div>', unsafe_allow_html=True)

        st.markdown('<div class="s-field-label">Full Name</div>', unsafe_allow_html=True)
        edit_name = st.text_input("Name", value=name, label_visibility="collapsed", key="set_name")

        st.markdown('<div class="s-field-label">Weight (kg)</div>', unsafe_allow_html=True)
        edit_weight = st.text_input(
            "Weight",
            value=str(weight),
            label_visibility="collapsed",
            key="set_weight"
        )
        try:
            edit_weight = float(edit_weight)
        except:
            st.session_state._settings_msg = ("warning", "⚠️ Enter valid weight!")
            st.rerun()

        st.markdown('<div class="s-field-label">Activity Level</div>', unsafe_allow_html=True)
        level_options = ["Beginner", "Intermediate", "Advanced"]
        edit_level = st.selectbox("Level", level_options,
                                  index=level_options.index(level),
                                  label_visibility="collapsed", key="set_level")

        st.markdown('<div class="s-field-label">Fitness Goal</div>', unsafe_allow_html=True)
        goal_options = ["Weight Loss", "Muscle Gain", "Stay Fit", "Endurance"]
        edit_goal = st.selectbox("Goal", goal_options,
                                 index=goal_options.index(goal),
                                 label_visibility="collapsed", key="set_goal")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Save Changes", use_container_width=True, type="primary", key="save_profile"):
            if not edit_name.strip():
                st.session_state._settings_msg = ("warning", "⚠️ Name cannot be empty!")
                st.rerun()
            else:
                updated = {
                    "name":   edit_name.strip(),
                    "weight": round(edit_weight, 1),
                    "level":  edit_level,
                    "goal":   edit_goal,
                }
                st.session_state.user_profile = updated
                with open("user_profile.json", "w") as f:
                    json.dump(updated, f)

                _today = datetime.today().strftime("%Y-%m-%d")
                if "weight_log" not in st.session_state:
                    st.session_state.weight_log = {}
                st.session_state.weight_log[_today] = round(edit_weight, 1)
                save_weight()

                st.session_state._settings_msg = ("success", f"✅ Saved! Hello, {edit_name.strip()}!")
                st.session_state.s_panel = None
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # RESET PANEL
    # ══════════════════════════════════════════════════════════════════════════
    elif panel == "reset":

        if st.button("← Back", type="secondary"):
            st.session_state.s_panel = None
            st.rerun()

        st.markdown("""
        <div class="s-edit-panel">
            <div class="s-edit-title" style="color:#ff3b30;">🗑 Reset All Data</div>
            <div style="font-family:'Inter',sans-serif;font-size:0.85rem;color:#6b7280;line-height:1.8;">
                This will permanently delete:<br>
                &nbsp;· Your profile &amp; name<br>
                &nbsp;· All session history<br>
                &nbsp;· Food &amp; nutrition logs<br>
                &nbsp;· Weight log &amp; streak<br>
                &nbsp;· All progress data<br><br>
                <strong style="color:#1c1c1e;">You will be taken back to onboarding.<br>This cannot be undone.</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        confirm = st.checkbox("I understand — delete everything permanently.", key="reset_confirm")

        if st.button("Reset Everything", use_container_width=True,
                     type="secondary", key="reset_all", disabled=not confirm):

            for fname in [
                "user_profile.json", "session_log.json", "food_log.json",
                "streak.json", "user_goals.json", "goals_vals.json",
                "weight_log.json", "custom_targets.json", "rest_days.json"
            ]:
                if os.path.exists(fname):
                    os.remove(fname)

            for key in list(st.session_state.keys()):
                del st.session_state[key]

            st.rerun()

    # ── Toast ─────────────────────────────────────────────────────────────────
    if "_settings_msg" in st.session_state:
        kind, msg = st.session_state._settings_msg
        st.markdown(f'<div class="s-toast {kind}">{msg}</div>', unsafe_allow_html=True)
        del st.session_state._settings_msg

