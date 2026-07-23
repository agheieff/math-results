#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {
constexpr int k = 5;
constexpr int limit = 11;
constexpr int power_four = 81;
constexpr std::array<std::array<int, 2>, 7> columns{{
    {0, 0}, {0, 1}, {1, 0}, {1, 1}, {1, 2}, {2, 1}, {2, 2},
}};

struct Metrics {
    std::size_t count;
    std::uint64_t xor_fingerprint;
    std::uint64_t sum_fingerprint;
};

bool compatible(int left, int right) {
    return !((left == 0 && right == 2) || (left == 2 && right == 0));
}

std::uint32_t pack(int u0, int first, int last, int queue, int b_count, int y_count) {
    return static_cast<std::uint32_t>(
        u0 | (first << 2) | (last << 10) | (queue << 12) | (b_count << 20) |
        (y_count << 24)
    );
}

void unpack(
    std::uint32_t value,
    int& u0,
    int& first,
    int& last,
    int& queue,
    int& b_count,
    int& y_count
) {
    u0 = value & 3;
    first = (value >> 2) & 255;
    last = (value >> 10) & 3;
    queue = (value >> 12) & 255;
    b_count = (value >> 20) & 15;
    y_count = (value >> 24) & 63;
}

std::array<int, k> trits(int code) {
    std::array<int, k> result{};
    for (int index = k - 1; index >= 0; --index) {
        result[index] = code % 3;
        code /= 3;
    }
    return result;
}

std::uint64_t splitmix64(std::uint64_t value) {
    value += 0x9e3779b97f4a7c15ULL;
    value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
    value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
    return value ^ (value >> 31);
}

Metrics metrics(const std::unordered_set<std::uint32_t>& states) {
    std::uint64_t xor_fingerprint = 0;
    std::uint64_t sum_fingerprint = 0;
    for (const std::uint32_t state : states) {
        const std::uint64_t fingerprint = splitmix64(state);
        xor_fingerprint ^= fingerprint;
        sum_fingerprint += fingerprint;
    }
    return {states.size(), xor_fingerprint, sum_fingerprint};
}

void initialize(
    int position,
    int u0,
    int last,
    int first,
    int queue,
    int b_count,
    int y_count,
    std::unordered_set<std::uint32_t>& states
) {
    if (position == k) {
        states.insert(pack(u0, first, last, queue, b_count, y_count));
        return;
    }
    for (const auto& column : columns) {
        const int outer = column[0];
        const int inner = column[1];
        if (position == 0 && outer != 1 && inner != 1) {
            continue;
        }
        if (position > 0 && !compatible(last, outer)) {
            continue;
        }
        const int next_b = b_count + (outer == 1) + (inner == 1);
        const int next_y = y_count + (outer == 2) + (inner == 2);
        if (next_b > limit) {
            continue;
        }
        initialize(
            position + 1,
            position == 0 ? outer : u0,
            outer,
            first * 3 + inner,
            queue * 3 + inner,
            next_b,
            next_y,
            states
        );
    }
}

void print_values(const std::vector<Metrics>& transcript, int field) {
    for (std::size_t index = 0; index < transcript.size(); ++index) {
        if (index != 0) {
            std::cout << ',';
        }
        if (field == 0) {
            std::cout << transcript[index].count;
        } else {
            std::cout << std::hex
                      << (field == 1 ? transcript[index].xor_fingerprint
                                     : transcript[index].sum_fingerprint)
                      << std::dec;
        }
    }
}

void solve(int n) {
    if (n < 11 || n > 33) {
        throw std::invalid_argument("native verifier supports 11 <= n <= 33");
    }
    std::unordered_set<std::uint32_t> states;
    states.reserve(10'000);
    initialize(0, 0, 0, 0, 0, 0, 0, states);
    std::vector<Metrics> transcript{metrics(states)};

    for (int position = k; position < n; ++position) {
        std::unordered_set<std::uint32_t> next;
        next.reserve(states.size() * 2);
        const int remaining = n - position - 1;
        for (const std::uint32_t encoded : states) {
            int u0;
            int first;
            int last;
            int queue;
            int b_count;
            int y_count;
            unpack(encoded, u0, first, last, queue, b_count, y_count);
            const auto first_values = trits(first);
            const int oldest = queue / power_four;

            for (const auto& column : columns) {
                const int outer = column[0];
                const int inner = column[1];
                if (!compatible(last, outer) || !compatible(oldest, inner)) {
                    continue;
                }
                if (position >= n - k &&
                    !compatible(inner, first_values[position - (n - k)])) {
                    continue;
                }
                if (position == n - 1 && !compatible(outer, u0)) {
                    continue;
                }
                const int next_b = b_count + (outer == 1) + (inner == 1);
                const int next_y = y_count + (outer == 2) + (inner == 2);
                if (next_b > limit || next_y > n || next_y + 2 * remaining < n) {
                    continue;
                }
                const int next_queue = (queue % power_four) * 3 + inner;
                next.insert(pack(u0, first, outer, next_queue, next_b, next_y));
            }
        }
        states = std::move(next);
        transcript.push_back(metrics(states));
    }

    std::cout << "n=" << n << " counterexample=" << (!states.empty() ? 1 : 0) << " counts=";
    print_values(transcript, 0);
    std::cout << " xor=";
    print_values(transcript, 1);
    std::cout << " sum=";
    print_values(transcript, 2);
    std::cout << '\n';
}
}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "provide at least one order\n";
        return 2;
    }
    try {
        for (int index = 1; index < argc; ++index) {
            solve(std::stoi(argv[index]));
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
    return 0;
}
