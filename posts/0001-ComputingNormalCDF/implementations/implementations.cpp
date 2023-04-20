#include <array> 
#include <cmath> 
#include <cstddef>
#include <iostream>
#include <random> 
#include <vector>

using normal_t = double; 

auto get_vals(double min = -3.0, double max = 3.0, double delta = 0.01) -> std::vector<normal_t>
{
    std::size_t _N_OBS = static_cast<std::size_t>((max - min) / delta) + 1;
    std::vector<normal_t> x_vals(_N_OBS); 
    normal_t _temp = -3.0; 
    normal_t _delta = static_cast<normal_t>(delta); 
    for(std::size_t index = 0; index < _N_OBS; ++index)
    {
        x_vals[index] = _temp; 
        _temp += _delta; 
    }
    return x_vals; 
}



// constexpr double SQRT_HALF = std::sqrt(0.5); 
constexpr normal_t SQRT_HALF = 0.70710678118; 
/**
 * Normal CDF using Erfc function 
*/
auto normalCDF_v1(normal_t x) -> normal_t
{
    return 0.5 * std::erfc(- SQRT_HALF * x); 
}

/**
 * Normal CDF using Taylor Series about 0
 * 
*/
// constexpr normal_t ONE_DIV_SQRT_TWO_PI = 1.0 / std::sqrt(2.0 * std::pi)
constexpr normal_t ONE_DIV_SQRT_TWO_PI = 0.39894228; 
auto normalCDF_v2(normal_t x, std::size_t N = 5) -> normal_t
{
    // if N < 0 we have error 
    if(N == 0){return 0.5 + (ONE_DIV_SQRT_TWO_PI * x);} 
    normal_t term = x; 
    normal_t total = x; 
    for(std::size_t k = 1; k <= N; ++k)
    {
        term *= - ((k - 0.5) * x * x) / (2.0 * k * (k + 0.5));
        total += term;  
    } 
    return 0.5 + (ONE_DIV_SQRT_TWO_PI * total); 
}

auto test_cdf() -> void
{
    std::vector<normal_t> x_vals = get_vals(); 
    for (const auto& x : x_vals)
    {
        // std::cout << x << ": " << std::normal_distribution
        std::cout << x << ": " << normalCDF_v1(x) << ", " << normalCDF_v2(x, 15) << '\n'; 
    }
    return; 
}

auto main() -> int 
{
    test_cdf(); 
    return 0; 
}