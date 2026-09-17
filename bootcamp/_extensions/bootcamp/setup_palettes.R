# Analytics brand palette -------------------------------------------------

analytics_colors <- c(
  dark  = "#530153",
  base  = "#800280",
  light = "#B974B9",
  tint  = "#F4EAF4",
  grey  = "#6B6B6B",
  rule  = "#E2E2E2"
)

# analytics_col("base") or analytics_col("dark", "light")
analytics_col <- function(...) {
  keys <- c(...)
  if (length(keys) == 0) return(analytics_colors)
  unname(analytics_colors[keys])
}

# Ordered sequence used for categorical fills, dark -> light
analytics_seq <- unname(analytics_colors[c("dark", "base", "light")])
