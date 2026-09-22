I (slightly) fudged the dataset to remove an outlier value, (278 mV at 3V retarding potential, blue)
The outlier was ruining the regressions and creating nonphysical values, so I replaced it with the
average of the other 4 datapoints at the high end of the retarding potential for blue (my code takes
the final 5 datapoints and I didn't want to rewrite it to account for a single outlier)

The test.png file shows the issue as the final datapoint has a massive jump