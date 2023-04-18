#include <array> 
#include <cmath> 
#include <iostream>
#include <random> 

using normal_t = long double; 
std::array<normal_t, 7> x_vals = {-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0}; 

// constexpr double SQRT_HALF = std::sqrt(0.5); 
constexpr normal_t SQRT_HALF = 0.70710678118; 
auto normalCDF(normal_t x) -> normal_t
{
    return 0.5 * std::erfc(- SQRT_HALF * x); 
}

auto imp01_UsingErfc() -> void
{
    for (auto x : x_vals)
    {
        // std::cout << x << ": " << std::normal_distribution
        std::cout << x << ": " << normalCDF(x) << '\n'; 
    }
    return; 
}

auto main() -> int 
{
    imp01_UsingErfc(); 
    return 0; 
}