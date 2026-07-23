#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <thread>
#include <vector>

#ifndef PETERSEN_K
#define PETERSEN_K 8
#endif

#ifndef PETERSEN_LIMIT
#define PETERSEN_LIMIT 17
#endif

#ifndef PETERSEN_FIRST_ORDER
#define PETERSEN_FIRST_ORDER 64
#endif

#ifndef PETERSEN_LAST_ORDER
#define PETERSEN_LAST_ORDER 72
#endif

namespace {
constexpr int k = PETERSEN_K;
constexpr int separator_limit = PETERSEN_LIMIT;
constexpr int first_order = PETERSEN_FIRST_ORDER;
constexpr int last_order = PETERSEN_LAST_ORDER;
constexpr std::uint64_t empty = 0;
constexpr int cost_shift = 32;
constexpr int last_shift = 1;
constexpr int queue_shift = 3;
constexpr int y_bits = 7;
constexpr std::array<std::array<int, 2>, 7> columns{{
    {0, 0}, {0, 1}, {1, 0}, {1, 1}, {1, 2}, {2, 1}, {2, 2},
}};

constexpr int power_of_three(int exponent) {
    int result = 1;
    for (int index = 0; index < exponent; ++index) {
        result *= 3;
    }
    return result;
}

constexpr int trit_codes = power_of_three(k);
constexpr int power_previous = power_of_three(k - 1);

constexpr int bits_for(int maximum) {
    int bits = 0;
    while ((1 << bits) <= maximum) {
        ++bits;
    }
    return bits;
}

constexpr int queue_bits = bits_for(trit_codes - 1);
constexpr int queue_mask = (1 << queue_bits) - 1;
constexpr int y_shift = queue_shift + queue_bits;
constexpr int key_bits = y_shift + y_bits;
constexpr std::uint64_t key_mask = (1ULL << key_bits) - 1;
constexpr int canonical_first_shift = 2;
constexpr int canonical_last_shift = canonical_first_shift + queue_bits;
constexpr int canonical_queue_shift = canonical_last_shift + 2;
constexpr int canonical_y_shift = canonical_queue_shift + queue_bits;

static_assert(k >= 3);
static_assert(last_order < (1 << y_bits));
static_assert(key_bits < cost_shift);
static_assert(canonical_y_shift + y_bits <= 40);

struct Metrics {
    std::uint64_t count = 0;
    std::uint64_t xor_fingerprint = 0;
    std::uint64_t sum_fingerprint = 0;

    Metrics& operator+=(const Metrics& other) {
        count += other.count;
        xor_fingerprint ^= other.xor_fingerprint;
        sum_fingerprint += other.sum_fingerprint;
        return *this;
    }
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
            slots_[index] = key | (static_cast<std::uint64_t>(cost) << cost_shift);
            ++size_;
        } else if (cost < static_cast<int>(slots_[index] >> cost_shift)) {
            slots_[index] = key | (static_cast<std::uint64_t>(cost) << cost_shift);
        }
    }

    void rehash(std::size_t capacity) {
        std::vector<std::uint64_t> previous = std::move(slots_);
        slots_.assign(capacity, empty);
        size_ = 0;
        for (const std::uint64_t encoded : previous) {
            if (encoded != empty) {
                insert_unchecked(
                    encoded & key_mask,
                    static_cast<int>(encoded >> cost_shift)
                );
            }
        }
    }
};

bool compatible(int left, int right) {
    return !((left == 0 && right == 2) || (left == 2 && right == 0));
}

std::uint64_t pack(int last, int queue, int y_count) {
    return 1ULL | (static_cast<std::uint64_t>(last) << last_shift) |
           (static_cast<std::uint64_t>(queue) << queue_shift) |
           (static_cast<std::uint64_t>(y_count) << y_shift);
}

void unpack(
    std::uint64_t encoded,
    int& last,
    int& queue,
    int& b_count,
    int& y_count
) {
    last = (encoded >> last_shift) & 3;
    queue = (encoded >> queue_shift) & queue_mask;
    b_count = encoded >> cost_shift;
    y_count = (encoded >> y_shift) & ((1 << y_bits) - 1);
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
    int last,
    int b_count,
    int y_count,
    int first_code,
    const std::array<int, k>& first_values,
    FlatMinSet& states
) {
    if (position == k) {
        states.insert(pack(last, first_code, y_count), b_count);
        return;
    }
    const int inner = first_values[position];
    for (int outer = 0; outer < 3; ++outer) {
        if ((position == 0 && outer != 1) || !compatible(outer, inner) ||
            (position > 0 && !compatible(last, outer))) {
            continue;
        }
        const int next_b = b_count + (outer == 1) + (inner == 1);
        const int next_y = y_count + (outer == 2) + (inner == 2);
        if (next_b <= separator_limit) {
            initialize(
                position + 1,
                outer,
                next_b,
                next_y,
                first_code,
                first_values,
                states
            );
        }
    }
}

bool is_closed(
    std::uint64_t encoded,
    int order,
    const std::array<int, k>& first_values
) {
    int last;
    int queue;
    int b_count;
    int y_count;
    unpack(encoded, last, queue, b_count, y_count);
    if (y_count != order || !compatible(last, 1)) {
        return false;
    }
    const auto last_values = trits(queue);
    for (int index = 0; index < k; ++index) {
        if (!compatible(last_values[index], first_values[index])) {
            return false;
        }
    }
    return true;
}

std::uint64_t canonical_state(std::uint64_t encoded, int first_code) {
    int last;
    int queue;
    int b_count;
    int y_count;
    unpack(encoded, last, queue, b_count, y_count);
    return 1ULL |
           (static_cast<std::uint64_t>(first_code) << canonical_first_shift) |
           (static_cast<std::uint64_t>(last) << canonical_last_shift) |
           (static_cast<std::uint64_t>(queue) << canonical_queue_shift) |
           (static_cast<std::uint64_t>(y_count) << canonical_y_shift) |
           (static_cast<std::uint64_t>(b_count) << 40);
}

std::pair<Metrics, Metrics> measure(
    const FlatMinSet& states,
    int order,
    int first_code,
    const std::array<int, k>& first_values
) {
    Metrics all;
    Metrics closed;
    for (const std::uint64_t encoded : states.slots()) {
        if (encoded == empty) {
            continue;
        }
        const std::uint64_t fingerprint = splitmix64(canonical_state(encoded, first_code));
        ++all.count;
        all.xor_fingerprint ^= fingerprint;
        all.sum_fingerprint += fingerprint;
        if (order >= first_order && is_closed(encoded, order, first_values)) {
            ++closed.count;
            closed.xor_fingerprint ^= fingerprint;
            closed.sum_fingerprint += fingerprint;
        }
    }
    return {all, closed};
}

std::size_t next_expected(std::size_t current) {
    if (current < 1'000'000) {
        return std::max<std::size_t>(16, current * 4);
    }
    if (current < 10'000'000) {
        return current * 3;
    }
    return current + current / 4;
}

struct Transcript {
    std::vector<Metrics> layers;
    std::vector<Metrics> closures;

    Transcript()
        : layers(last_order - k + 1),
          closures(last_order - first_order + 1) {
    }
};

void process_partition(int first_code, Transcript& transcript) {
    const auto first_values = trits(first_code);
    FlatMinSet states;
    initialize(0, 0, 0, 0, first_code, first_values, states);
    transcript.layers[0] += measure(states, k, first_code, first_values).first;

    for (int position = k; position < last_order && states.size() > 0; ++position) {
        FlatMinSet next(next_expected(states.size()));
        const int length = position + 1;
        const int minimum_y = std::max(0, 2 * length - last_order);
        for (const std::uint64_t encoded : states.slots()) {
            if (encoded == empty) {
                continue;
            }
            int last;
            int queue;
            int b_count;
            int y_count;
            unpack(encoded, last, queue, b_count, y_count);
            const int oldest = queue / power_previous;

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
                const int next_queue = (queue % power_previous) * 3 + inner;
                next.insert(pack(outer, next_queue, next_y), next_b);
            }
        }
        states = std::move(next);
        auto [layer_metrics, closure_metrics] =
            measure(states, length, first_code, first_values);
        transcript.layers[length - k] += layer_metrics;
        if (length >= first_order) {
            transcript.closures[length - first_order] += closure_metrics;
        }
    }
}

void print_metrics(const std::vector<Metrics>& transcript, int field) {
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

int main(int argc, char** argv) {
    int thread_count = static_cast<int>(std::thread::hardware_concurrency());
    if (argc == 2) {
        thread_count = std::stoi(argv[1]);
    } else if (argc != 1) {
        throw std::invalid_argument("usage: native_partitioned [threads]");
    }
    if (thread_count < 1) {
        throw std::invalid_argument("thread count must be positive");
    }
    thread_count = std::min(thread_count, trit_codes);

    std::atomic<int> next_code = 0;
    std::atomic<int> completed = 0;
    std::mutex progress_mutex;
    std::vector<Transcript> worker_transcripts(thread_count);
    std::vector<std::thread> workers;
    workers.reserve(thread_count);
    for (int worker = 0; worker < thread_count; ++worker) {
        workers.emplace_back([&, worker]() {
            while (true) {
                const int first_code = next_code.fetch_add(1);
                if (first_code >= trit_codes) {
                    return;
                }
                process_partition(first_code, worker_transcripts[worker]);
                const int done = completed.fetch_add(1) + 1;
                if (done % 256 == 0 || done == trit_codes) {
                    const std::lock_guard lock(progress_mutex);
                    std::cerr << "partitions=" << done << '/' << trit_codes << '\n';
                }
            }
        });
    }
    for (auto& worker : workers) {
        worker.join();
    }

    Transcript combined;
    for (const Transcript& transcript : worker_transcripts) {
        for (std::size_t index = 0; index < combined.layers.size(); ++index) {
            combined.layers[index] += transcript.layers[index];
        }
        for (std::size_t index = 0; index < combined.closures.size(); ++index) {
            combined.closures[index] += transcript.closures[index];
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
    print_metrics(combined.closures, 0);
    std::cout << " closed_xor=";
    print_metrics(combined.closures, 1);
    std::cout << " closed_sum=";
    print_metrics(combined.closures, 2);
    std::cout << " counts=";
    print_metrics(combined.layers, 0);
    std::cout << " xor=";
    print_metrics(combined.layers, 1);
    std::cout << " sum=";
    print_metrics(combined.layers, 2);
    std::cout << '\n';
}
