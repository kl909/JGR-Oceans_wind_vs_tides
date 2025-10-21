# Load necessary libraries
library(tidyr)
library(dplyr)
library(ggplot2)
library(ggpubr)

setwd("~/Documents/chapter_1/diagonal_analysis/cairns")

data <- read.csv("particle_diagonals_cairns.csv")

# remove first column
data <- data[, -1]
names(data)[1] <- "Tides"
names(data)[2] <- "Wind"
names(data)[3] <- "Wind & Tides"

# convert zeros to na
#data[data == -Inf] <- 0

# convert wide data to long
data_long <- data %>%
  pivot_longer(cols = everything(), names_to = "simulation", values_to = "value")

#data_long$value = data_long$value+1

#data_long$value = log10(data_long$value)

# Perform ANOVA
anova_result <- aov(value ~ simulation, data_long)

# Print the summary of ANOVA
summary(anova_result)

#posthoc Turkey
posthoc <- TukeyHSD(x=anova_result, conf.level=0.95)
posthoc<-as.data.frame(posthoc[1])
write.csv(posthoc, 'particle_posthoc_tukey_cairns.csv')
posthoc

# plot box and whisker graph
ggplot(data_long, aes(x = resolution, y = value)) +
  geom_boxplot() +
  labs(title = "Box-and-Whisker Plot",
       x = "Variable",
       y = "Value") +
  theme_minimal()

#ggpubr box and whisker plot
#ggboxplot(data_long, x = "resolution", y = "value",
#               color = "resolution", palette =c("#101E6A","#785ECE","#3FD2D6","#ea7070"),
#               add = "jitter", #shape = "resolution",
#               xlab = expression(Number ~ of ~ particles ~ per ~ km^2),
#               ylab = 'Self Connectivity')

ggplot(data_long, aes(x = simulation, y = value, color = simulation)) +
  geom_boxplot() +
  geom_jitter(width = 0.2) +  # Adds jittered points
  scale_color_manual(values = c("#101E6A", "#785ECE", "#3FD2D6", "#ea7070")) +
  labs(
    x = expression(Simulation),  # Superscript 2 in the label
    y = "Self Connectivity",
    #title = "Boxplot of Self Connectivity by Particle Number"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(size = 10, colour = "black"),  # Adjust x-axis text size
    axis.text.y = element_text(size = 10, colour = "black"),  # Adjust y-axis text size
    axis.title.x = element_text(size = 14, margin = margin(t=10)),  # Adjust x-axis label size
    axis.title.y = element_text(size = 14, margin = margin(r=10)),  # Adjust y-axis label size
    #plot.title = element_text(size = 18, face = "bold"),  # Adjust plot title size
  )

#scale_color_manual(values = c("#625E85", "#217154","#5A9CBB", "#9B88DB","#46eaee","#ea7070", "#e59572")
                   
#scale_color_manual(values = c("#9B88DB","#46eaee","#ea7070"
                   

