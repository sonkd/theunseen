---
title: Researches
permalink: /archive/researches/
layout: default
excerpt: All researches.
comments: false
---

<section class="header pt-20">
  <h1 class="header-title text-center" aria-label="Archived">Archived</h1>
</section>

<!-- FILTER NAV -->
<nav class="mb-6 flex gap-4 text-sm font-medium mx-auto">
  {% assign current_type = page.archive_type | default: 'researches' %}
  {% assign filters = "all,quotes,researches,articles" | split: "," %}
  {% for filter in filters %}
    {% if current_type == filter %}
      {% assign is_active = true %}
    {% else %}
      {% assign is_active = false %}
    {% endif %}
    <a href="/archive/{% unless filter == 'all' %}{{ filter }}{% endunless %}/"
       class="px-3 py-1 rounded-full border 
              {% if is_active %}bg-blue-600 text-white border-blue-600 hover:bg-blue-700{% else %}text-gray-600 border-gray-300 hover:bg-gray-100{% endif %}">
      {{ filter | capitalize }}
    </a>
  {% endfor %}
</nav>

<!-- POSTS LIST -->
<div class="space-y-4">
  {% assign posts = "" %}
  {% if current_type == "researches" %}
    {% assign posts = site.researches | sort: "title" %}

  {% for post in posts %}
    <article class="p-4 border bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow">
      <h2 class="text-lg font-semibold text-gray-900 mb-1">
        <a href="{{ post.url }}" class="hover:underline">{{ post.title }}</a>
      </h2>
      <p class="text-sm text-gray-500">{{ post.date | date: "%B %d, %Y" }}</p>
      
      {% if post.tags %}
        <div class="mt-2 flex flex-wrap gap-2">
          {% for tag in post.tags %}
            <span class="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full">
              #{{ tag }}
            </span>
          {% endfor %}
        </div>
      {% endif %}
    </article>
  {% endfor %}
{% endif %}
</div>