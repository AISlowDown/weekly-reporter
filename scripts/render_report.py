#!/usr/bin/env python3
"""Render verified project/day data with the bundled weekly-report HTML layout."""
import argparse
import csv
from datetime import date, timedelta
from html import escape
import json
import math
from pathlib import Path
import re

PASTELS = ['#ACC9EA','#F1BDB7','#AAD8C4','#C8B8E0','#E4BED8','#EAC69E','#DED5A5','#CEDDB2','#F1D99E','#BDDCE0','#C9C4BA','#B9D1C2']
INKS = ['#355577','#7B4B46','#355E50','#5F4C79','#704D67','#745238','#655D38','#52623B','#786133','#3D6166','#555149','#3D5F50']
CHART = ['#9E0142','#D53E4F','#F46D43','#FDAE61','#FEE08B','#E6F598','#ABDDA4','#66C2A5','#3288BD','#5E4FA2','#876C89','#627C84']
ROOT = Path(__file__).resolve().parents[1]

def e(value):
    return escape(str(value), quote=True)

def render(data, output):
    start, end = date.fromisoformat(data['start']), date.fromisoformat(data['end'])
    if not 0 <= (end-start).days <= 30:
        raise ValueError('Report must cover 1–31 calendar days.')
    days = [(start+timedelta(days=i)).isoformat() for i in range((end-start).days+1)]
    mode = data.get('time_mode','none')
    if mode not in ('none','estimated','measured'):
        raise ValueError('time_mode must be none, estimated or measured.')
    missing = set(data.get('missing_dates',[]))
    if not missing <= set(days):
        raise ValueError('missing_dates outside report range.')
    projects = data['projects']
    if not projects or len({p['id'] for p in projects}) != len(projects):
        raise ValueError('Provide projects with unique IDs.')
    known = {}
    records = {}
    partial = bool(data.get('partial',False) or missing)
    for p in projects:
        rec = {}
        for r in p.get('days',[]):
            d = r['date']
            if d not in days or d in rec:
                raise ValueError('Each project needs unique dates within range.')
            m = r.get('minutes')
            if m is not None and (isinstance(m,bool) or not isinstance(m,(int,float)) or not math.isfinite(m) or m < 0 or m != int(m)):
                raise ValueError('minutes must be nonnegative whole minutes or null.')
            if d in missing and m is not None:
                raise ValueError('Do not assign time to a missing date.')
            if not isinstance(r.get('actions',[]),list):
                raise ValueError('actions must be a list of short descriptions.')
            if mode != 'none' and m is None:
                partial = True
            rec[d] = r
        records[p['id']] = rec
        vals = [r['minutes'] for r in rec.values() if r.get('minutes') is not None]
        known[p['id']] = sum(vals) if vals else None
        if mode != 'none' and not vals:
            partial = True
    if mode != 'none':
        projects = sorted(projects,key=lambda p: (known[p['id']] is None,-(known[p['id']] or 0)))
    daytot = {}
    for d in days:
        vals = [records[p['id']][d]['minutes'] for p in projects if d in records[p['id']] and records[p['id']][d].get('minutes') is not None]
        daytot[d] = sum(vals) if vals else None
        if mode != 'none' and not vals:
            partial = True
        if daytot[d] is not None and daytot[d] > 1440:
            raise ValueError('Daily allocations exceed 24 hours; check overlapping records.')
    total = sum(v for v in known.values() if v is not None)
    showtime = mode != 'none' and any(v is not None for v in known.values())
    prefix = '约 ' if mode == 'estimated' else ''
    def fmt(m):
        if m is None: return '用时未知'
        h,mins = divmod(round(m),60)
        return prefix + (f'{h}小时' if h else '') + (f'{mins}分' if mins or not h else '')
    def style(i):
        return f'--project:{PASTELS[i%len(PASTELS)]};--project-ink:{INKS[i%len(INKS)]}'
    def amount(pid):
        return fmt(known[pid]) if showtime else ''
    # Stable IDs map all table, summary, and chart calculations to the same records.
    tasks = []
    highlighted = [p for p in projects if p.get('featured')]
    for p in (highlighted or projects)[:3]:
        i = projects.index(p)
        bullets = p.get('highlights',[])[:3] or [p.get('outcome','本周进展待补充。')]
        tasks.append(f'<article class="task" style="{style(i)}"><div class="task-top"><span class="task-no">{len(tasks)+1:02}</span><span class="task-days">{amount(p["id"])}</span></div><h3>{e(p["name"])}</h3><ul>'+''.join(f'<li>{e(v)}</li>' for v in bullets)+'</ul></article>')
    table=[]; details=[]
    for i,p in enumerate(projects):
        rec=records[p['id']]; cells=[]; entries=[]
        for d in days:
            r=rec.get(d)
            if r:
                items=''.join(f'<li>{e(a)}</li>' for a in r.get('actions',[])[:3])
                if showtime: items+=f'<li class="cell-time">{fmt(r.get("minutes"))}</li>'
                cells.append(f'<td><ul class="cell-activities">{items}</ul></td>')
                entries.append(f'<li><time>{d[5:].replace("-",".")}</time><span>{e(r.get("detail") or "；".join(r.get("actions",[])))}</span></li>')
            else:
                cells.append('<td class="missing">记录缺失</td>' if d in missing else '<td></td>')
        table.append(f'<tr style="{style(i)}"><th scope="row"><i class="key"></i><span>{e(p["name"])}</span></th>'+''.join(cells)+'</tr>')
        notes=''.join(f'<p class="detail-note"><strong>{label}</strong>　{e(p[key])}</p>' for key,label in [('outcome','进展与状态'),('next','下一步')] if p.get(key))
        paper=f'<p class="paper">{e(p["paper_title"])}</p>' if p.get('paper_title') else ''
        details.append(f'<details class="project-detail" style="{style(i)}"><summary><i class="key"></i>{e(p["name"])}<span class="project-total">{amount(p["id"])}</span></summary>{paper}<ul>{"".join(entries)}</ul>{notes}</details>')
    chart=''; overview=''
    if showtime:
        label='可估算部分合计' if partial and mode=='estimated' else ('已记录部分合计' if partial else ('本周估算投入' if mode=='estimated' else '本周记录投入'))
        overview=f'<section class="time-overview"><div class="week-time"><span class="time-label">{label}</span><strong>{fmt(total)}</strong><small>{"活动窗口估算" if mode=="estimated" else "计时记录"}{" · 部分记录，非全周总工时" if partial else ""}</small></div><div class="day-times">'+''.join(f'<div><span>{d[5:].replace("-",".")}</span><strong>{fmt(daytot[d])}</strong></div>' for d in days)+'</div></section>'
        top=max(1,math.ceil(max((v or 0) for v in daytot.values())/60/2)*2)
        width=max(900,130*len(days));base=320; scale=260/top;stride=(width-80)/len(days)
        svg=[f'<svg viewBox="0 0 {width} 380" role="img" aria-label="每日已记录投入堆积图">']
        for n in range(5):
            h=top*n/4;y=base-h*scale
            svg.append(f'<line x1="45" y1="{y}" x2="{width-10}" y2="{y}" stroke="#e4e6de"/><text class="axis-label" x="8" y="{y+4}">{h:g}h</text>')
        for di,d in enumerate(days):
            x=70+di*stride; y=base;dt=daytot[d]
            if dt is None:svg.append(f'<text class="axis-label" x="{x+26}" y="{base-20}" text-anchor="middle">未知</text>')
            for i,p in enumerate(projects):
                m=records[p['id']].get(d,{}).get('minutes') or 0
                if not m:continue
                ht=m/60*scale;y-=ht;pct=m/dt*100
                color=CHART[i] if i<len(CHART) else f'hsl({(i*137.5)%360:.0f} 42% 50%)'
                tip=f'{d} · {p["name"]}｜{fmt(m)}｜占当日已记录投入 {pct:.1f}%'
                svg.append(f'<g class="stack-segment" tabindex="0" role="img" aria-label="{e(tip)}" data-tip="{e(tip)}"><title>{e(tip)}</title><rect x="{x}" y="{y}" width="54" height="{ht}" fill="{color}" stroke="white" stroke-width="1"/></g>')
                if ht>=23:svg.append(f'<text x="{x+27}" y="{y+ht/2+4}" text-anchor="middle" class="segment-pct" style="fill:{"white" if i in (0,1,8,9,10,11) else "#28332f"}">{pct:.0f}%</text>')
            if dt is not None:svg.append(f'<text class="bar-total" x="{x+27}" y="{y-12}" text-anchor="middle">{dt/60:.2f}h</text>')
            svg.append(f'<text class="axis-date" x="{x+27}" y="350" text-anchor="middle">{d[5:].replace("-",".")}</text>')
        svg.append('</svg>')
        legend=''.join(f'<li><i style="background:{CHART[i] if i<len(CHART) else f"hsl({(i*137.5)%360:.0f} 42% 50%)"}"></i>{e(p["name"])}<strong>{(known[p["id"]] or 0)/total*100:.1f}%</strong></li>' for i,p in enumerate(projects) if known[p['id']] and total)
        chart='<section id="time-chart" class="section"><div class="chart-heading"><h2><span>02</span>每日投入分布</h2><p>柱高：当日已记录时长 · 色块：占当日已记录投入比例</p></div><div class="stack-shell"><div class="stack-scroll">'+''.join(svg)+'</div><div class="legend-heading"><span>项目图例</span><span>占全部已记录投入</span></div><ul class="stack-legend">'+legend+'</ul></div></section>'
    weekdays='一二三四五六日'
    head='<tr><th>项目 / 专项工作</th>'+''.join(f'<th>{d[-2:]}<small>周{weekdays[date.fromisoformat(d).weekday()]}</small></th>' for d in days)+'</tr>'
    obs=data.get('obsidian_url','')
    if obs and not obs.startswith('obsidian://open?'):raise ValueError('Invalid Obsidian open URL.')
    slots={'TITLE':e(f'{data.get("author", "学术周报")}｜{start}—{end}'),'AUTHOR':e(data.get('author') or '学术周报'),'WEEK':f'WEEK {start.isocalendar().week}','DATES':f'{str(start).replace("-",".")} — {str(end).replace("-",".")}','TIMEZONE':e(data.get('timezone','')),'CHART_NAV':'<a href="#time-chart">投入分布</a>' if showtime else '', 'TIME_OVERVIEW':overview,'TASKS':''.join(tasks),'CHART':chart,'GANTT_NUMBER':'03' if showtime else '02','DETAIL_NUMBER':'04' if showtime else '03','TABLE_HEAD':head,'TABLE_BODY':''.join(table),'DETAILS':''.join(details),'NOTES':e(data.get('notes','记录覆盖情况待说明。')),'OBSIDIAN':f'<a class="obsidian" href="{e(obs)}">在 Obsidian 中打开</a>' if obs else ''}
    template=(ROOT/'assets/weekly-report.html').read_text()
    result=re.sub(r'@@([A-Z_]+)@@',lambda m:slots[m.group(1)],template)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(result,encoding='utf-8')
    with output.with_suffix('.csv').open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.writer(f);writer.writerow(['project_id','project','date','actions','minutes','time_mode'])
        for p in projects:
            for d in days:
                r=records[p['id']].get(d,{})
                writer.writerow([p['id'],p['name'],d,'；'.join(r.get('actions',[])),r.get('minutes') if mode!='none' else None,mode])
    return {'html':str(output),'csv':str(output.with_suffix('.csv')),'minutes':total if showtime else None,'partial':partial}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('data',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args()
    print(json.dumps(render(json.loads(args.data.read_text()),args.output),ensure_ascii=False))
