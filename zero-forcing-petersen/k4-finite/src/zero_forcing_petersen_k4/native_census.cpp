#include <openssl/evp.h>

#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr std::array<int, 4> kWeight = {0, 1, 1, 2};

class Sha256 {
  public:
    Sha256() : context_(EVP_MD_CTX_new(), EVP_MD_CTX_free) {
        if (context_ == nullptr || EVP_DigestInit_ex(context_.get(), EVP_sha256(), nullptr) != 1) {
            throw std::runtime_error("could not initialize SHA-256");
        }
    }

    void update(const unsigned char* data, std::size_t size) {
        if (EVP_DigestUpdate(context_.get(), data, size) != 1) {
            throw std::runtime_error("could not update SHA-256");
        }
    }

    std::string finish() {
        std::array<unsigned char, EVP_MAX_MD_SIZE> output{};
        unsigned int size = 0;
        if (EVP_DigestFinal_ex(context_.get(), output.data(), &size) != 1 || size != 32) {
            throw std::runtime_error("could not finalize SHA-256");
        }
        std::ostringstream encoded;
        encoded << std::hex << std::setfill('0');
        for (unsigned int index = 0; index < size; ++index) {
            encoded << std::setw(2) << static_cast<unsigned int>(output[index]);
        }
        return encoded.str();
    }

  private:
    std::unique_ptr<EVP_MD_CTX, decltype(&EVP_MD_CTX_free)> context_;
};

struct Census {
    int n;
    int target_weight;
    std::vector<int> word;
    std::vector<std::uint64_t> adjacency;
    std::uint64_t full_mask;
    std::uint64_t tested = 0;
    std::uint64_t forcing = 0;
    std::uint64_t first_witness = 0;
    Sha256 digest;

    explicit Census(int order, int weight)
        : n(order),
          target_weight(weight),
          word(static_cast<std::size_t>(order + 1)),
          adjacency(static_cast<std::size_t>(2 * order)),
          full_mask((std::uint64_t{1} << (2 * order)) - 1) {
        const std::array<unsigned char, 8> header = {
            'P',
            '4',
            'Z',
            '9',
            static_cast<unsigned char>(n),
            0,
            static_cast<unsigned char>(target_weight),
            0,
        };
        digest.update(header.data(), header.size());
        for (int index = 0; index < n; ++index) {
            adjacency[static_cast<std::size_t>(index)] =
                (std::uint64_t{1} << ((index + n - 1) % n)) |
                (std::uint64_t{1} << ((index + 1) % n)) |
                (std::uint64_t{1} << (n + index));
            adjacency[static_cast<std::size_t>(n + index)] =
                (std::uint64_t{1} << index) |
                (std::uint64_t{1} << (n + (index + n - 4) % n)) |
                (std::uint64_t{1} << (n + (index + 4) % n));
        }
    }

    std::uint64_t close(std::uint64_t initial) const {
        std::uint64_t black = initial;
        while (true) {
            std::uint64_t additions = 0;
            std::uint64_t sources = black;
            while (sources != 0) {
                const std::uint64_t bit = sources & (~sources + 1);
                sources -= bit;
                const int vertex = std::countr_zero(bit);
                const std::uint64_t white =
                    adjacency[static_cast<std::size_t>(vertex)] & ~black;
                if (std::has_single_bit(white)) {
                    additions |= white;
                }
            }
            const std::uint64_t updated = black | additions;
            if (updated == black) {
                return black;
            }
            black = updated;
        }
    }

    static void serialize(std::uint64_t value, unsigned char* output) {
        for (int byte = 0; byte < 8; ++byte) {
            output[byte] = static_cast<unsigned char>(value >> (8 * byte));
        }
    }

    void inspect() {
        std::uint64_t mask = 0;
        for (int index = 0; index < n; ++index) {
            const int symbol = word[static_cast<std::size_t>(index + 1)];
            if ((symbol & 1) != 0) {
                mask |= std::uint64_t{1} << index;
            }
            if ((symbol & 2) != 0) {
                mask |= std::uint64_t{1} << (n + index);
            }
        }

        const std::uint64_t closed = close(mask);
        std::array<unsigned char, 16> transcript{};
        serialize(mask, transcript.data());
        serialize(closed, transcript.data() + 8);
        digest.update(transcript.data(), transcript.size());
        ++tested;
        if (closed == full_mask) {
            ++forcing;
            if (first_witness == 0) {
                first_witness = mask;
            }
        }
    }

    void generate(int position, int period, int weight) {
        if (weight > target_weight ||
            weight + 2 * (n - position + 1) < target_weight) {
            return;
        }
        if (position > n) {
            if (n % period == 0 && weight == target_weight) {
                inspect();
            }
            return;
        }

        const int copied = word[static_cast<std::size_t>(position - period)];
        word[static_cast<std::size_t>(position)] = copied;
        generate(position + 1, period, weight + kWeight[static_cast<std::size_t>(copied)]);
        for (int symbol = copied + 1; symbol < 4; ++symbol) {
            word[static_cast<std::size_t>(position)] = symbol;
            generate(
                position + 1,
                position,
                weight + kWeight[static_cast<std::size_t>(symbol)]
            );
        }
    }
};

void run(int n) {
    if (n < 9 || n > 31) {
        throw std::invalid_argument("orders must lie in [9,31]");
    }
    Census census(n, 9);
    census.generate(1, 1, 0);
    std::cout << "n=" << n << " necklaces=" << census.tested
              << " forcing=" << census.forcing
              << " first_witness=" << census.first_witness
              << " sha256=" << census.digest.finish() << '\n';
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "usage: census N [N ...]\n";
        return EXIT_FAILURE;
    }
    try {
        for (int index = 1; index < argc; ++index) {
            run(std::stoi(argv[index]));
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return EXIT_FAILURE;
    }
}
