#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {
constexpr int k = 6;
constexpr int separator_limit = 13;
constexpr int first_order = 34;
constexpr int last_order = 42;
constexpr int power_five = 243;
constexpr std::uint64_t empty = 0;
constexpr std::uint64_t key_mask = (1ULL << 30) - 1;
constexpr std::array<std::array<int, 2>, 7> columns{{
    {0, 0}, {0, 1}, {1, 0}, {1, 1}, {1, 2}, {2, 1}, {2, 2},
}};

struct Metrics {
    std::size_t count = 0;
    std::uint64_t xor_fingerprint = 0;
    std::uint64_t sum_fingerprint = 0;
};

std::uint64_t splitmix64(std::uint64_t value) {
    value += 0x9e3779b97f4a7c15ULL;
    value = (value ^ (value >> 30)) * 0xbf58476d1ce4e5b9ULL;
    value = (value ^ (value >> 27)) * 0x94d049bb133111ebULL;
    return value ^ (value >> 31);
}

class FlatMinSet {
  public:
    explicit FlatMinSet(std::size_t expected = 16) {
        std::size_t capacity = 16;
        while (capacity - capacity / 4 < expected) {
            capacity *= 2;
        }
        slots_.assign(capacity, empty);
    }

    void insert(std::uint64_t key, int cost) {
        if (key == empty) {
            throw std::logic_error("zero is reserved as the empty marker");
        }
        if (size_ + 1 > slots_.size() - slots_.size() / 4) {
            rehash(slots_.size() * 2);
        }
        insert_unchecked(key, cost);
    }

    [[nodiscard]] std::size_t size() const {
        return size_;
    }

    [[nodiscard]] const std::vector<std::uint64_t>& slots() const {
        return slots_;
    }

  private:
    std::vector<std::uint64_t> slots_;
    std::size_t size_ = 0;

    void insert_unchecked(std::uint64_t key, int cost) {
        const std::size_t mask = slots_.size() - 1;
        std::size_t index = splitmix64(key) & mask;
        while (slots_[index] != empty && (slots_[index] & key_mask) != key) {
            index = (index + 1) & mask;
        }
        if (slots_[index] == empty) {
            slots_[index] = key | (static_cast<std::uint64_t>(cost) << 32);
            ++size_;
        } else if (cost < static_cast<int>(slots_[index] >> 32)) {
            slots_[index] = key | (static_cast<std::uint64_t>(cost) << 32);
        }
    }

    void rehash(std::size_t capacity) {
        std::vector<std::uint64_t> previous = std::move(slots_);
        slots_.assign(capacity, empty);
        size_ = 0;
        for (const std::uint64_t encoded : previous) {
            if (encoded != empty) {
                insert_unchecked(encoded & key_mask, static_cast<int>(encoded >> 32));
            }
        }
    }
};

bool compatible(int left, int right) {
    return !((left == 0 && right == 2) || (left == 2 && right == 0));
}

std::uint64_t pack(int u0, int first, int last, int queue, int y_count) {
    return static_cast<std::uint64_t>(u0) |
           (static_cast<std::uint64_t>(first) << 2) |
           (static_cast<std::uint64_t>(last) << 12) |
           (static_cast<std::uint64_t>(queue) << 14) |
           (static_cast<std::uint64_t>(y_count) << 24);
}

void unpack(
    std::uint64_t encoded,
    int& u0,
    int& first,
    int& last,
    int& queue,
    int& b_count,
    int& y_count
) {
    u0 = encoded & 3;
    first = (encoded >> 2) & 1023;
    last = (encoded >> 12) & 3;
    queue = (encoded >> 14) & 1023;
    b_count = encoded >> 32;
    y_count = (encoded >> 24) & 63;
}

std::array<int, k> trits(int code) {
    std::array<int, k> result{};
    for (int index = k - 1; index >= 0; --index) {
        result[index] = code % 3;
        code /= 3;
    }
    return result;
}

void initialize(
    int position,
    int u0,
    int last,
    int first,
    int queue,
    int b_count,
    int y_count,
    FlatMinSet& states
) {
    if (position == k) {
        states.insert(pack(u0, first, last, queue, y_count), b_count);
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
        if (next_b > separator_limit) {
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

bool is_closed(std::uint64_t encoded, int order) {
    int u0;
    int first;
    int last;
    int queue;
    int b_count;
    int y_count;
    unpack(encoded, u0, first, last, queue, b_count, y_count);
    if (y_count != order || !compatible(last, u0)) {
        return false;
    }
    const auto first_values = trits(first);
    const auto last_values = trits(queue);
    for (int index = 0; index < k; ++index) {
        if (!compatible(last_values[index], first_values[index])) {
            return false;
        }
    }
    return true;
}

std::pair<Metrics, Metrics> measure(const FlatMinSet& states, int order) {
    Metrics all;
    Metrics closed;
    for (const std::uint64_t encoded : states.slots()) {
        if (encoded == empty) {
            continue;
        }
        const std::uint64_t fingerprint = splitmix64(encoded);
        ++all.count;
        all.xor_fingerprint ^= fingerprint;
        all.sum_fingerprint += fingerprint;
        if (order >= first_order && is_closed(encoded, order)) {
            ++closed.count;
            closed.xor_fingerprint ^= fingerprint;
            closed.sum_fingerprint += fingerprint;
        }
    }
    return {all, closed};
}

std::size_t next_expected(std::size_t current) {
    if (current < 1'000'000) {
        return current * 4;
    }
    if (current < 10'000'000) {
        return current * 3;
    }
    return current + current / 4;
}

void print_decimal(const std::vector<Metrics>& transcript, int field) {
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
}  // namespace

int main() {
    FlatMinSet states(30'000);
    initialize(0, 0, 0, 0, 0, 0, 0, states);
    std::vector<Metrics> layers;
    std::vector<Metrics> closures;
    layers.push_back(measure(states, k).first);

    for (int position = k; position < last_order; ++position) {
        FlatMinSet next(next_expected(states.size()));
        const int length = position + 1;
        const int minimum_y = std::max(0, 2 * length - last_order);
        for (const std::uint64_t encoded : states.slots()) {
            if (encoded == empty) {
                continue;
            }
            int u0;
            int first;
            int last;
            int queue;
            int b_count;
            int y_count;
            unpack(encoded, u0, first, last, queue, b_count, y_count);
            const int oldest = queue / power_five;

            for (const auto& column : columns) {
                const int outer = column[0];
                const int inner = column[1];
                if (!compatible(last, outer) || !compatible(oldest, inner)) {
                    continue;
                }
                const int next_b = b_count + (outer == 1) + (inner == 1);
                const int next_y = y_count + (outer == 2) + (inner == 2);
                if (next_b > separator_limit || next_y > last_order ||
                    next_y < minimum_y) {
                    continue;
                }
                const int next_queue = (queue % power_five) * 3 + inner;
                next.insert(pack(u0, first, outer, next_queue, next_y), next_b);
            }
        }
        states = std::move(next);
        auto [layer_metrics, closure_metrics] = measure(states, length);
        layers.push_back(layer_metrics);
        if (length >= first_order) {
            closures.push_back(closure_metrics);
        }
    }

    std::cout << "orders=";
    for (int order = first_order; order <= last_order; ++order) {
        if (order != first_order) {
            std::cout << ',';
        }
        std::cout << order;
    }
    std::cout << " closed=";
    print_decimal(closures, 0);
    std::cout << " closed_xor=";
    print_decimal(closures, 1);
    std::cout << " closed_sum=";
    print_decimal(closures, 2);
    std::cout << " counts=";
    print_decimal(layers, 0);
    std::cout << " xor=";
    print_decimal(layers, 1);
    std::cout << " sum=";
    print_decimal(layers, 2);
    std::cout << '\n';
}
