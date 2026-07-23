#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

#include <boost/multiprecision/cpp_int.hpp>

namespace {

using boost::multiprecision::cpp_int;
constexpr std::uint32_t n = 26;
constexpr std::uint32_t class_bits = 27;
constexpr std::uint32_t class_count = 1U << class_bits;
constexpr int fast_max_k = 13;
constexpr int big_max_k = 40;
constexpr std::int64_t separator_numerator = 779;
constexpr std::int64_t separator_denominator = 101;

static_assert(fast_max_k <= 13);

template <typename Integer>
using Vector = std::array<Integer, n>;

template <typename Integer>
Vector<Integer> multiply(std::uint32_t mask, const Vector<Integer>& input) {
    Vector<Integer> output{};
    const auto add_edge = [&](std::uint32_t u, std::uint32_t v, int sign) {
        output[u] += sign * input[v];
        output[v] += sign * input[u];
    };

    for (std::uint32_t i = 0; i + 1 < n; ++i) {
        add_edge(i, i + 1, 1);
    }
    add_edge(n - 1, 0, (mask & 1U) == 0U ? 1 : -1);
    for (std::uint32_t i = 0; i < n; ++i) {
        const int sign = ((mask >> (i + 1)) & 1U) == 0U ? 1 : -1;
        add_edge(i, (i + 2) % n, sign);
    }
    return output;
}

int fast_witness(std::uint32_t mask, std::uint32_t start) {
    Vector<std::int64_t> vector{};
    vector[start] = 1;
    for (int k = 0; k <= fast_max_k; ++k) {
        const auto image = multiply(mask, vector);
        __int128 numerator = 0;
        __int128 denominator = 0;
        for (std::uint32_t i = 0; i < n; ++i) {
            numerator += static_cast<__int128>(image[i]) * image[i];
            denominator += static_cast<__int128>(vector[i]) * vector[i];
        }
        if (static_cast<__int128>(separator_denominator) * numerator
            > static_cast<__int128>(separator_numerator) * denominator) {
            return k;
        }
        vector = multiply(mask, image);
    }
    return -1;
}

int big_witness(std::uint32_t mask, std::uint32_t start) {
    Vector<cpp_int> vector{};
    vector[start] = 1;
    for (int k = 0; k <= big_max_k; ++k) {
        const auto image = multiply(mask, vector);
        cpp_int numerator = 0;
        cpp_int denominator = 0;
        for (std::uint32_t i = 0; i < n; ++i) {
            numerator += image[i] * image[i];
            denominator += vector[i] * vector[i];
        }
        if (separator_denominator * numerator > separator_numerator * denominator) {
            return k;
        }
        vector = multiply(mask, image);
    }
    return -1;
}

int edge_sign(std::uint32_t mask, std::uint32_t bit) {
    return ((mask >> bit) & 1U) == 0U ? 1 : -1;
}

int triangle_flux(std::uint32_t mask, std::uint32_t i) {
    const int wrap = edge_sign(mask, 0);
    const int first = i == n - 1 ? wrap : 1;
    const int second = (i + 1) % n == n - 1 ? wrap : 1;
    return first * second * edge_sign(mask, i + 1);
}

bool is_twisted(std::uint32_t mask) {
    if (edge_sign(mask, 0) != -1) {
        return false;
    }
    for (std::uint32_t i = 0; i < n; ++i) {
        if (triangle_flux(mask, (i + 1) % n) != -triangle_flux(mask, i)) {
            return false;
        }
    }
    return true;
}

void print_histogram(const std::array<std::uint64_t, big_max_k + 1>& histogram) {
    std::cout << "{";
    bool first = true;
    for (int k = 0; k <= big_max_k; ++k) {
        if (histogram[k] == 0) {
            continue;
        }
        if (!first) {
            std::cout << ",";
        }
        std::cout << "\"" << k << "\":" << histogram[k];
        first = false;
    }
    std::cout << "}";
}

}  // namespace

int main() {
    std::array<std::uint64_t, big_max_k + 1> fast_histogram{};
    std::array<std::uint64_t, big_max_k + 1> big_zero_histogram{};
    std::array<std::uint64_t, big_max_k + 1> big_one_histogram{};
    std::vector<std::uint32_t> after_fast;
    std::vector<std::uint32_t> after_big_zero;
    std::vector<std::uint32_t> unresolved;

    for (std::uint32_t mask = 0; mask < class_count; ++mask) {
        const int k = fast_witness(mask, 0);
        if (k >= 0) {
            ++fast_histogram[k];
        } else {
            after_fast.push_back(mask);
        }
    }
    for (const std::uint32_t mask : after_fast) {
        const int k = big_witness(mask, 0);
        if (k >= 0) {
            ++big_zero_histogram[k];
        } else {
            after_big_zero.push_back(mask);
        }
    }
    for (const std::uint32_t mask : after_big_zero) {
        const int k = big_witness(mask, 1);
        if (k >= 0) {
            ++big_one_histogram[k];
        } else {
            unresolved.push_back(mask);
        }
    }

    bool valid = unresolved.size() == 2;
    for (const std::uint32_t mask : unresolved) {
        valid = valid && is_twisted(mask);
    }

    std::cout << "{\n";
    std::cout << "  \"n\":26,\n";
    std::cout << "  \"class_bits\":27,\n";
    std::cout << "  \"class_count\":" << class_count << ",\n";
    std::cout << "  \"separator_square\":\"779/101\",\n";
    std::cout << "  \"fast_start_0\":";
    print_histogram(fast_histogram);
    std::cout << ",\n  \"big_start_0\":";
    print_histogram(big_zero_histogram);
    std::cout << ",\n  \"big_start_1\":";
    print_histogram(big_one_histogram);
    std::cout << ",\n  \"after_fast\":" << after_fast.size() << ",\n";
    std::cout << "  \"after_big_start_0\":" << after_big_zero.size() << ",\n";
    std::cout << "  \"unresolved_masks\":[";
    for (std::size_t i = 0; i < unresolved.size(); ++i) {
        if (i != 0) {
            std::cout << ",";
        }
        std::cout << unresolved[i];
    }
    std::cout << "],\n";
    std::cout << "  \"all_unresolved_are_twisted\":" << (valid ? "true" : "false") << "\n";
    std::cout << "}\n";
    return valid ? 0 : 1;
}
