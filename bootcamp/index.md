---
layout: default
title: "AI-Enabled Research Bootcamp"
description: "Oct 1 & Oct 5–8, 2026 · World Bank Group"
permalink: /bootcamp/
---

<div class="bootcamp">

<p class="crumb"><a href="{{ '/' | relative_url }}">&larr; All training materials</a></p>

{% include bootcamp-hero.html %}

<h2 id="about">About the bootcamp</h2>

{% for p in site.data.bootcamp.intro %}
<p>{{ p }}</p>
{% endfor %}

<h2 id="days">Choose a day</h2>

<div class="day-list">
{%- for d in site.data.bootcamp.days -%}
{%- assign dm = d.date | split: ' ' -%}
{%- assign n = 0 -%}{%- assign h = 0 -%}
{%- for s in d.sessions -%}
{%- unless s.kind -%}{%- assign n = n | plus: 1 -%}{%- if s.hands_on -%}{%- assign h = h | plus: 1 -%}{%- endif -%}{%- endunless -%}
{%- endfor -%}
<a class="day-row day-{{ d.tag }}" href="{{ '/bootcamp/day-' | append: d.id | append: '/' | relative_url }}">
<span class="day-date"><small>{{ dm[0] }}</small><b>{{ dm[1] }}</b><em>{{ d.weekday | slice: 0, 3 }}</em></span>
<span class="day-body">
<span class="day-title"><strong>Day {{ d.id }}</strong> · {{ d.theme }} <span class="track track-{{ d.tag }}">{{ d.track }}</span></span>
<span class="day-short">{{ d.short }}</span>
<span class="day-meta">{{ n }} sessions · {{ h }} hands-on</span>
</span>
<span class="day-cta">Go to Day {{ d.id }} &rarr;</span>
</a>
{%- endfor -%}
</div>

<p class="legend"><strong>New to AI?</strong> Start with Day 0 (setup), then attend Days 1&ndash;3. <strong>Already using AI tools?</strong> Skip Day 0, and add Day 4 for advanced workflows. Timing changes are always reflected first in the <a href="{{ site.data.bootcamp.agenda_url }}">live Canva agenda</a>.</p>

</div>
