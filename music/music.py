import streamlit as st
import streamlit.components.v1 as components
import os
import base64

MUSIC_DIR = "music/songs"
os.makedirs(MUSIC_DIR, exist_ok=True)


def get_songs():
    if not os.path.isdir(MUSIC_DIR):
        return []
    files = [f for f in os.listdir(MUSIC_DIR)
             if f.lower().endswith((".mp3", ".wav", ".ogg"))]
    files.sort()
    return [(f, os.path.join(MUSIC_DIR, f)) for f in files]


def clean_name(filename):
    return os.path.splitext(filename)[0]


def file_ext(filename):
    return os.path.splitext(filename)[1].lstrip(".").upper()


def music_page():

    if "music_current" not in st.session_state:
        st.session_state.music_current = None

    songs = get_songs()
    if st.session_state.music_current is None and songs:
        st.session_state.music_current = songs[0][0]
    current = st.session_state.music_current

    # ── Global CSS ──────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Inter:wght@400;500;600;700&display=swap');

    [data-testid="stAppViewContainer"] > [data-testid="stMain"] {
        background: #f0f4ff !important;
    }
    [data-testid="block-container"] {
        padding-top: 1.4rem !important;
        padding-bottom: 2rem !important;
    }
    [data-testid="stFileUploader"] {
        background: white !important;
        border-radius: 14px !important;
        border: 1.5px dashed #c7d2fe !important;
        padding: 6px !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: white !important;
        border: none !important;
        border-radius: 10px !important;
    }
    button[kind="primary"] {
        background: #0d1b3e !important;
        color: white !important;
        border: none !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.15s ease !important;
        margin-top: 5px !important;
    }
    button[kind="secondary"] { 
        background: #ffff !important; 
        color: black !important; 
        border: none !important; 
        border-radius: none !important;
        margin-top:21px !important;
    }
    .song-row {
        background: white;
        border: 1.5px solid #e4eaf5;
        border-radius: 14px;
        padding: 14px 16px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 14px;
        transition: all 0.15s ease;
    }
    .song-row:hover { border-color: #b0bcef; }
    .song-row.active { background: #eef2ff; border-color: #4f6ef7; }
    .song-icon {
        width: 46px; height: 46px; border-radius: 12px;
        display: flex; align-items: center;
        justify-content: center; font-size: 20px; flex-shrink: 0;
    }
    .song-icon.active   { background: #0d1b3e; }
    .song-icon.inactive { background: #f0f4ff; }
    .song-title {
        font-family: 'Inter', sans-serif; font-size: 0.88rem;
        font-weight: 700; color: #0d1b3e;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .song-meta { font-family: 'Inter', sans-serif; font-size: 0.68rem; color: #94a3b8; margin-top: 2px; }
    .now-playing-pill {
        display: inline-flex; align-items: center; gap: 5px;
        background: rgba(79,110,247,0.12); color: #4f6ef7;
        border-radius: 999px; padding: 3px 10px;
        font-size: 0.65rem; font-weight: 700;
        font-family: 'Inter', sans-serif; margin-top: 4px;
    }
    .pulse-dot {
        width: 6px; height: 6px; background: #4f6ef7;
        border-radius: 50%; animation: pulse 1.2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%       { opacity: 0.5; transform: scale(0.7); }
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Page Header ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(120deg,#0d1b3e 55%,#1a3a6b 100%);
                border-radius:20px;padding:36px 40px;margin:-40px 0 24px 0;text-align:center;">
        <div style="display:inline-flex;align-items:center;gap:8px;
                    background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
                    color:rgba(255,255,255,0.7);border-radius:999px;padding:5px 16px;
                    font-size:0.68rem;font-weight:700;letter-spacing:1.5px;
                    text-transform:uppercase;margin-bottom:14px;font-family:Inter,sans-serif;">
            🎵 WORKOUT MUSIC
        </div>
        <div style="font-family:'Barlow Condensed',sans-serif;font-weight:800;
                    font-size:2.4rem;color:white;line-height:1;margin-bottom:8px;">
            Your Music Library
        </div>
        <div style="font-family:Inter,sans-serif;color:rgba(255,255,255,0.5);font-size:0.85rem;">
            Upload and play your favorite workout tracks while training.
        </div>
        <div style="display:flex;gap:8px;justify-content:center;margin-top:16px;">
            <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
                        color:rgba(255,255,255,0.6);border-radius:999px;padding:4px 14px;
                        font-size:0.7rem;font-weight:700;font-family:Inter,sans-serif;">MP3</div>
            <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
                        color:rgba(255,255,255,0.6);border-radius:999px;padding:4px 14px;
                        font-size:0.7rem;font-weight:700;font-family:Inter,sans-serif;">WAV</div>
            <div style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.12);
                        color:rgba(255,255,255,0.6);border-radius:999px;padding:4px 14px;
                        font-size:0.7rem;font-weight:700;font-family:Inter,sans-serif;">OGG</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([1.15, 1], gap="medium")

    with col_left:

            if current:
                np_name = clean_name(current)
                np_ext  = file_ext(current)

                fpath = os.path.join(MUSIC_DIR, current)
                audio_b64 = ""
                if os.path.exists(fpath):
                    with open(fpath, "rb") as af:
                        audio_b64 = base64.b64encode(af.read()).decode()

                audio_src = "data:audio/" + np_ext.lower() + ";base64," + audio_b64

                player_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background: transparent; font-family: Inter, sans-serif; }

    .card {
        background: linear-gradient(135deg, #0d1b3e 0%, #1a3a6b 100%);
        border-radius: 18px;
        padding: 22px 24px;
    }
    .top-row {
        display: flex; align-items: center; gap: 14px; margin-bottom: 20px;
    }
    .music-icon {
        width: 56px; height: 56px; border-radius: 14px;
        background: rgba(255,255,255,0.12);
        display: flex; align-items: center; justify-content: center;
        font-size: 26px; flex-shrink: 0;
    }
    .song-label {
        font-size: 0.65rem; font-weight: 700; letter-spacing: 1px;
        text-transform: uppercase; color: rgba(255,255,255,0.4);
        margin-bottom: 4px;
    }
    .song-name {
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.3rem; font-weight: 800; color: white;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        max-width: 300px;
    }
    .song-fmt { font-size: 0.72rem; color: rgba(255,255,255,0.4); margin-top: 2px; }
    .live-badge {
        margin-left: auto; flex-shrink: 0;
        display: flex; align-items: center; gap: 5px;
        background: rgba(0,230,118,0.12); border: 1px solid rgba(0,230,118,0.3);
        border-radius: 999px; padding: 4px 10px;
    }
    .live-dot {
        width: 7px; height: 7px; background: #00e676;
        border-radius: 50%; animation: blink 1.4s infinite;
    }
    .live-text { font-size: 0.62rem; font-weight: 700; color: #00e676; letter-spacing: 0.5px; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

    .controls {
        background: rgba(255,255,255,0.07);
        border-radius: 14px; padding: 16px 18px;
    }
    .seek-row {
        display: flex; align-items: center; gap: 12px; margin-bottom: 12px;
    }
    .play-btn {
        width: 44px; height: 44px; border-radius: 50%;
        background: white; border: none; cursor: pointer;
        font-size: 16px; color: #0d1b3e;
        flex-shrink: 0; transition: transform 0.1s, box-shadow 0.1s;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .play-btn:hover { transform: scale(1.08); box-shadow: 0 6px 16px rgba(0,0,0,0.4); }

    input[type=range] {
        -webkit-appearance: none;
        height: 4px; border-radius: 99px; cursor: pointer; outline: none;
    }
    #seek-bar { flex: 1; background: rgba(255,255,255,0.2); }
    #vol-bar  { width: 80px; background: rgba(255,255,255,0.2); }
    input[type=range]::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 14px; height: 14px;
        border-radius: 50%; background: white; cursor: pointer;
    }

    .time {
        font-size: 0.72rem; color: rgba(255,255,255,0.6);
        font-weight: 600; white-space: nowrap; min-width: 86px; text-align: right;
    }
    .vol-row { display: flex; align-items: center; gap: 10px; }
    .vol-icon { font-size: 14px; color: rgba(255,255,255,0.5); }
    .vol-label { font-size: 0.68rem; color: rgba(255,255,255,0.35); }
    </style>
    </head>
    <body>
    <div class="card">
    <div class="top-row">
        <div class="music-icon">🎵</div>
        <div style="flex:1;min-width:0;">
        <div class="song-label">Now Playing</div>
        <div class="song-name">SONG_NAME</div>
        <div class="song-fmt">SONG_EXT Format</div>
        </div>
        <div class="live-badge">
        <div class="live-dot"></div>
        <span class="live-text">LIVE</span>
        </div>
    </div>
    <audio id="audio" src="AUDIO_SRC" preload="auto"></audio>
    <div class="controls">
        <div class="seek-row">
        <button class="play-btn" id="play-btn" onclick="togglePlay()">&#9654;</button>
        <input type="range" id="seek-bar" value="0" min="0" max="100" step="0.1"
                oninput="seekAudio(this.value)">
        <div class="time" id="time-display">0:00 / 0:00</div>
        </div>
        <div class="vol-row">
        <span class="vol-icon">&#128264;</span>
        <input type="range" id="vol-bar" value="100" min="0" max="100"
                oninput="setVol(this.value)">
        <span class="vol-label">Volume</span>
        </div>
    </div>
    </div>
    <script>
    var audio = document.getElementById('audio');
    var playBtn = document.getElementById('play-btn');
    var seekBar = document.getElementById('seek-bar');
    var timeDisp = document.getElementById('time-display');

    function fmt(s) {
        var m = Math.floor(s/60), sec = Math.floor(s%60);
        return m + ':' + (sec<10?'0':'') + sec;
    }
    function togglePlay() {
        if (audio.paused) { audio.play(); playBtn.innerHTML='&#9646;&#9646;'; }
        else { audio.pause(); playBtn.innerHTML='&#9654;'; }
    }
    function seekAudio(v) { if(audio.duration) audio.currentTime = audio.duration*v/100; }
    function setVol(v) { audio.volume = v/100; }
    audio.addEventListener('timeupdate', function() {
        if(audio.duration) {
        seekBar.value = (audio.currentTime/audio.duration)*100;
        timeDisp.textContent = fmt(audio.currentTime)+' / '+fmt(audio.duration);
        }
    });
    audio.addEventListener('ended', function() {
        playBtn.innerHTML='&#9654;'; seekBar.value=0;
    });
    </script>
    </body>
    </html>"""
                player_html = player_html.replace("SONG_NAME", np_name)
                player_html = player_html.replace("SONG_EXT", np_ext)
                player_html = player_html.replace("AUDIO_SRC", audio_src)
                components.html(player_html, height=230)

            else:
                # ── No track state — cleaner card ──────────────────────────────
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #0d1b3e 0%, #1a3a6b 100%);
                    border-radius: 18px; padding: 24px; margin-bottom: 4px;
                ">
                    <div style="display:flex; align-items:center; gap:14px;">
                        <div style="
                            width:56px; height:56px; border-radius:14px;
                            background:rgba(255,255,255,0.08);
                            display:flex; align-items:center; justify-content:center;
                            font-size:26px; flex-shrink:0;
                        ">🎧</div>
                        <div>
                            <div style="
                                font-family:Inter,sans-serif; font-size:0.68rem;
                                font-weight:700; letter-spacing:1px; text-transform:uppercase;
                                color:rgba(255,255,255,0.35); margin-bottom:6px;
                            ">No Track Selected</div>
                            <div style="
                                font-family:'Barlow Condensed',sans-serif;
                                font-size:1.2rem; font-weight:800;
                                color:rgba(255,255,255,0.5);
                            ">Upload songs to start</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            cnt = len(songs)
            cnt_label = str(cnt) + (" songs" if cnt != 1 else " song")

            # Library Header — apna alag card
            st.markdown(
                '<div style="background:white;border-top-left-radius:10px;border-top-right-radius:10px;'
                'padding:16px 15px; margin-top:8px;'
                'display:flex;align-items:center;justify-content:space-between;">'
                '<div style="display:flex;align-items:center;gap:10px;">'
                '<span style="font-size:18px;">🎵</span>'
                '<span style="font-family:\'Barlow Condensed\',sans-serif;font-size:1.2rem;'
                'font-weight:800;color:#0d1b3e;">Library</span>'
                '</div>'
                '<span style="font-family:Inter,sans-serif;font-size:0.7rem;font-weight:700;'
                'color:#4f6ef7;background:#eef2ff;border:1.5px solid #c7d2fe;'
                'border-radius:999px;padding:4px 14px;">' + cnt_label + '</span>'
                '</div>',
                unsafe_allow_html=True
            )

            if not songs:
                st.markdown(
                    '<div style="background:white;border:1.5px solid #e4eaf5;'
                    'border-bottom-left-radius:10px;padding:34px 20px;text-align:center;border-bottom-right-radius:10px;'
                    'margin-top:2px;box-shadow:0 2px 12px rgba(0,0,0,0.06);">'
                    '<div style="font-size:2.8rem;margin-bottom:10px;">🎵</div>'
                    '<div style="font-family:Inter,sans-serif;font-size:1rem;'
                    'font-weight:700;color:#0d1b3e;">No songs yet</div>'
                    '<div style="font-family:Inter,sans-serif;font-size:0.78rem;'
                    'color:#94a3b8;margin-top:5px;">Upload MP3, WAV, or OGG to get started</div>'
                    '</div>',
                    unsafe_allow_html=True
                )
            else:
                for fname, fpath in songs:
                    is_active = fname == current
                    row_bg    = "#f0f4ff" if is_active else "#f8faff"
                    icon_bg   = "#0d1b3e" if is_active else "#1e3a8a"
                    pill_html = (
                        '<div style="display:inline-flex;align-items:center;gap:5px;'
                        'color:#4f6ef7;font-size:0.68rem;font-weight:600;'
                        'font-family:Inter,sans-serif;margin-top:3px;">'
                        '<div style="width:6px;height:6px;background:#4f6ef7;border-radius:50%;"></div>'
                        ' Now Playing</div>'
                    ) if is_active else ""

                    col_song, col_del = st.columns([10,1], gap="small")

                    with col_song:
                        st.markdown(
                            '<div style="background:' + row_bg + ';border: 1.5px solid #0d1b3e;'
                            'padding:10px 12px;margin-top:10px;'
                            'display:flex;align-items:center;gap:12px;">'
                            '<div style="width:42px;height:42px;border-radius:10px;'
                            'background:' + icon_bg + ';display:flex;align-items:center;'
                            'justify-content:center;font-size:18px;flex-shrink:0;">🎵</div>'
                            '<div style="flex:1;min-width:0;">'
                            '<div style="font-family:Inter,sans-serif;font-size:0.88rem;'
                            'font-weight:700;color:#0d1b3e;white-space:nowrap;overflow:hidden;'
                            'text-overflow:ellipsis;">' + clean_name(fname) + '</div>'
                            + pill_html +
                            '</div></div>',
                            unsafe_allow_html=True
                        )
                        if not is_active:
                            if st.button("Play", key="play_" + fname,
                                         use_container_width=True, type="primary"):
                                st.session_state.music_current = fname
                                st.rerun()

                    with col_del:
                        if st.button("✕", key="del_" + fname,
                                     use_container_width=True, type="secondary"):
                            try: os.remove(fpath)
                            except: pass
                            remaining = [f for f, _ in songs if f != fname]
                            st.session_state.music_current = remaining[0] if remaining else None
                            st.rerun()
    # ════════════════════════════════
    # RIGHT — Upload + Stats + Tips
    # ════════════════════════════════
    with col_right:

        st.markdown("""
            <div style="
                background: white;
                border-radius: 20px 20px 0 0;
                padding: 24px;
                box-shadow: 0 2px 16px rgba(0,0,0,0.08);
                margin-bottom: 0 !important;
            ">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                    <div style="
                        background:#2563EB; border-radius:10px;
                        width:38px; height:38px;
                        display:flex; align-items:center; justify-content:center;
                    ">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20"
                            fill="white" viewBox="0 0 24 24">
                            <path d="M12 2a1 1 0 0 1 .707.293l4 4a1 1 0 0 1-1.414 
                                    1.414L13 5.414V15a1 1 0 1 1-2 0V5.414L8.707 
                                    7.707A1 1 0 0 1 7.293 6.293l4-4A1 1 0 0 1 12 
                                    2zM4 17a1 1 0 0 1 1 1v1h14v-1a1 1 0 1 1 2 
                                    0v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1a1 1 0 
                                    0 1 1-1z"/>
                        </svg>
                    </div>
                    <span style="font-size:22px; font-weight:700; color:#1E293B;">Add Songs</span>                
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <style>
        /* Uploaded file preview hide karo */
                [data-testid="stFileUploaderFile"],
                [data-testid="stFileUploaderFileData"] {
                    display: none !important;
                }
        /* Uploader - top radius remove, sirf bottom rounded */
        [data-testid="stFileUploader"] {
            background: white !important;
            border-radius: 0 0 20px 20px !important;
            padding: 24px !important;
            border: none !important;
            box-shadow: 0 2px 16px rgba(0,0,0,0.08) !important;
            margin-top: -15px !important;
        }

        /* Inner dashed dropzone */
        [data-testid="stFileUploader"] section {
            background: #F0F7FF !important;
            border: 2px dashed #A8CEED !important;
            border-radius: 16px !important;
            padding: 48px 24px !important;
            min-height: 240px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            background: transparent !important;
            border: none !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 6px !important;
        }

        [data-testid="stFileUploaderDropzone"] svg {
            color: #3B82F6 !important;
            background: white !important;
            border-radius: 50% !important;
            padding: 14px !important;
            width: 52px !important;
            height: 52px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
            margin-bottom: 16px !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            text-align: center !important;
            gap: 4px !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] div span {
            color: #1E293B !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            display: block !important;
            text-align: center !important;
        }

        [data-testid="stFileUploaderDropzoneInstructions"] div small {
            color: #94A3B8 !important;
            font-size: 13px !important;
            display: block !important;
            text-align: center !important;
        }

        [data-testid="stFileUploader"] button {
            background: #2563EB !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 10px 32px !important;
            border: none !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            width: auto !important;
            min-width: 160px !important;
            max-width: 220px !important;
            white-space: nowrap !important;
            overflow: visible !important;
            margin: 16px auto 0 auto !important;
            display: block !important;
            box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
        }

        [data-testid="stFileUploader"] button:hover {
            background: #1D4ED8 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload music files",
            type=["mp3", "wav", "ogg"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if uploaded:
            saved = 0
            for uf in uploaded:
                dest = os.path.join(MUSIC_DIR, uf.name)
                if not os.path.exists(dest):
                    with open(dest, "wb") as out:
                        out.write(uf.read())
                    saved += 1
                    if st.session_state.music_current is None:
                        st.session_state.music_current = uf.name
            if saved:
                st.markdown(
                    '<div style="background:#f0fdf4;border:1.5px solid #bbf7d0;'
                    'border-radius:12px;padding:12px 16px;margin-top:10px;'
                    'font-family:Inter,sans-serif;font-size:0.85rem;'
                    'font-weight:600;color:#15803d;">✅ '
                    + str(saved) + ' song' + ('s' if saved > 1 else '') + ' added!</div>',
                    unsafe_allow_html=True
                )
                st.rerun()