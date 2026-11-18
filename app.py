    l, r = st.columns([1.1, 1])
    with l:
        st.markdown('<div style="padding-top:2.2rem"><div class="eyebrow gold">AI voice authenticity</div><div class="hero-t">Trust every voice.<br><span class="gold"><i>Verify every signal.</i></span></div>'
          '<p class="mute" style="max-width:34rem;font-size:1.05rem">Advanced AI-powered voice analysis designed to identify synthetic, cloned and potentially manipulated audio.</p></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("Start detecting  →", use_container_width=True, on_click=go_to, args=("Detect",))
        c2.button("How it works", use_container_width=True, on_click=go_to, args=("About",))
    with r: components.html(hero(T), height=450)
    for col, (n, t, d) in zip(st.columns(3), [("16 kHz", "Mono analysis", "Every clip is resampled the same way before detection."), ("64", "Mel bands", "A time-frequency picture of the voice for the CNN."), ("2", "Detection models", "Baseline V1 and the advanced V2 with a prevention decision.")]):
        with col: card(f'<div class="num">{n}</div><b>{t}</b><p class="mute">{d}</p>')
    st.markdown('<div class="marq"><div class="track">' + MARQ + '</div></div>', unsafe_allow_html=True)
    for col, (ic, t, d) in zip(st.columns(3), [("🎙️", "Upload or record", "Drop a WAV or MP3, or record straight from your microphone."),
                                               ("🧠", "CNN-powered verdicts", "Genuine and spoof confidence straight from the trained PyTorch model."),
                                               ("🛡️", "Honest by design", "If the model is offline you get a clear status, never an invented score.")]):
        with col: card(f'<div class="ico">{ic}</div><b>{t}</b><p class="mute">{d}</p>')
    st.markdown('<div class="band"><div class="eyebrow gold">Ready when you are</div><div class="hero-t" style="font-size:clamp(2rem,5vw,3.2rem)">Is that voice <span class="gold"><i>real?</i></span></div><p class="mute">Drop in a recording and let VoxGuard read the signal.</p></div>', unsafe_allow_html=True)
    st.button("Start analysing  →", key="band_go", on_click=go_to, args=("Detect",))

elif page == "Detect":
    head("Workspace", "Detect a voice", "Choose a model, add a recording, and read the full report right below. All in one place.")
    model_choice = st.selectbox("Detection model", ["V1 — Baseline Model", "V2 — Advanced Model"], key="detection_model")
    selected_model = "V2" if model_choice.startswith("V2") else "V1"

    cu, cm = st.columns(2)
    with cu:
        st.markdown("**Upload a file**")
        rec = uploader("main", model_version=selected_model)
        # Only a newly uploaded file/model selection becomes the active result.
        # This prevents the upload result from replacing a microphone result on reruns.
        current_upload_id = ss.get("main_id")
        if rec is not None and current_upload_id != ss.get("last_upload_seen"):
            ss.cur = rec
            ss.active_source = "upload"
            ss.last_upload_seen = current_upload_id
        if rec is not None and ss.get("active_source") == "microphone":
            if st.button("Show uploaded-file result", key="show_upload_result", use_container_width=True):
                ss.cur = rec
                ss.active_source = "upload"

    with cm:
        st.markdown("**Or record with your microphone**")
        mic_audio = st.audio_input("Click to record your voice", sample_rate=SR, key="voxguard_microphone")
        if mic_audio is not None:
            st.caption("Please enter the audio using microphone for audio analysis")
            if st.button("Analyze recorded voice", key="analyze_mic", use_container_width=True):
                mic_hash = hashlib.sha256(mic_audio.getvalue()).hexdigest()
                mic_id = (mic_hash, selected_model)
                try:
                    with st.spinner("Analysing microphone recording…"):
                        mrec = process(
                            mic_audio,
                            model_version=selected_model,
                            source="microphone",
                        )
                    ss.cur = mrec
                    ss.active_source = "microphone"
                    if mrec["R"].get("status") == "ok":
                        st.success("Microphone recording analysed successfully by the selected trained model.")
                    else:
                        st.warning("Microphone recording was captured, but the model could not produce a prediction. See the model status below.")
                except Exception as exc:
                    st.error(f"Microphone analysis failed: {exc}")

    if rec is not None and ss.get("active_source") is None and ss.cur is None:
        ss.cur = rec
        ss.active_source = "upload"

    if ss.cur:
        show_result(ss.cur)
        st.button("Clear result", key="clear_cur", on_click=clear_cur)
    else:
        card('<div class="eyebrow">Awaiting signal</div><div class="big">Add a voice clip to begin</div><p class="mute">VoxGuard decodes the audio, draws its Mel spectrogram and asks the trained CNN for a verdict. Your report appears here.</p>' + EQ
             + '<span class="pill">WAV</span><span class="pill">MP3</span><span class="pill">Microphone</span><span class="pill">Up to 100 MB</span>')

elif page == "Compare":
    head("Side by side", "Compare two samples", "Compares model outputs and audio characteristics only. It does not identify speakers.")
    l, r = st.columns(2)
    with l: A = uploader("cA", "Sample A")
    with r: B = uploader("cB", "Sample B")
    if A and B:
        for idx, (col, rec) in enumerate(zip(st.columns(2), (A, B))):
            with col:
                card(meta(rec)); status_box(rec["R"]); verdict(rec["R"])
                plot(fig_wave(rec["F"], T), chart_key=f"compare_waveform_{idx}")
                plot(fig_mel(rec["F"], T), chart_key=f"compare_mel_{idx}")
                F = rec["F"]; st.caption(f'Centroid {np.mean(F["cent"]):.0f} Hz · Rolloff {np.mean(F["roll"]):.0f} Hz · Dominant {F["dom"]:.0f} Hz')
    else:
        card('<div class="eyebrow">Awaiting two samples</div><div class="big">Weigh two voices side by side</div><p class="mute">Upload Sample A and Sample B to compare spectrograms, predictions and audio characteristics.</p>' + EQ)

elif page == "History":
    head("Records", "Detection history")
    h = hist_load()
    if not h:
        card('<div class="eyebrow">Nothing here yet</div><div class="big">No analyses yet</div>' + EQ)
        st.button("Go to Detect  →", key="es_hist", on_click=go_to, args=("Detect",))
    for r in h:
        lab = {"genuine": "Genuine", "spoof": "AI / Spoof", "genuine_demo": "Genuine (Mic Demo)"}.get(r.get("label"), "No prediction")
        conf = f' · {pct(max(r["genuine"], r["spoof"]))}' if r.get("genuine") is not None else ""
        with st.expander(f'{r["name"]} · {r["ts"]} · {lab}{conf}'):
            st.write(f'Status: **{r.get("status", "unknown")}** · Source {r.get("source", "upload")} · Model {r.get("model", "V1")} · Duration {r.get("duration", "?")} s')
            if r.get("genuine") is not None: st.write(f'Genuine {pct(r["genuine"])} · Spoof {pct(r["spoof"])}')
            if r.get("note"): st.caption(r.get("note", ""))
    if h and st.button("Clear history"): hist_clear(); st.rerun()
    st.caption("Stored in a local JSON file on the server. On shared hosting it may be visible to all visitors and reset on restart.")

else:
    head("About", "VoxGuard", "An AI-based voice authenticity detection system designed to help identify synthetic and cloned voice recordings.")
    steps = [("Audio input", "WAV/MP3 decoded to mono."), ("Preprocessing", "Librosa resampling and normalisation."), ("Mel spectrogram", "Time-frequency image of the voice."),
             ("CNN (PyTorch)", "Convolutional network trained by Member 2."), ("Classification", "Genuine vs spoof confidence.")]
    st.markdown('<div class="flow">' + "".join(f'<div class="card step"><div class="num">{i+1}</div><b>{t}</b><p class="mute">{d}</p></div>' for i, (t, d) in enumerate(steps)) + '</div>', unsafe_allow_html=True)
    for col, (n, r_, w) in zip(st.columns(3), [("Antony", "Member 1", "Audio Preprocessing"), ("Afan", "Member 2", "Deep Learning and Detection Model"), ("Abhishek", "Member 3", "Website Development, UI/UX and Integration")]):
        with col: card(f'<div class="avatar">{n[0]}</div><div class="eyebrow">{r_}</div><div class="big">{n}</div><p class="mute">{w}</p>')
    card(f'<div class="eyebrow">Contact</div><div class="big">Questions, feedback or collaboration?</div><p class="mute">Write to us and we will get back to you.</p><a class="cta" href="mailto:{CONTACT}">✉ {CONTACT}</a>')

footer()
