# Healthcare-Project
This is my response to the "U.S. Medical Insurance Costs" problem.

It's a fairly simple exercise that gives quite a bit of scope for playing around with the data.

My first approach was to identify the formula for how the cost is generated off the metrics. Much to my (dis?)pleasure I found that though some people have the same metrics and the same insurance costs, others have the same metrics and different costs. Further investigation shows that changes in metrics were not correlated with consistent changes in cost. This suggest several plausible possibilities about the meta-data set:

1) The data is corrupt.
2) There are other variables that aren't shown to the analyst.
3) There is an inherent bias that can't be explained by the metrics given.

Number (3) is the most interesting working within the frame of the dataset itself. Regardless, there was no possible way to create a formula for this dataset.

After that, I did some general analysis focussing on what the "average" person was in the dataset (male, over 30, at least one kid, non smoker...) and explored some aspects to the metrics that could potentially impact the cost (like smokers, who pay on average 3.8 times as much as non-smokers), or more controversial ones like location (southeners can expect to pay as much as much as 18% more on average than northeners. Is the southern weather more dangerous? Or is there a 'Global South' type bias at play here?).

I concluded by creating a class to define new people that might be added to the database, and gave them recommendations on how much they might expect to pay based on how they stack up against the average on a metric-by-metric level.
