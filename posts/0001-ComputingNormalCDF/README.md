# 0001: Fast and correct computation of the standard normal CDF 



## Introduction 

One of the most fundamental computations in all of probability and statistics is 
computing the CDF of a normal distribution. 
For a normal random variable $X$ with mean $\mu$ and standard deviation $\sigma$, i.e. $X \sim \mathrm{N}(\mu, \sigma)$, 
the normal CDF is given by 
<!-- $$ \Phi(x; \mu, \sigma) = \frac{1}{\sigma \sqrt{2 \pi}} \int_{-\infty}^{x} \mathrm{exp} \left( - \frac{(t - \mu)^2}{2 \sigma^2} \right) \,\mathrm{d}t. $$ -->
```math
\Phi(x; \mu, \sigma) = \frac{1}{\sigma \sqrt{2 \pi}} \int_{-\infty}^{x} \mathrm{exp} \left( - \frac{(t - \mu)^2}{2 \sigma^2} \right) \,\mathrm{d}t.
```
This integral generally has no closed-form solution, 
so we have to compute $\Phi$ using some numerical scheme. 

As a reminder, for any r.v. $X \sim \mathrm{N}(\mu, \sigma)$, 
by *standardizing* we have $(X - \mu) / \sigma = Z$, 
where $Z \sim \mathrm{N}(0, 1)$ is the standard normal distribution. 
In this case, $\Phi$ is given by 
```math
\Phi(x) = \frac{1}{\sqrt{2 \pi}} \int_{-\infty}^{x} \mathrm{exp} \left( - \frac{t^2}{2} \right) \,\mathrm{d}t.
``` 
This will be "the" $\Phi$ that we will implement, and we can just standardize the inputs to use it no matter what $\mu$ and $\sigma$ are. 

Given its popularity, most programming languages have some efficient implementation of $\Phi$, e.g. `Python` or `C++`, 
but not all! 
The reason for writing about this topic is that `SQL` (specifically `PostgreSQL`) does **not** have its own implementation of $\Phi$. 
If any queries involve computing $\Phi$ arise, you will need your own implementation. 

That being said, in the rest of this post we will do the following: 
- Review current implementations
- Derive a fast algorithm for computing $\Phi$ 
- Implement and compare performance (both accuracy and speed) 



## Current implementations 

### Python 

There are two good `Python` implementations I was able to find. 

First, 

```python
from statistics import NormalDist 

x_vals: list[float] = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
cdf_vals = [NormalDist().cdf(x_val) for x_val in x_vals] 

"""
Using NormalDist from statistics: 
 -3.0: 0.0013499
 -2.0: 0.0227501
 -1.0: 0.1586553
  0.0: 0.5000000
  1.0: 0.8413447
  2.0: 0.9772499
  3.0: 0.9986501
"""
```

The `scipy.stats` module has a `norm` class that contains a `cdf` method. 

```python
from scipy.stats import norm # has cdf 

x_vals: list[float] = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
cdf_vals = norm.cdf(x_vals)

"""
Using norm from scipy.stats: 
 -3.0: 0.0013499
 -2.0: 0.0227501
 -1.0: 0.1586553
  0.0: 0.5000000
  1.0: 0.8413447
  2.0: 0.9772499
  3.0: 0.9986501
"""
```