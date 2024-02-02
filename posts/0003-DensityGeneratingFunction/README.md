---
math: mathjax
---

# 0003: Attempts at making a density generating function

## Introduction

Generating functions in general are useful in statistics,
particularly a random variable's moment generating function
or characteristic function.
Another kind of generating function is a
*probability generating function (PGF)*.

For a discrete random variable $X$
with non-negative support $\mathcal{D}_X \subseteq \mathbb{Z}_+$,
its PGF is given by
$$
G_X(s)
\coloneqq
\mathbb{E} \big[ s^{X} \big]
= \sum_{x \in \mathcal{D}_X} s^x f_X(x),
$$
where $f_X(x)$ is the probability mass function of $X$.
One key property (and hence the name)
is that you can generate probabilities
by taking successive derivatives:
$$
f_X(k)
= \frac{1}{k!} \frac{\mathrm{d}^k G_X}{\mathrm{d}s^k}(0).
% = \frac{1}{k!} G_X^{(k)}(0)
$$
That is, to find the probability that $X$ is equal to some $k \in \mathcal{D}_X$,
you differentiate the generating function $k$ times, evaluate it at $s = 0$,
and then divide by $k!$.
This is due to the repeated differentiation of $s^x$,
which becomes $s^{x - k}$;
the only time this is non-zero when $s=0$ is when the exponent $x - k = 0$ as well,
so $x = k$ is the only component of the sum not eliminated.
The division by $k!$ cancels out the build up when repeatedly differentiating $s^x$.

The main utility of PGFs are not to generate probabilities.
If you already have $f_X$, computing the probabilities via $G_X$
is pointless.
This is especially true if $G_X$ does not have a closed-form formula.
<!--
Add some more comments here
-->

## Generating densities

One might ask then:
is it possible to have a similar generating function for a *continuous* random variable?
Because of the continuous domain,
we would not be generating probabilities,
but probability *densities*;
It makes sense to then call this a *density generating function (DGF)*.
If $X$ is a continuous random variable with support $\mathcal{D}_X \subseteq \mathbb{R}_+$,
then its DGF is given by
$$
G_X(s)
\coloneqq
\mathbb{E} \big[ s^{X} \big]
= \int_{x \in \mathcal{D}_X} s^x f_X(x) \,\mathrm{d}x,
$$
where $f_X(x)$ is the probability density function of $X$.

<!-- We could generate densities by taking derivatives,
and also have similar properties as a PGF. -->

When generating probabilities using $G_X$, we took repeated derivatives,
and this was okay because the domain is discrete.
To do the same thing with a continuous distribution,
we will need some kind of "continuous" derivative as well.