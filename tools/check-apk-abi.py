#!/usr/bin/env python3
"""报告 APK 内含的 native ABI。

存在的意义：csproj 里写 <RuntimeIdentifiers> 时，只给 -r 不一定能让产物
变成单架构，会出现「步骤成功、包却是混架构」的静默失败。CI 里编完必须验。

用法: check-apk-abi.py <apk> [期望abi]
      给了期望值时，不符则退出码 1。
"""
import sys
import zipfile


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    apk = argv[1]
    expect = argv[2] if len(argv) > 2 else None

    try:
        with zipfile.ZipFile(apk) as z:
            names = z.namelist()
    except (OSError, zipfile.BadZipFile) as e:
        print("::error::读不了 APK：%s" % e)
        return 1

    abis = sorted({n.split("/")[1] for n in names
                   if n.startswith("lib/") and n.count("/") >= 2})
    print("%s 内含 ABI: %s" % (apk, abis))

    if expect is None:
        return 0
    if abis == [expect]:
        print("OK：纯 %s" % expect)
        return 0
    print("::warning::期望纯 %s，实际 %s" % (expect, abis))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
