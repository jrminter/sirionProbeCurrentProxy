# plot-Si-voltage-series.R

rm(list=ls())
library(ggplot2)
library(grid)
library(gridExtra)

gitDir <- Sys.getenv("GIT_HOME")
str.wd <- paste0(gitDir, '/sirionProbeCurrentProxy/R/')
setwd(str.wd)

fi <-'../dat/csv/Si-10000-Traj.csv'

df <- read.csv(fi, header=TRUE, as.is=TRUE)

# add the fudge factor for 4 mm and difference in integral
df$Si.Int.mu <- 0.3208*df$Si.Int.mu
df$Si.Int.unc <- 0.3208*df$Si.Int.unc
print(head(df))


si.int.lm = lm(Si.Int.mu~e0.kV, df)
si.int.loess = loess(Si.Int.mu~e0.kV, df)

e0.kV <- seq(from=5.0, to=30.0, by=0.5)
df2 <- data.frame(e0.kV=e0.kV)
df3 <- data.frame(e0.kV=e0.kV)

df2$Si.Int.mu = round(predict(si.int.lm, newdata = df2), 2)
df3$Si.Int.mu = round(predict(si.int.loess, span=0.75, newdata = df3), 2)



siInt <- ggplot(df, aes(x=e0.kV, y=Si.Int.mu)) + 
  geom_errorbar(aes(ymin=Si.Int.mu - 1.96*Si.Int.unc,
                    ymax=Si.Int.mu + 1.96*Si.Int.unc), width=.1) +
  # geom_line(color='blue') +
  geom_point(color='black') + xlab("e0 [kV]") +
  ylab("Si-K intensity [cts/nA-sec]") +
  geom_line(color='red', size=1.25, aes(color="red"), data=df2) +
  annotate("text", label = 'lm',
           x = 25, y = 35000.,
           size = 5, colour = "red") +
  geom_line(color='blue', size=1.25, aes(color="blue"), data=df3) +
  annotate("text", label = 'LOESS',
           x = 25, y = 25000.,
           size = 5, colour = "blue") +
  ggtitle("Monte Carlo model of Si peak intensity at 4 mm WD") +
  theme(axis.text=element_text(size=12),
        axis.title=element_text(size=14),
        plot.title = element_text(hjust = 0.5))
 # +
#annotate("text", x = 0, y = 1750, label = "core") +
#annotate("text", x = 3.75, y = 1750, label = "shell")

print(siInt)


fi <- '../pdf/Si-voltage-series-plt-10000.pdf'
ggsave(siInt, file=fi, width=9.0, height=6.0, units="in", dpi=300)

fi <- '../png/Si-voltage-series-plt-10000.png'
ggsave(siInt, file=fi, width=9.0, height=6.0, units="in", dpi=300)

fi <- '../dat/csv/si-loess-pred-10000.csv'
write.csv(df3, file=fi, row.names=FALSE)
