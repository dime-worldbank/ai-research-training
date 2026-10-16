#' Complete list of palettes
#'
#' Use \code{\link{decdi_palette}} to construct palettes of desired length.
#' Colors synchronized from the skill's branding/colors.yml.
#'
#' @export
decdi_palettes <- list(
  "DECDI" = c("Navy" = "#002A4F",
              "BlueDark" = "#1C618C",
              "BlueMid" = "#2599CD",
              "BlueLight" = "#2AACE2",
              "Cyan" = "#01ADEF"),
  # Categorical: one base color per Impact Lab / program.
  "SubLabs" = c("People" = "#991D38",
                "Prosperity" = "#FFC20D",
                "Infrastructure" = "#047D70",
                "eMBeD" = "#F78D28",
                "Analytics" = "#800280"),
  # Sequential 3-step ramps per lab, for when a chart needs shades of a
  # single lab's color rather than a categorical comparison across labs.
  # Only the "Base" value is a brand-guide color; "Dark"/"Light" are derived
  # tints/shades (see the skill's branding/colors.yml) -- not brand-guide-verified.
  "People" = c("Dark" = "#631324", "Base" = "#991D38", "Light" = "#C78392"),
  "Prosperity" = c("Dark" = "#A67E08", "Base" = "#FFC20D", "Light" = "#FFDD7A"),
  "Infrastructure" = c("Dark" = "#035149", "Base" = "#047D70", "Light" = "#75B8B0"),
  "eMBeD" = c("Dark" = "#A15C1A", "Base" = "#F78D28", "Light" = "#FBC089"),
  "Analytics" = c("Dark" = "#530153", "Base" = "#800280", "Light" = "#B974B9")
)

#' A DECDI palette generator
#'
#' Color palettes for DECDI presentations. Use the "DECDI" palette (navy to
#' cyan) as the default sequential/branding palette; use "SubLabs" for
#' categorical charts comparing Impact Labs/programs; use the per-lab name
#' (e.g. "People", "Analytics") for a sequential ramp within one lab's color.
#'
#' @param name Name of desired palette: \code{DECDI}, \code{SubLabs}, or a
#'   lab name (\code{People}, \code{Prosperity}, \code{Infrastructure},
#'   \code{eMBeD}, \code{Analytics}).
#' @param n Number of colors desired. If omitted, uses all colours.
#' @param type Either "discrete" or "continuous". Use continuous to
#'   interpolate between colors.
#' @export
#' @keywords colors
#' @examples
#' decdi_palette("DECDI")
#' decdi_palette("SubLabs")
#' pal <- decdi_palette(name = "DECDI", n = 21, type = "continuous")
decdi_palette <- function(name, n, type = c("discrete", "continuous")) {
  type <- match.arg(type)
  pal <- decdi_palettes[[name]]
  if (is.null(pal))
    stop("Palette not found.")
  if (missing(n)) {
    n <- length(pal)
  }
  if (type == "discrete" && n > length(pal)) {
    stop("Number of requested colors greater than what palette can offer")
  }
  out <- switch(type,
                continuous = grDevices::colorRampPalette(pal)(n),
                discrete = pal[1:n]
  )
  structure(out, class = "palette", name = name)
}

#' @export
#' @importFrom graphics rect par image text
#' @importFrom grDevices rgb
print.palette <- function(x, ...) {
  n <- length(x)
  old <- par(mar = c(0.5, 0.5, 0.5, 0.5))
  on.exit(par(old))
  image(1:n, 1, as.matrix(1:n), col = x,
        ylab = "", xaxt = "n", yaxt = "n", bty = "n")
  rect(0, 0.9, n + 1, 1.1, col = rgb(1, 1, 1, 0.8), border = NA)
  text((n + 1) / 2, 1, labels = attr(x, "name"), cex = 1, family = "serif")
}
