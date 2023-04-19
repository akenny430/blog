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
// std::array<normal_t, 7> x_vals = {-3.0}; 

// constexpr double SQRT_HALF = std::sqrt(0.5); 
constexpr normal_t SQRT_HALF = 0.70710678118; 
/**
 * Implementing normal CDF using Erfc function 
*/
auto normalCDF_v1(normal_t x) -> normal_t
{
    return 0.5 * std::erfc(- SQRT_HALF * x); 
}

auto imp01_UsingErfc() -> void
{
    std::vector<normal_t> x_vals = get_vals(); 
    for (const auto& x : x_vals)
    {
        // std::cout << x << ": " << std::normal_distribution
        std::cout << x << ": " << normalCDF_v1(x) << '\n'; 
    }
    return; 
}

auto main() -> int 
{
    auto junk = get_vals(); 
    imp01_UsingErfc(); 
    std::cout << junk[0] << ", " << junk[1] << ", ..., " << junk.back() << '\n';  
    return 0; 
}