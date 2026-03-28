import re

def parse_vcd(filename):
    signals = {}
    id_to_name = {}
    time = 0
    events = []
    
    with open(filename) as f:
        lines = f.readlines()
    
    in_defs = True
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if '$var' in line:
            parts = line.split()
            try:
                sig_id = parts[3]
                sig_name = parts[4]
                id_to_name[sig_id] = sig_name
                signals[sig_name] = []
            except:
                pass
                
        elif line.startswith('#'):
            try:
                time = int(line[1:])
            except:
                pass
                
        elif line.startswith('b'):
            parts = line.split()
            if len(parts) == 2:
                val = parts[0][1:]
                sig_id = parts[1]
                if sig_id in id_to_name:
                    name = id_to_name[sig_id]
                    signals[name].append((time, val))
                    
        elif len(line) == 2 and line[0] in '01xz':
            val = line[0]
            sig_id = line[1]
            if sig_id in id_to_name:
                name = id_to_name[sig_id]
                signals[name].append((time, val))
    
    return signals

def make_html(signals):
    # figure out time range
    all_times = []
    for events in signals.values():
        for t, v in events:
            all_times.append(t)
    if not all_times:
        print("No signal data found in VCD file.")
        return
    
    max_time = max(all_times)
    
    # order we want to show
    show_order = ['clk', 'rst_n', 'in', 'detected', 'current_state']
    ordered = [s for s in show_order if s in signals]
    for s in signals:
        if s not in ordered:
            ordered.append(s)

    rows_html = ""
    for sig in ordered:
        events = signals.get(sig, [])
        if not events:
            continue
        
        is_bus = any(len(v) > 1 for _, v in events)
        
        # build segments
        segs = []
        for i, (t, v) in enumerate(events):
            t_next = events[i+1][0] if i+1 < len(events) else max_time + 1000
            segs.append((t, t_next, v))
        
        seg_html = ""
        for (t, t_next, v) in segs:
            x = t / (max_time + 1000) * 100
            w = (t_next - t) / (max_time + 1000) * 100
            
            if is_bus:
                color = "var(--color-background-info)" if v != "x" else "var(--color-background-warning)"
                seg_html += f'''
                <div style="position:absolute;left:{x:.3f}%;width:{w:.3f}%;height:100%;
                     background:{color};border-right:1px solid var(--color-border-secondary);
                     display:flex;align-items:center;justify-content:center;overflow:hidden;">
                  <span style="font-size:10px;font-family:var(--font-mono);
                        color:var(--color-text-info);white-space:nowrap;">{v}</span>
                </div>'''
            else:
                if v == '1':
                    seg_html += f'''
                    <div style="position:absolute;left:{x:.3f}%;width:{w:.3f}%;height:100%;
                         background:var(--color-background-success);
                         border-right:1px solid var(--color-border-secondary);">
                    </div>'''
                elif v == '0':
                    seg_html += f'''
                    <div style="position:absolute;left:{x:.3f}%;width:{w:.3f}%;height:4px;
                         bottom:0;background:var(--color-border-secondary);"></div>'''
                else:
                    seg_html += f'''
                    <div style="position:absolute;left:{x:.3f}%;width:{w:.3f}%;height:100%;
                         background:var(--color-background-warning);opacity:0.5;"></div>'''

        rows_html += f'''
        <div style="display:flex;align-items:stretch;border-bottom:0.5px solid var(--color-border-tertiary);min-height:32px;">
          <div style="width:140px;flex-shrink:0;padding:0 12px;display:flex;align-items:center;
               font-size:12px;font-family:var(--font-mono);color:var(--color-text-secondary);
               border-right:0.5px solid var(--color-border-tertiary);background:var(--color-background-secondary);">
            {sig}
          </div>
          <div style="flex:1;position:relative;overflow:hidden;">
            {seg_html}
          </div>
        </div>'''

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Waveform — 1011 Sequence Detector</title>
<style>
  :root {{
    --color-background-primary: #ffffff;
    --color-background-secondary: #f5f5f3;
    --color-background-info: #e6f1fb;
    --color-background-success: #eaf3de;
    --color-background-warning: #faeeda;
    --color-border-tertiary: rgba(0,0,0,0.12);
    --color-border-secondary: rgba(0,0,0,0.25);
    --color-text-primary: #1a1a18;
    --color-text-secondary: #5f5e5a;
    --color-text-info: #0c447c;
    --font-mono: ui-monospace, monospace;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --color-background-primary: #1a1a18;
      --color-background-secondary: #242422;
      --color-background-info: #0c447c;
      --color-background-success: #173404;
      --color-background-warning: #412402;
      --color-border-tertiary: rgba(255,255,255,0.1);
      --color-border-secondary: rgba(255,255,255,0.2);
      --color-text-primary: #e8e6de;
      --color-text-secondary: #9c9a92;
      --color-text-info: #85b7eb;
    }}
  }}
  body {{ margin:0; background:var(--color-background-primary);
          color:var(--color-text-primary); font-family:sans-serif; }}
  h2 {{ margin:0; padding:16px 20px; font-size:15px; font-weight:500;
        border-bottom:0.5px solid var(--color-border-tertiary); }}
  .subtitle {{ font-size:12px; color:var(--color-text-secondary);
               padding:8px 20px 12px; }}
  .legend {{ display:flex; gap:16px; padding:8px 20px;
             border-bottom:0.5px solid var(--color-border-tertiary);
             font-size:11px; color:var(--color-text-secondary); }}
  .leg {{ display:flex; align-items:center; gap:6px; }}
  .leg-box {{ width:20px; height:12px; border-radius:2px; }}
</style>
</head>
<body>
<h2>Waveform viewer — 1011 sequence detector</h2>
<p class="subtitle">
  Simulation output from iverilog. Each column = one time unit. 
  Pattern 1011 detected when <code>detected</code> goes HIGH.
</p>
<div class="legend">
  <div class="leg"><div class="leg-box" style="background:var(--color-background-success)"></div>HIGH (1)</div>
  <div class="leg"><div class="leg-box" style="background:var(--color-border-secondary)"></div>LOW (0)</div>
  <div class="leg"><div class="leg-box" style="background:var(--color-background-info)"></div>Bus value</div>
</div>
<div style="overflow-x:auto;">
  {rows_html}
</div>
<p style="padding:12px 20px;font-size:11px;color:var(--color-text-secondary);">
  States: 000=IDLE  001=got-1  010=got-10  011=got-101  100=MATCH(detected)
</p>
</body>
</html>'''
    
    with open('waveform.html', 'w') as f:
        f.write(html)
    print("Done! Opening waveform.html in your browser...")

sigs = parse_vcd('waves.vcd')
make_html(sigs)
