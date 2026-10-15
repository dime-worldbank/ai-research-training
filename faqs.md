---
layout: default
title: "Frequently Asked Questions"
description: "Frequently asked questions about using AI in your research"
permalink: /faqs/
---

<!--
HOW TO EDIT
- Edit section titles and order in _data/faqs/_config-sections.yml; file names omit .yml and also set section anchors.
- Edit questions in _data/faqs/<file>.yml; their list order sets their order on this page.
- Each question has a unique id (keep existing ids for stable links), a title, and an answer.
- Write answers as normal Markdown under answer: |, indenting every nonblank answer line by two spaces.
- Blank lines create paragraphs; Markdown lists and links work normally. Use <br> for a forced line break.
- Use relative internal links such as ../roadmap/; Liquid expressions inside YAML answers are not evaluated.
- Set coming_soon: true for unfinished answers; remove it when ready. Optional coming_soon_position: after puts the label after the answer.
- New section: create its YAML file and add its file name and title to _config-sections.yml.
- Add 🔒 to the link text when a link needs a World Bank login.
-->

<div class="faq">

<p class="crumb"><a href="{{ '/' | relative_url }}">&larr; All training materials</a></p>

Answers to the questions we hear most often from researchers as they bring AI into their own work, whether or not you attended one of our trainings. We are still writing some of these answers; questions marked <span class="faq-soon">Coming soon</span> will be filled in over the coming weeks.

<p class="faq-legend">🔒 Internal only: the link needs a World Bank login.</p>

<nav class="faq-topics" aria-label="FAQ topics">
{% for section in site.data.faqs['_config-sections'] %}
  <a href="#{{ section.file | escape }}">{{ section.title | escape }}</a>
{% endfor %}
</nav>

{% for section in site.data.faqs['_config-sections'] %}
<h2 id="{{ section.file | escape }}">{{ section.title | escape }}</h2>

{% assign questions = site.data.faqs[section.file] %}
{% for question in questions %}
<details class="faq-item" id="{{ question.id | escape }}">
<summary>{{ question.title | escape }}</summary>
<div class="faq-answer">
{% if question.coming_soon and question.coming_soon_position != 'after' %}
<p class="faq-soon">Coming soon</p>
{% endif %}
{{ question.answer | default: '' | markdownify }}
{% if question.coming_soon and question.coming_soon_position == 'after' %}
<p class="faq-soon">Coming soon</p>
{% endif %}
</div>
</details>
{% endfor %}
{% endfor %}

<p class="home-footer">Don't see your question? Write to <a href="mailto:dimeanalytics@worldbank.org">dimeanalytics@worldbank.org</a>.</p>

</div>
