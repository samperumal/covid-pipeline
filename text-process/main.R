dt <- read.table("/var/data/sacorona/images/combined.tsv",
  header = FALSE,
  sep = "\t"
)

dt[, "date"] <- as.Date(dt[, "V5"], "%d %B %Y")

ds <- as.data.frame(dt[, c("province" = "V1", "V2", "date")])

dd <- ds[order(ds["V1"], ds["date"], dt["V2"]), ]

dd <- dd[dd$V1 %in% c(
  "North West",
  "Northern Cape",
  "Western Cape",
  "Eastern Cape",
  "Free State",
  "Gauteng",
  "KwaZulu-Natal",
  "Limpopo",
  "Mpumalanga",
  "North West"
), ]

colnames(dd) <- c("province", "total", "date")

dd[, "diff"] <- 0
dd[, "diff2"] <- 0

trow <- 1
for (srow in 2:nrow(dd)) {
  if (dd[srow, "province"] == dd[srow - 1, "province"]) {
    dd[srow, "diff"] <- dd[srow, "total"] - dd[srow - 1, "total"]
    dd[srow, "diff2"] <- dd[srow, "diff"] - dd[srow - 1, "diff"]
    trow <- trow + 1
  }
}

rownames(dd) = NULL

write.csv(file = "/var/data/sacorona/images/analysis.csv", x = dd, row.names = FALSE)

require("ggplot2")

for (p in c(
  "North West",
  "Northern Cape",
  "Western Cape",
  "Eastern Cape",
  "Free State",
  "Gauteng",
  "KwaZulu-Natal",
  "Limpopo",
  "Mpumalanga",
  "North West"
)) {

p1 <- ggplot(data = dd[dd["province"] == p, ], aes(x = date, y = total, color = province)) +
      geom_point(stat = "identity") +
      labs(title = paste("Coronavirus cases in ", p),
           subtitle = "2nd Wave",
           x = "Date", y = "Total cases")

ggsave(paste("/var/data/sacorona/images/", p, ".png", sep =""), plot = p1)
}
