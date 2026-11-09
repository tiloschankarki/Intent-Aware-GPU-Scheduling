import io
import urllib.request
import zipfile

URL = (
    "https://tre-clusterdata.oss-cn-hangzhou.aliyuncs.com/"
    "cluster-trace-gpu-v2026/data/"
    "asi_opensource_pod_hourly.zip"
)

TARGET = (
    "asi_opensource_pod_hourly/"
    "day=109/hour=00/part-000.parquet"
)

SIZE = 351_803_513_445


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
            raise ValueError("Negative seek position")

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


remote = HTTPRangeReader(URL, SIZE)

print("Opening remote ZIP...")
with zipfile.ZipFile(remote, "r") as zf:
    print("ZIP opened successfully.")

    info = zf.getinfo(TARGET)
    output = "/tmp/day109_hour00.parquet"

    print()
    print("Extracting target member...")

    with zf.open(info, "r") as src, open(output, "wb") as dst:
        while True:
            chunk = src.read(8 * 1024 * 1024)  # 8 MiB
            if not chunk:
                break
            dst.write(chunk)

    print("Saved:", output)
    print()
    print("TARGET FOUND")
    print("filename:", info.filename)
    print("file_size:", info.file_size)
    print("file_size_MiB:", info.file_size / 1024**2)
    print("compress_size:", info.compress_size)
    print("compress_size_MiB:", info.compress_size / 1024**2)
    print("compress_type:", info.compress_type)
    print("header_offset:", info.header_offset)
    print("CRC:", hex(info.CRC))