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
```math
G_X(s)
\coloneqq
\mathbb{E} \big[ s^{X} \big]
= \sum_{x \in \mathcal{D}_X} s^x f_X(x),
```
where $f_X(x)$ is the probability mass function of $X$.
One key property (and hence the name)
is that you can generate probabilities
by taking successive derivatives:
```math
f_X(k)
= \frac{1}{k!} \frac{\mathrm{d}^k G_X}{\mathrm{d}s^k}(0).
% = \frac{1}{k!} G_X^{(k)}(0)
```
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
```math
G_X(s)
\coloneqq
\mathbb{E} \big[ s^{X} \big]
= \int_{x \in \mathcal{D}_X} s^x f_X(x) \,\mathrm{d}x,
```
where $f_X(x)$ is the probability density function of $X$.

<!-- We could generate densities by taking derivatives,
and also have similar properties as a PGF. -->

When generating probabilities using $G_X$, we took repeated derivatives,
and this was okay because the domain is discrete.
To do the same thing with a continuous distribution,
we will need some kind of "continuous" derivative as well.

## Fractional derivatives

For some function $f(s)$, we want to generalize the $k$th derivative
$\mathrm{d}^kf / \mathrm{d}s^k$ from $k \in \mathbb{N}$
to $k \in \mathbb{R}_+$.
Let's consider the function $f(s) = s^x$;
differentiating $k$ times gives us
```math
\frac{\mathrm{d}^k}{\mathrm{d}s^k} s^x
= \frac{x!}{(x - k)!} s^{x - k}.
```
A natural extension is to replace the factorial with the Gamma function:
```math
% \frac{\mathrm{d}^k}{\mathrm{d}s^k} s^x
\mathrm{D}^k s^x
= \frac{\Gamma(x + 1)}{\Gamma(x + 1 - k)} s^{x - k},
```
where $\mathrm{D}^k$ is the *continuous differential operator*.
With more rigorous treatment, one can show this is indeed a valid generalization.
For any function $f(s)$, we can construct
```math
\mathrm{D}^k
= \frac{1}{\Gamma(\lceil k \rceil - k)}
\cdot \frac{\mathrm{d}^{\lceil k \rceil}}{\mathrm{d}s^{\lceil k \rceil}}
\int_{\alpha}^s (s - t)^{\lceil k \rceil - k - 1} f(t) \,\mathrm{d}t,
```
although for the DGF we only need to differentiate $f(s) = s^x$.

## Back to generating densities

Applying $\mathrm{D}^k$ to the DGF gives
```math
\mathrm{D}^k \, G_X(s)
= \mathrm{D}^k \int_{x \in \mathcal{D}_X} s^x f_X(x) \,\mathrm{d}x
= \int_{x \in \mathcal{D}_X} \mathrm{D}^k \, s^x \cdot f_X(x) \,\mathrm{d}x
= \int_{x \in \mathcal{D}_X} \frac{\Gamma(x + 1)}{\Gamma(x + 1 - k)} s^{x - k} \cdot f_X(x) \,\mathrm{d}x.
```
Just as with the PGF, plugging in $s=0$ gives
```math
\mathrm{D}^k \, G_X(0)
= \int_{x \in \mathcal{D}_X} \frac{\Gamma(x + 1)}{\Gamma(x + 1 - k)} \cdot 0^{x - k} \cdot f_X(x) \,\mathrm{d}x
= \frac{\Gamma(k + 1)}{\Gamma(k + 1 - k)} f_X(k)
= \Gamma(k + 1) \cdot f_X(k),
```
from which we get
```math
f_X(k)
% = \frac{\mathrm{D}^k \, G_X(0)}{\Gamma(k + 1)}
= \frac{1}{\Gamma(k + 1)} \cdot \mathrm{D}^k \, G_X(0).
```
This is indeed a generalization from the PGF;
if $k \in \mathbb{N}$, then $\Gamma(k + 1) = k!$.