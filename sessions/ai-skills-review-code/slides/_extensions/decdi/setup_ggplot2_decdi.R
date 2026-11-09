# A theme for {ggplot2} graphs matching the DECDI presentation theme.
theme_decdi <- function(base_family = "Lato",
                         base_size = 11.5,
                         plot_title_family = "Montserrat",
                         plot_title_size = 18,
                         plot_title_face = "bold",
                         plot_title_margin = 10,
                         subtitle_family = base_family,
                         subtitle_size = 12,
                         subtitle_face = "plain",
                         subtitle_margin = 15,
                         caption_family = base_family,
                         caption_size = 9,
                         caption_face = "italic",
                         caption_margin = 10,
                         axis_text_size = base_size,
                         axis_title_size = 9,
                         grid_col = "#cccccc",
                         grid = TRUE) {
  ret <- ggplot2::theme_minimal(base_family = base_family, base_size = base_size)

  ret <- ret + ggplot2::theme(
    legend.background = ggplot2::element_blank(),
    legend.key = ggplot2::element_blank(),
    panel.grid = ggplot2::element_line(color = grid_col, linewidth = 0.2),
    axis.ticks = ggplot2::element_blank(),
    axis.text.x = ggplot2::element_text(size = axis_text_size),
    axis.text.y = ggplot2::element_text(size = axis_text_size),
    axis.title = ggplot2::element_text(size = axis_title_size),
    plot.title = ggplot2::element_text(
      hjust = 0, size = plot_title_size, family = plot_title_family,
      face = plot_title_face, margin = ggplot2::margin(b = plot_title_margin)
    ),
    plot.subtitle = ggplot2::element_text(
      hjust = 0, size = subtitle_size, family = subtitle_family,
      face = subtitle_face, margin = ggplot2::margin(b = subtitle_margin)
    ),
    plot.caption = ggplot2::element_text(
      hjust = 1, size = caption_size, family = caption_family,
      face = caption_face, margin = ggplot2::margin(t = caption_margin)
    ),
    plot.margin = ggplot2::margin(30, 30, 30, 30)
  )

  if (!grid) {
    ret <- ret + ggplot2::theme(panel.grid = ggplot2::element_blank())
  }

  ret
}

ggplot2::theme_set(theme_decdi())

# Use the DECDI palette as the default discrete/continuous scale.
options(
  ggplot2.discrete.colour = function(...) ggplot2::scale_colour_manual(..., values = decdi_palette("DECDI")),
  ggplot2.discrete.fill = function(...) ggplot2::scale_fill_manual(..., values = decdi_palette("DECDI")),
  ggplot2.continuous.colour = function(...) ggplot2::scale_colour_gradientn(..., colours = decdi_palette("DECDI")),
  ggplot2.continuous.fill = function(...) ggplot2::scale_fill_gradientn(..., colours = decdi_palette("DECDI"))
)
