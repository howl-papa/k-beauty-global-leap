---
layout: default
title: "케이스 스터디"
permalink: /case-studies/
---

<section class="case-studies">
  <h1>케이스 스터디</h1>
  <p>K-Beauty 산업 파트너와 진행한 협력 사례와 성과를 공유합니다.</p>

  {% for study in site['case-studies'] %}
    <article class="case-study-card">
      <h2><a href="{{ study.url | relative_url }}">{{ study.title }}</a></h2>
      <p>{{ study.excerpt | strip_html | truncate: 150 }}</p>
    </article>
  {% else %}
    <p>첫 케이스 스터디가 곧 업데이트될 예정입니다.</p>
  {% endfor %}
</section>
