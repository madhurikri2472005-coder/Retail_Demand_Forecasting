from pathlib import Path

input_file = Path.home() / "Downloads" / "sell_prices.csv"
output_dir = Path.home() / "Downloads"

max_size = 70 * 1024 * 1024  # 70 MB

with open(input_file, "rb") as f:
    header = f.readline()

    part = 1
    output_file = output_dir / f"sell_prices_part{part}.csv"
    out = open(output_file, "wb")
    out.write(header)
    current_size = len(header)

    for line in f:
        if current_size + len(line) > max_size:
            out.close()

            part += 1
            output_file = output_dir / f"sell_prices_part{part}.csv"
            out = open(output_file, "wb")
            out.write(header)
            current_size = len(header)

        out.write(line)
        current_size += len(line)

    out.close()

print(f"Created {part} parts successfully.")