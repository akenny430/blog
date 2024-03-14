# 0004: Determining if an "approximate" correlation matrix is PSD

## Introduction

For a set of $p$ random variables $X_1, \ldots, X_p = \mathbf{x} \in \mathbb{R}^p$
(assume that $\mathbb{E}[\mathbf{x}] = \mathbf{0}$),
it is useful to examine its *covariance matrix*
$$
\mathbf{C}
= \mathbb{V}\mathrm{ar}[\mathbf{x}]
= \mathbb{E}[\mathbf{x} \mathbf{x}^\top].
$$
If you have $n$ observations of $\mathbf{x}$
stored in the matrix $\mathbf{X} \in \mathbb{R}^{n \times p}$,
we can look at the *sample covariance matrix*
$$
\mathbf{C}
= \frac{1}{n - 1} \mathbf{X}^\top \mathbf{X}.
$$
By design, this matrix will be positive semi-definite (PSD);
i.e., $\mathbf{w}^\top \mathbf{C} \mathbf{w} \ge 0$
for all non-zero vectors $\mathbf{w} \in \mathbb{R}^p$.
<!--
TODO: add links to proofs of these
https://statproofbook.github.io/P/covmat-psd.html
-->

As an example from finance,
suppose you have a portfolio containing $p$ assets.
If $X_i$ is the change/shock of asset $i$
and $w_i$ is portfolio's dollar position of asset $i$
(for some horizon, e.g., 1 day),
then the change in portfolio value over this horizion is
$$
\sum_{i = 1}^p w_i X_i
= \mathbf{w}^\top \mathbf{x}.
$$
We can then measure the variance of this change as
$$
\mathbb{V}\mathrm{ar}[\mathbf{w}^\top \mathbf{x}]
= \mathbf{w}^\top \mathbb{V}\mathrm{ar}[\mathbf{x}] \mathbf{w}
= \mathbf{w}^\top \mathbf{C} \mathbf{w}.
$$

An alternative way of looking at these computations is the *correlation matrix*,
$\mathbf{R}$.
Suppose for variable $i$ we have the standard deviation $s_i$,
which we can store in a vector $\mathbf{s} \in \mathbb{R}^p$.
If we define the diagonal matrix $\mathbf{S} = \mathrm{diag}(\mathbf{s})$,
we can relate the covariance and correlation matrices with
$$
\begin{align*}
    \mathbf{C} &= \mathbf{S}^\top \mathbf{R} \mathbf{S}, \\
    \mathbf{R} &= \mathbf{S}^{-\top} \mathbf{C} \mathbf{S}^{-1}. \\
\end{align*}
$$
Our quadratic form can then be written as
$$
\mathbf{w}^\top \mathbf{C} \mathbf{w}
= \mathbf{w}^\top (\mathbf{S}^\top \mathbf{R} \mathbf{S}) \mathbf{w}
= (\mathbf{S} \mathbf{w})^\top \mathbf{R} (\mathbf{S} \mathbf{w})
= \tilde{\mathbf{w}}^\top \mathbf{R} \tilde{\mathbf{w}}.
$$

Given that $\mathbf{C}$ is PSD,
it follows that $\mathbf{R}$ is PSD as well.
<!--
TODO: add proof of this
-->

However, suppose for whatever reason,
you are not able to empirically determine the covariance/correlation
between every variable.
Thinking back to the finance example,
you could have a new instrument in your portfolio
without enough historical data to compute the correlations with other assets
(and despite this, you still decide to include it in your portfolio :P).
In this case, you could *approximate* the correlation with another value.
In an extreme case, you might make the (very rigid) assumption that
the correlation between every element is the same.

We can look at this *approximation correlation matrix* $\mathbf{Q}$,
whose elements are given by
$$
q_{i,j}
=
\begin{cases}
    1& i = j, \\
    \rho& i \neq j.
\end{cases}
$$
That is, every element still has correlation $1$ with itself,
but you assume it has correlation $\rho$ with every other element.
Our variance would then be approximated by
$$
\mathbb{V}\mathrm{ar}[\mathbf{w}^\top \mathbf{x}]
= \tilde{\mathbf{w}}^\top \mathbf{R} \tilde{\mathbf{w}}
\approx \tilde{\mathbf{w}}^\top \mathbf{Q} \tilde{\mathbf{w}}.
% = \sum_{i = 1}^p \tilde{w}_i^2 + \rho \sum_{i = 1}^p \sum_{j = 1}^p \tilde{w}_i \tilde{w}_j
$$
<!--
TODO: figure out how to put i \neq j in subscript
-->

While the full correlation matrix $\mathbf{R}$ is PSD,
it may not be true that the approximate matrix $\mathbf{Q}$ is.
That brings us to the purpose of this post:
*when is the matrix $\mathbf{Q}$ PSD?*
<!-- we have its correlation *correlation* matrix $\mathbf{R}$
(not a covariance matrix);
element $(i, j)$, $\rho_{i, j}$,
is the correlation between $X_i$ and $X_j$. -->
<!-- $$
\rho_{i,j}
=
\begin{cases}
    1& i = j \\

\end{cases}
$$ -->