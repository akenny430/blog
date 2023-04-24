#include <array> 
#include <cmath> 
#include <cstddef>
#include <fstream>
#include <iostream>
#include <random> 
#include <vector>

using normal_t = double; 

auto get_vals(double min = -4.0, double max = 4.0, double delta = 0.01) -> std::vector<normal_t>
{
    std::size_t _N_OBS = static_cast<std::size_t>((max - min) / delta) + 1;
    std::vector<normal_t> x_vals(_N_OBS); 
    normal_t _temp = min; 
    normal_t _delta = static_cast<normal_t>(delta); 
    for(std::size_t index = 0; index < _N_OBS; ++index)
    {
        x_vals[index] = _temp; 
        _temp += _delta; 
    }
    return x_vals; 
}



/**
 * Normal CDF using Erfc function 
*/
constexpr normal_t SQRT_HALF = 0.70710678118; 
auto phi_ERFC(normal_t x) -> normal_t
{
    return 0.5 * std::erfc(- SQRT_HALF * x); 
}

/**
 * Normal CDF using Taylor Series about 0
 * 
*/
constexpr normal_t ONE_DIV_SQRT_TWO_PI = 0.39894228; 
auto phi_TS(normal_t x, std::size_t N = 5) -> normal_t
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

/**
 * Normal CDF using *dynamic* Taylor series about 0 
*/
auto n_fitted(normal_t x) -> std::size_t
{
    normal_t z = std::abs(x); 
    normal_t quadratic = 0.68936564 + z * ( 2.50832137 + z * 0.93954765 ); 
    return static_cast<std::size_t>(quadratic); 
}

auto phi_DTS(normal_t x) -> normal_t
{
    if (x >= 4.0) {return 1.0;}
    if (x <= -4.0) {return 0.0;}
    std::size_t N = n_fitted(x); 
    return phi_TS(x, N); 
}



auto write1_TaylorSeries() -> void 
{
    std::ofstream res_file; 

    res_file.open("../results/taylor_series.csv");
    res_file << "x,Erfc,TS05,TS10,TS15,TS20,TS30\n"; 
    for (const normal_t& x : get_vals() )
    {
        res_file 
        << x << ',' 
        << phi_ERFC(x) << ','  
        << phi_TS(x, 5) << ','  
        << phi_TS(x, 10) << ','  
        << phi_TS(x, 15) << ','  
        << phi_TS(x, 20) << ','  
        << phi_TS(x, 30) << ','  
        << '\n'; 
    } 
    res_file.close(); 
}

auto write2_DynamicTS() -> void
{
    std::ofstream res_file; 
    res_file.open("../results/taylor_series_dynamic.csv");

    // columns 
    res_file << "x" << ','; 
    for (int N = 0; N <= 30; ++N)
    { res_file << 'N' << N << ','; }
    res_file << '\n'; 

    // data 
    for (const normal_t& x : get_vals(-4.0, 4.0, 0.001) )
    {
        res_file << x << ','; 
        for (int N = 0; N <= 30; ++N)
        { res_file << phi_TS(x, N) << ','; }
        res_file << '\n'; 
    }

    res_file.close(); 
}

auto write3_FinalComp() -> void
{
    std::ofstream res_file; 
    res_file.open("../results/taylor_series_final.csv");
    res_file << "x,Erfc,TS30,DTS (Fitted)\n"; 
    for (const normal_t& x : get_vals() )
    {
        res_file 
        << x << ',' 
        << phi_ERFC(x) << ','  
        << phi_TS(x, 30) << ','  
        << phi_DTS(x) << ','  
        << '\n'; 
    } 
    res_file.close(); 
}



auto main() -> int 
{
    // write1_TaylorSeries(); 
    // write2_DynamicTS(); 
    write3_FinalComp(); 

    return 0; 
}