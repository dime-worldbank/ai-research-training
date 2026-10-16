local folder = pandoc.path.directory(PANDOC_SCRIPT_FILE)
local input = os.getenv("AI_BOOTCAMP_BASELINE_DATA")
if not input or input == "" then
  local config = io.open(pandoc.path.join({folder, "baseline-path.local.txt"}), "r")
  if config then
    input = config:read("*a"):match("^%s*(.-)%s*$")
    config:close()
  end
end
if not input or input == "" then
  error("Set AI_BOOTCAMP_BASELINE_DATA or baseline-path.local.txt to the raw baseline CSV/XLSX response export. Charts will not be rendered from stale data.")
end

local stats = pandoc.json.decode(pandoc.pipe(
  os.getenv("AI_BOOTCAMP_PYTHON") or "python",
  {
    pandoc.path.join({folder, "make_baseline_chart.py"}),
    "--input", input,
    "--output-dir", pandoc.path.join({folder, "images"})
  },
  ""
))

return {{
  Str = function(element)
    if element.text:match("BASELINE_[A-Z_]+") then
      local text = element.text:gsub("BASELINE_[A-Z_]+", function(token)
        return assert(stats[token], "Unknown baseline token: " .. token)
      end)
      return pandoc.read(text).blocks[1].content
    end
  end
}}
