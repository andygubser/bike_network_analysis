#### PREPROCESSING OF BIKESHAREING DATA ####

# remove all objects loaded and clear memory
rm(list = ls(all.names = TRUE))
gc()


## load packages and install them when necessary ##
list.of.packages <- c("installr", "Hmisc", "ggmap", "tidyverse", "tidyr", "corrplot",
                      "viridis", "leaflet", "lubridate", "checkpoint", "zoo", "caTools",
                      "randomForest", "boot", "ggpubr")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)
for (p in list.of.packages){
  library(p, character.only = TRUE)
}

checkpoint(snapshotDate = "2099-12-29")

######################################################################

d.bike.raw = read_csv("./data/NYC-CitiBike-2016.csv")

## replace white space by underscore in column names 
d.bike.raw <- d.bike.raw %>% select_all(snakecase::to_snake_case)

## convert data
d.bike <- d.bike.raw %>%
  select(starttime, tripduration) %>%
  mutate(starttime = mdy_hms(starttime),
         date = date(starttime), # YYYY-MM-DD
         month = factor(month(starttime)),
         weekday = factor(weekdays(starttime)),
         hour = factor(hour(starttime)),
         tripduration = round(tripduration/60) #second to minute
  )

## there is no NA in the dataset
colSums(is.na(d.bike))

## This data frame shows the number of bike rentals grouped in hourly trip duration
## The values show high confidence for using the data, there is no considerable anormaly
data.frame(trip_duration_in_hour = floor(d.bike$tripduration / 60), rental_count = d.bike$rental_count) %>% 
  group_by(trip_duration_in_hour) %>% summarise(rental_count = sum(rental_count)) %>% 
  arrange(desc(trip_duration_in_hour))

## aggreate bike sharing data on hour basis, and only relevant predictos are 
## used for the analysis
d.bike <- d.bike %>% 
  group_by(date, month, weekday, hour) %>%
  summarise(tripduration=sum(tripduration), rental_count=n())
head(d.bike)

saveRDS(d.bike, file = "./data/d.bike.rds")

