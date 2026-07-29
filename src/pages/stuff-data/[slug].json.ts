import fs from 'fs/promises'
import path from 'path'
import matter from 'gray-matter'

export const prerender = true

export async function getStaticPaths() {
  const dir = path.resolve('./content/stuff')
  const entries = await fs.readdir(dir, { withFileTypes: true })
  const slugs = []

  for (const entry of entries) {
    if (entry.isFile() && entry.name.endsWith('.md')) {
      slugs.push({ params: { slug: entry.name.replace(/\.md$/, '') } })
    }
  }

  return slugs
}

function renderMarkdown(markdown) {
  const escapeHtml = text => text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  const inline = text => escapeHtml(text)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>')

  const lines = markdown.split(/\r?\n/)
  let html = ''
  let inList = false

  for (const rawLine of lines) {
    const line = rawLine.trim()
    if (!line) {
      if (inList) {
        html += '</ul>'
        inList = false
      }
      continue
    }

    const headingMatch = line.match(/^(#{1,6})\s+(.+)$/)
    if (headingMatch) {
      if (inList) {
        html += '</ul>'
        inList = false
      }
      const level = headingMatch[1].length
      html += `<h${level}>${inline(headingMatch[2])}</h${level}>`
      continue
    }

    const listMatch = line.match(/^[-*]\s+(.+)$/)
    if (listMatch) {
      if (!inList) {
        html += '<ul>'
        inList = true
      }
      html += `<li>${inline(listMatch[1])}</li>`
      continue
    }

    html += `<p>${inline(line)}</p>`
  }

  if (inList) html += '</ul>'
  return html
}

export async function GET({ params }) {
  try {
    const slug = params.slug
    const filePath = path.resolve('./content/stuff', `${slug}.md`)
    const raw = await fs.readFile(filePath, 'utf-8')
    const { data, content } = matter(raw)
    const body_html = renderMarkdown(content)
    const payload = {
      title: data.title || slug,
      front: data.front || data.title || '',
      back: data.back || '',
      refs: Array.isArray(data.refs) ? data.refs : [],
      links: Array.isArray(data.links) ? data.links : [],
      strategy: data.strategy || '',
      body_html,
    }
    return new Response(JSON.stringify(payload), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
      },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Not found' }), { status: 404 })
  }
}
