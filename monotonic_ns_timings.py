# this is an approximation of joint distribution of times `time.monotonic_ns` call takes.
# Method of computation:
# 0. create an accumulator array. index is time, value by the index is frequency
# 1. call `time.monotonic_ns` multiple times
# 2. compute deltas
# 3. it turns out (after the experiment with averaging one call) the distribution is multimodal, a mixture of multiple distributions.  So check if all the deltas belong to the same subdistribution by comparing them to local mimima of PDFs, separating the unimodal subdistributions. If the values belong to different distributions, do nothing, try again.
# 4. use arythm average of the deltas as the key: the last time minus the first time, divided by count of deltas. Use only odd number of deltas to avoid rounding errors.
# 5. when we increase count of consecutive evaluations of `time.monotonic_ns`, the resulting distribution tends to shift into the area of lower times. It seems the overhead becomes lower. Since Python version used was not JITted ... IDK origin of this.

import numpy
import scipy.stats

d1 = scipy.stats.norm(loc=100.88800333333336, scale=1.186251833851963)
d2 = scipy.stats.norm(loc=129.43312242240475, scale=2.4933842584502934)
d3 = scipy.stats.norm(loc=142.0452, scale=4.552126641472099)
weights = np.array((0.2761394101876676, 0.4557640750670241, 0.2680965147453083))
def jointPDF(x):
	return d1.pdf(x) * weights[0] + d2.pdf(x) * weights[1] + d3.pdf(x) * weights[2]

