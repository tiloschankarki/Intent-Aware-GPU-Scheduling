import io
import urllib.request
import zipfile
import re
from collections import defaultdict

URL = (
    "https://tre-clusterdata.oss-cn-hangzhou.aliyuncs.com/"
    "cluster-trace-gpu-v2026/data/"
    "asi_opensource_pod_hourly.zip"
)

SIZE = 351_803_513_445

PATTERN = re.compile(
    r"asi_opensource_pod_hourly/"
    r"day=(\d+)/hour=(\d+)/part-000\.parquet$"
)


class HTTPRangeReader(io.RawIOBase):
    def __init__(self, url, size):
        self.url = url
        self.size = size
        self.pos = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=io.SEEK_SET):
        if whence == io.SEEK_SET:
            new_pos = offset
        elif whence == io.SEEK_CUR:
            new_pos = self.pos + offset
        elif whence == io.SEEK_END:
            new_pos = self.size + offset
        else:
            raise ValueError("Invalid whence")

        if new_pos < 0:
            raise ValueError("Negative seek")

        self.pos = new_pos
        return self.pos

    def read(self, n=-1):
        if self.pos >= self.size:
            return b""

        if n is None or n < 0:
            n = self.size - self.pos

        end = min(self.pos + n, self.size)

        req = urllib.request.Request(
            self.url,
            headers={
                "Range": f"bytes={self.pos}-{end - 1}",
                "User-Agent": "ASI-research-range-reader/1.0",
            },
        )

        with urllib.request.urlopen(req) as response:
            data = response.read()

        self.pos += len(data)
        return data


print("Opening remote ZIP central directory...")

remote = HTTPRangeReader(URL, SIZE)

daily = defaultdict(lambda: {
    "hours": 0,
    "bytes": 0,
    "uncompressed": 0
})

members = []

with zipfile.ZipFile(remote, "r") as zf:

    for info in zf.infolist():
        m = PATTERN.match(info.filename)

        if not m:
            continue

        day = int(m.group(1))
        hour = int(m.group(2))

        daily[day]["hours"] += 1
        daily[day]["bytes"] += info.compress_size
        daily[day]["uncompressed"] += info.file_size

        members.append({
            "day": day,
            "hour": hour,
            "size": info.compress_size,
            "uncompressed": info.file_size,
            "compression": info.compress_type,
        })


print("\n=== ARCHIVE SUMMARY ===")
print(f"Hourly parquet members: {len(members):,}")
print(f"Days represented:       {len(daily):,}")

if daily:
    print(f"Day range:              {min(daily)} - {max(daily)}")

total_bytes = sum(x["size"] for x in members)

print(
    f"Total hourly data:      "
    f"{total_bytes / 1024**3:,.2f} GiB"
)

print()


print("=== DAILY TRANSFER SIZE ===")
print(f"{'DAY':>4} {'HOURS':>6} {'GiB':>10} {'MiB/HOUR':>12}")
print("-" * 38)

for day in sorted(daily):

    d = daily[day]

    gib = d["bytes"] / 1024**3

    avg_mib = (
        d["bytes"] / d["hours"] / 1024**2
        if d["hours"]
        else 0
    )

    print(
        f"{day:>4} "
        f"{d['hours']:>6} "
        f"{gib:>10.3f} "
        f"{avg_mib:>12.1f}"
    )


print("\n=== DAYS WE ARE CONSIDERING ===")

candidate_days = [50, 100, 108, 109, 110, 120, 129, 130, 150, 180]

candidate_total = 0

for day in candidate_days:

    if day not in daily:
        print(f"Day {day:>3}: NOT PRESENT")
        continue

    size = daily[day]["bytes"]
    candidate_total += size

    print(
        f"Day {day:>3}: "
        f"{daily[day]['hours']:>2} hours | "
        f"{size / 1024**3:.3f} GiB"
    )

print(
    f"\nAll candidate days combined: "
    f"{candidate_total / 1024**3:.3f} GiB"
)


print("\n=== COMPRESSION METHODS ===")

methods = {}

for x in members:
    methods[x["compression"]] = methods.get(x["compression"], 0) + 1

for method, count in sorted(methods.items()):
    print(f"method {method}: {count:,} members")


print("\n=== HOURLY SIZE EXTREMES ===")

smallest = min(members, key=lambda x: x["size"])
largest = max(members, key=lambda x: x["size"])

print(
    f"Smallest: day={smallest['day']} "
    f"hour={smallest['hour']:02d} "
    f"{smallest['size']/1024**2:.2f} MiB"
)

print(
    f"Largest:  day={largest['day']} "
    f"hour={largest['hour']:02d} "
    f"{largest['size']/1024**2:.2f} MiB"
)