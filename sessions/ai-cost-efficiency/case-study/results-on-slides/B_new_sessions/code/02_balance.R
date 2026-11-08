# Balance table: baseline characteristics by treatment arm
library(dplyr)
root <- here::here()
hh <- readRDS(file.path(root, "data", "clean", "hh_panel.rds"))

balance_vars <- c("hh_size", "head_female", "head_age", "head_educ_yrs",
                  "consumption_pc", "food_insecure", "n_children_u5",
                  "livestock_tlu", "dist_market_km")

balance <- lapply(balance_vars, function(v) {
  t <- t.test(hh[[v]] ~ hh$treatment)
  data.frame(variable = v,
             control = mean(hh[[v]][hh$treatment == 0]),
             treatment = mean(hh[[v]][hh$treatment == 1]),
             p_value = t$p.value)
})
balance <- do.call(rbind, balance)
dir.create(file.path(root, "output"), showWarnings = FALSE)
write.csv(balance, file.path(root, "output", "balance_table.csv"), row.names = FALSE)
