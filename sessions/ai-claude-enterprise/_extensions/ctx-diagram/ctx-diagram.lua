-- ctx-diagram: AI interfaces -> Context Window -> Models
--
-- Usage:
--   {{< ctx-diagram interfaces="mAI;ChatGPT" models="Model X;Model Y;Model Z" >}}
--
-- Arguments:
--   interfaces  ";"-separated list of left-hand nodes
--   models      ";"-separated list of right-hand nodes
--   model-icons ";"-separated list of icons for the model nodes, matched by
--               position to "models". One of "nn" (default, neural network),
--               "lock" (padlock, e.g. for a secure/private server), or "spy"
--               (spy icon, e.g. for a non-secure server). A single value
--               applies to every model node. Missing entries default to "nn".
--   center      label of the center node (default "Context|Window")
--   color            context window and line color (default "#D5B84E")
--   interface-color  interface node fill (default "#2599CD"; logo nodes are white)
--   model-color      model node fill (default "#000000")
--   height      CSS max-height of the diagram (default "520px")
--
-- In any label, "|" is a line break. An item ending in .png/.jpg/.jpeg/.svg/.gif
-- is drawn as a logo, embedded as base64 so it survives self-contained output.
-- Model nodes show an icon (see model-icons) with the name at the bottom. The
-- center node shows its label as a title with lines mimicking text below.

local diagram_count = 0

-- Fixed geometry in viewBox units (1000 x 600)
local VB_W, VB_H = 1000, 600
local MID_Y = VB_H / 2
local CENTER = { x = 410, y = 180, w = 180, h = 240 }
local LEFT_X, RIGHT_X, SIDE_W = 40, 780, 180
local LEFT_BUS, RIGHT_BUS = 315, 685
local USABLE_H, GAP, MAX_NODE_H = 560, 30, 150

local function xml_escape(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local function split(s, sep)
  local out = {}
  for part in (s .. sep):gmatch("(.-)" .. sep:gsub("%p", "%%%0")) do
    part = part:match("^%s*(.-)%s*$")
    if part ~= "" then table.insert(out, part) end
  end
  return out
end

local b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
local function base64(data)
  return ((data:gsub(".", function(x)
    local r, b = "", x:byte()
    for i = 8, 1, -1 do r = r .. (b % 2 ^ i - b % 2 ^ (i - 1) > 0 and "1" or "0") end
    return r
  end) .. "0000"):gsub("%d%d%d?%d?%d?%d?", function(x)
    if #x < 6 then return "" end
    local c = 0
    for i = 1, 6 do c = c + (x:sub(i, i) == "1" and 2 ^ (6 - i) or 0) end
    return b64chars:sub(c + 1, c + 1)
  end) .. ({ "", "==", "=" })[#data % 3 + 1])
end

local function is_image(item)
  local ext = item:lower():match("%.(%w+)$")
  return ext == "png" or ext == "jpg" or ext == "jpeg" or ext == "svg" or ext == "gif"
end

local function text_label(label, cx, cy, size)
  local lines = split(label, "|")
  local line_h = size * 1.25
  local first_y = cy - (#lines - 1) * line_h / 2
  local out = {}
  for i, line in ipairs(lines) do
    table.insert(out, string.format(
      '<tspan x="%.1f" y="%.1f">%s</tspan>', cx, first_y + (i - 1) * line_h, xml_escape(line)))
  end
  return string.format(
    '<text fill="#FFFFFF" font-size="%d" text-anchor="middle" dominant-baseline="central">%s</text>',
    size, table.concat(out))
end

local BORDER = "#000000"

local function box(x, y, w, h, color)
  return string.format(
    '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="22" fill="%s" stroke="%s" stroke-width="2"/>',
    x, y, w, h, color, BORDER)
end

-- Neural network icon (3-4-3 layers) fitted inside the given area
local function nn_icon(x, y, w, h)
  local layers = { 3, 4, 3 }
  local r = math.min(w, h) * 0.07
  local pts = {}
  for li, n in ipairs(layers) do
    local px = x + r + (li - 1) * (w - 2 * r) / (#layers - 1)
    pts[li] = {}
    for ni = 1, n do
      pts[li][ni] = { px, y + r + (ni - 0.5) * (h - 2 * r) / n }
    end
  end
  local out = {}
  for li = 1, #layers - 1 do
    for _, a in ipairs(pts[li]) do
      for _, b in ipairs(pts[li + 1]) do
        table.insert(out, string.format(
          '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="1.5"/>',
          a[1], a[2], b[1], b[2]))
      end
    end
  end
  for _, layer in ipairs(pts) do
    for _, p in ipairs(layer) do
      table.insert(out, string.format('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFFFFF"/>', p[1], p[2], r))
    end
  end
  return table.concat(out)
end

-- Padlock icon (secure server): shackle ring behind a body rect, so the
-- bottom of the ring is covered by the body; a cutout keyhole uses the
-- node's own fill color so it reads as a hole rather than a solid mark.
local function lock_icon(x, y, w, h, color)
  local size = math.min(w, h)
  local cx, cy = x + w / 2, y + h / 2
  local body_w, body_h = size * 0.64, size * 0.5
  local body_x = cx - body_w / 2
  local body_y = cy - body_h / 2 + size * 0.1
  local shackle_r = body_w * 0.36
  local shackle_sw = size * 0.11
  local out = {}
  table.insert(out, string.format(
    '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="#FFFFFF" stroke-width="%.1f"/>',
    cx, body_y, shackle_r, shackle_sw))
  table.insert(out, string.format(
    '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#FFFFFF"/>',
    body_x, body_y, body_w, body_h, size * 0.08))
  table.insert(out, string.format(
    '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"/>',
    cx - size * 0.07, body_y + body_h * 0.22, size * 0.14, body_h * 0.42, size * 0.03, color))
  return table.concat(out)
end

-- Spy icon (non-secure server): hat silhouette over sunglasses, with the
-- lenses cut out in the node's own fill color.
local function spy_icon(x, y, w, h, color)
  local size = math.min(w, h)
  local cx = x + w / 2
  local brim_w, brim_h = size * 0.95, size * 0.12
  local brim_y = y + h * 0.5 - size * 0.28
  local top_w1, top_w2, top_h = size * 0.55, size * 0.4, size * 0.22
  local out = {}
  table.insert(out, string.format(
    '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#FFFFFF"/>',
    cx - top_w1 / 2, brim_y, cx + top_w1 / 2, brim_y, cx + top_w2 / 2, brim_y - top_h, cx - top_w2 / 2, brim_y - top_h))
  table.insert(out, string.format(
    '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#FFFFFF"/>',
    cx - brim_w / 2, brim_y, brim_w, brim_h, brim_h / 2))
  local gl_y = brim_y + brim_h + size * 0.14
  local lens_w, lens_h = size * 0.3, size * 0.2
  local gap = size * 0.1
  local inset = lens_w * 0.15
  for _, side in ipairs({ -1, 1 }) do
    local lx = cx + side * (gap / 2 + (side < 0 and lens_w or 0))
    table.insert(out, string.format(
      '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#FFFFFF"/>',
      lx, gl_y, lens_w, lens_h, lens_h * 0.3))
    table.insert(out, string.format(
      '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"/>',
      lx + inset, gl_y + inset, lens_w - 2 * inset, lens_h - 2 * inset, lens_h * 0.2, color))
  end
  table.insert(out, string.format(
    '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#FFFFFF"/>',
    cx - gap / 2, gl_y + lens_h * 0.35, gap, lens_h * 0.15))
  return table.concat(out)
end

local MODEL_ICONS = { nn = nn_icon, lock = lock_icon, spy = spy_icon }

-- Model node: icon on top (neural network by default, or lock/spy), name at the bottom
local function model_node(label, x, y, w, h, color, size, icon)
  local icon_fn = MODEL_ICONS[icon] or nn_icon
  local n_lines = #split(label, "|")
  local label_h = n_lines * size * 1.25
  local pad = 12
  local icon_h = h - label_h - 3 * pad
  if icon_h < 35 then
    return box(x, y, w, h, color) .. text_label(label, x + w / 2, y + h / 2, size)
  end
  local icon_w = math.min(w - 2 * pad, icon_h * 1.4)
  return box(x, y, w, h, color) ..
    icon_fn(x + (w - icon_w) / 2, y + pad, icon_w, icon_h, color) ..
    text_label(label, x + w / 2, y + h - pad - label_h / 2, size)
end

-- Context window node: title at the top, lines mimicking text below
local function context_node(label, x, y, w, h, color, size)
  local n_lines = #split(label, "|")
  local pad = 16
  local title_h = n_lines * size * 1.25
  local out = { box(x, y, w, h, color), text_label(label, x + w / 2, y + pad + title_h / 2, size) }
  local top = y + 2 * pad + title_h
  table.insert(out, string.format(
    '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#FFFFFF" stroke-width="2"/>',
    x + pad, top - pad / 2, x + w - pad, top - pad / 2))
  local widths = { 1, 0.85, 0.95, 0.6, 1, 0.9, 0.75, 1, 0.5 }
  local step = 17
  local i = 0
  while top + i * step + 6 <= y + h - pad do
    local lw = (w - 2 * pad) * widths[i % #widths + 1]
    table.insert(out, string.format(
      '<rect x="%.1f" y="%.1f" width="%.1f" height="6" rx="3" fill="#FFFFFF" fill-opacity="0.75"/>',
      x + pad, top + i * step, lw))
    i = i + 1
  end
  return table.concat(out)
end

local function node(item, x, y, w, h, color, size, kind, icon)
  local cx, cy = x + w / 2, y + h / 2
  local mime, contents
  if is_image(item) then
    local ok
    ok, mime, contents = pcall(pandoc.mediabag.fetch, item)
    if not ok or not contents then
      quarto.log.warning("ctx-diagram: could not read image " .. item)
    end
  end
  if contents then
    if mime == nil or mime == "" then mime = "image/png" end
    local pad = math.min(15, h * 0.12)
    return string.format(
      '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="22" fill="#FFFFFF" stroke="%s" stroke-width="2"/>' ..
      '<image x="%.1f" y="%.1f" width="%.1f" height="%.1f" preserveAspectRatio="xMidYMid meet" href="data:%s;base64,%s"/>',
      x, y, w, h, BORDER, x + pad, y + pad, w - 2 * pad, h - 2 * pad, mime, base64(contents))
  end
  if kind == "model" then return model_node(item, x, y, w, h, color, size, icon) end
  if kind == "context" then return context_node(item, x, y, w, h, color, size) end
  return box(x, y, w, h, color) .. text_label(item, cx, cy, size)
end

-- Vertical layout for n nodes, centered around MID_Y. Returns node height and top y's.
local function layout(n)
  local h = math.min(MAX_NODE_H, (USABLE_H - (n - 1) * GAP) / n)
  local total = n * h + (n - 1) * GAP
  local top = MID_Y - total / 2
  local ys = {}
  for i = 1, n do ys[i] = top + (i - 1) * (h + GAP) end
  return h, ys
end

-- Look up the icon for model i: a single value broadcasts to every model,
-- a matched list applies by position, and missing entries default to "nn".
local function icon_for(model_icons, i)
  if #model_icons == 1 then return model_icons[1] end
  return model_icons[i] or "nn"
end

local function render(interfaces, models, center, color, interface_color, model_color, max_h, model_icons)
  diagram_count = diagram_count + 1
  local arrow_id = "ctx-arrow-" .. diagram_count
  local parts = {}
  local function add(s) table.insert(parts, s) end
  local line = string.format('fill="none" stroke="%s" stroke-width="2.5"', color)

  -- Crop the viewBox vertically to the content (symmetric around MID_Y, so the
  -- context window stays centered) to avoid empty space above and below
  local top = CENTER.y
  for _, n in ipairs({ #interfaces, #models }) do
    if n > 0 then
      local _, ys = layout(n)
      top = math.min(top, ys[1])
    end
  end
  top = math.max(0, top - 4)

  add(string.format(
    '<svg class="ctx-diagram" viewBox="0 %.1f %d %.1f" preserveAspectRatio="xMidYMid meet" ' ..
    'style="display:block;margin:0 auto;width:100%%;height:auto;max-height:%s;font-family:inherit" ' ..
    'xmlns="http://www.w3.org/2000/svg">', top, VB_W, VB_H - 2 * top, max_h))
  add(string.format(
    '<defs><marker id="%s" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" markerHeight="5" orient="auto">' ..
    '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker></defs>', arrow_id, color))

  -- Left: interfaces -> bus -> context window
  if #interfaces > 0 then
    local h, ys = layout(#interfaces)
    for _, y in ipairs(ys) do
      add(string.format('<path d="M%d,%.1f H%d V%d" %s/>', LEFT_X + SIDE_W, y + h / 2, LEFT_BUS, MID_Y, line))
    end
    add(string.format('<path d="M%d,%d H%d" %s marker-end="url(#%s)"/>', LEFT_BUS, MID_Y, CENTER.x, line, arrow_id))
    local size = h < 90 and 20 or 26
    for i, item in ipairs(interfaces) do add(node(item, LEFT_X, ys[i], SIDE_W, h, interface_color, size)) end
  end

  -- Right: context window -> bus -> models
  if #models > 0 then
    local h, ys = layout(#models)
    add(string.format('<path d="M%d,%d H%d" %s/>', CENTER.x + CENTER.w, MID_Y, RIGHT_BUS, line))
    for _, y in ipairs(ys) do
      add(string.format('<path d="M%d,%d V%.1f H%d" %s marker-end="url(#%s)"/>',
        RIGHT_BUS, MID_Y, y + h / 2, RIGHT_X, line, arrow_id))
    end
    local size = h < 90 and 20 or 26
    for i, item in ipairs(models) do
      add(node(item, RIGHT_X, ys[i], SIDE_W, h, model_color, size, "model", icon_for(model_icons, i)))
    end
  end

  add(node(center, CENTER.x, CENTER.y, CENTER.w, CENTER.h, color, 24, "context"))
  add("</svg>")
  return table.concat(parts)
end

return {
  ["ctx-diagram"] = function(args, kwargs)
    if not quarto.doc.is_format("html:js") then
      return pandoc.Null()
    end
    local function arg(name, default)
      local v = pandoc.utils.stringify(kwargs[name] or "")
      if v == "" then return default end
      return v
    end
    -- Accepts "#RRGGBB", "RRGGBB", or PowerPoint's "AARRGGBB" (alpha first, e.g. "FF2378A0")
    local function color_arg(name, default)
      local v = arg(name, default)
      local a, rgb = v:match("^#?(%x%x)(%x%x%x%x%x%x)$")
      if a then
        if a:upper() == "FF" then return "#" .. rgb end
        return "#" .. rgb .. a
      end
      return (v:gsub("^(%x+)$", "#%1"))
    end
    local svg = render(
      split(arg("interfaces", ""), ";"),
      split(arg("models", ""), ";"),
      arg("center", "Context|Window"),
      color_arg("color", "#8A741F"),
      color_arg("interface-color", "#2378A0"),
      color_arg("model-color", "#545454"),
      arg("height", "520px"),
      split(arg("model-icons", ""), ";"))
    return pandoc.RawBlock("html", svg)
  end
}
