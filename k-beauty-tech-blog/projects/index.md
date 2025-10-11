---
layout: default
title: "프로젝트"
permalink: /projects/
---

<section class="projects">
  <h1>프로젝트 모음</h1>
  <p>K-Beauty Global Leap와 관련된 연구 및 개발 프로젝트를 소개합니다.</p>

  {% for project in site.projects %}
    <article class="project-card">
      <h2><a href="{{ project.url | relative_url }}">{{ project.title }}</a></h2>
      {% if project.subtitle %}
        <p>{{ project.subtitle }}</p>
      {% endif %}
      <p>{{ project.excerpt | strip_html | truncate: 150 }}</p>
    </article>
  {% else %}
    <p>곧 프로젝트 사례가 업데이트될 예정입니다.</p>
  {% endfor %}
</section>
