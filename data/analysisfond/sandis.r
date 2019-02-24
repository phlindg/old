


datapath <- "C:/Users/Phili/Desktop/fond/data"

eric <- read.csv("C:/Users/Phili/Desktop/fond/data/ERIC.csv", sep=";")
sand <- read.csv("C:/Users/Phili/Desktop/fond/data/SAND.csv", sep=";")

eric$Date <- as.Date(eric$Date)
sand$Date <- as.Date(sand$Date)

date <- as.Date("2010-01-01")
date_slut <- as.Date("2018-01-01")

eric <- subset(eric, Date > date & Date < date_slut )
sand <- subset(sand, Date > date & Date < date_slut)

eric.close <- eric$Closing.price
sand.close <- sand$Closing.price


v0 <- 100
c <- seq(0.1,1,0.2)
c <- 0.5

rets <- cbind(eric.close, sand.close)
ettor <- rep(1, ncol(rets))

sig <- solve(matrix(c(0.0625, 0.015, 0.015, 0.09), nrow=2, ncol = 2))
mu = c(1.1, 1.15)
a <- sig %*% ettor
b <- ettor %*% a 
w <- v0 * a/c(b)
sqrt(t(w) %*% solve(sig) %*% w)
