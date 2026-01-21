library(tidyverse)
library(readxl)
library(wordcloud2)
library(htmlwidgets)

# base directory (project root)
BASE_DIR <- dirname(getwd())

# paths
KEYWORDS_PATH <- file.path(BASE_DIR, "keywords", "keywords.csv")
OUTPUT_DIR <- file.path(BASE_DIR, "visualizations")

dir.create(OUTPUT_DIR, showWarnings = FALSE)

# read keywords csv
data <- read_csv(KEYWORDS_PATH, col_names = c("keyword", "frequency"))

# ==================
# Bar chart (top 20)
# ==================
top_keywords <- data %>%
  arrange(desc(frequency)) %>%
  slice_head(n = 20)

bar_chart <- ggplot(top_keywords, aes(x = reorder(keyword, frequency), y = frequency)) +
  geom_col(fill = "#2C3E50") +
  coord_flip() +
  labs(
    title = "Top 20 Keywords in Job Descriptions",
    x = "Keyword",
    y = "Frequency"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(face = "bold", size = 18, hjust = 0.5),
    axis.text.y = element_text(size = 12),
    axis.text.x = element_text(size = 12)
  )

ggsave(
  filename = file.path(OUTPUT_DIR, "bar_chart.png"),
  plot = bar_chart,
  width = 8,
  height = 6,
  dpi = 300
)

# ==================
# Word cloud
# ==================
wc <- wordcloud2(
  data,
  size = 0.8,
  color = "random-dark",
  backgroundColor = "white"
)

saveWidget(
  wc,
  file = file.path(OUTPUT_DIR, "wordcloud.html"),
  selfcontained = TRUE
)

# optional static export
# webshot2::webshot(
#   file.path(OUTPUT_DIR, "wordcloud.html"),
#   file.path(OUTPUT_DIR, "wordcloud.png"),
#   vwidth = 800,
#   vheight = 600
# )
