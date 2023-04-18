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

Given its popularity, a lot of programming languages (e.g. `Python` or `R`) have an out-of-the-box implementation, which we will look at below. 
Depending on the implementation, the function is either available on its own or as a method of a class, so you would choose depending on the situation. 
Other languagues (e.g. `C++` or `Postgres`) *do not* have an implementation, so you would have to write one on your own. 
You may be able to use some other ready functionality, or have to do it completely from scratch. 

<!-- That being said, in the rest of this post we will do the following: 
- Review current implementations
- Derive a fast algorithm for computing $\Phi$ 
- Implement and compare performance (both accuracy and speed)  -->



## Current implementations 

### Python 

The `scipy` modules contains a `scipy.stats.norm` object that can compute the CDF. 
It takes in a list of values and computes the CDF like this: 

```python
x_vals: list[float] = [-3.0 + (n * 0.01) for n in range(0, 602)] # values from -3.0 to 3.0 

import numpy as np 
from scipy.stats import norm as Norm 

_: np.ndarray = Norm.cdf(x_vals)
```

Python also has an implementation via the `NormDist` class from the native `statistics` module. 
You can initialize a class and then use list comprehension to compute the values: 

```python
from statistics import NormalDist

norm: NormalDist = NormalDist(0.0, 1.0) 
_: list[float] = [norm.cdf(x_val) for x_val in x_vals] 
```

As an aside, with the setup I did, it seems that the `statistics` method works a bit faster: 

```bash
$ py implementations.py 
Testing normal distribution on 602 values stored in a list of floats ... 
Time of imp01_scipy: 630,600 ns
Time of imp02_statistics: 324,100 ns
```

But this was not a rigorous test; point is, Python has a few ways you can compute this on your own. 



## Implementing ourselves 

Now comes the fun part: we want to write an implementation of this on our own. 
For simplicity, our function will only compute $\Phi$ for a single number, without trying to do anything fancy with vectorization. 
Let's try using `C++`. 

`C++` has many built-in math functions in the `cmath` header, which we can try to utilize first. 
From the [official documentation](https://en.cppreference.com/w/cpp/header/cmath), there is an implementation of the $\mathrm{Erf}$ function that can be useful. 

