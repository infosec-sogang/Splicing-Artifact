#!/usr/bin/env python3
import os, sys, re
from utils import check_fuzzlog, FUZZ_LOG_NAME

FUZZER_STATS_NAME = "default/fuzzer_stats"
INTERESTING_DIRS = ("default/queue",)


def read_fuzzer_stats(bench_dir):
    stats = {}
    with open(os.path.join(bench_dir, FUZZER_STATS_NAME)) as f:
        for line in f:
            if ":" in line:
                key, value = line.split(":", 1)
                stats[key.strip()] = value.strip()
    return stats


def count_splicing_finds(bench_dir):
    count = 0
    for sub in INTERESTING_DIRS:
        d = os.path.join(bench_dir, sub)
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            if "op:search" in name or "op:splice" in name:
                count += 1
    return count


def analyze_iteration(bench_dir):
    stats = read_fuzzer_stats(bench_dir)

    search_execs = int(stats.get("search_execs", 0))
    splice_execs = int(stats.get("splice_execs", stats.get("splice_cycles", 0)))
    search_time_ms = int(stats.get("search_time_ms", 0))
    splice_time_ms = int(stats.get("splice_time_ms", 0))

    splicing_execs = search_execs + splice_execs
    splicing_time_s = (search_time_ms + splice_time_ms) / 1000.0

    interesting = count_splicing_finds(bench_dir)

    effectiveness = (interesting / splicing_execs) if splicing_execs else 0.0
    throughput = (splicing_execs / splicing_time_s) if splicing_time_s else 0.0

    return {
        "interesting": interesting,
        "splicing_execs": splicing_execs,
        "splicing_time_s": splicing_time_s,
        "effectiveness": effectiveness,
        "throughput": throughput,
    }


def analyze_benchmark(outdir, iter_cnt, bench_name, verbose=False):
    rows = []
    for i in range(iter_cnt):
        bench_dir = os.path.join(outdir, "%s-%d" % (bench_name, i))
        stats_path = os.path.join(bench_dir, FUZZER_STATS_NAME)
        if not os.path.isfile(stats_path):
            continue

        row = analyze_iteration(bench_dir)
        rows.append(row)

        if verbose:
            print(f"(iter #{i}) interesting: {row['interesting']} / "
                  f"execs: {row['splicing_execs']} / "
                  f"time(s): {row['splicing_time_s']:.0f}"
                  f"\n\teffectiveness: {row['effectiveness']:.4%}"
                  f"\n\tthroughput: {row['throughput']:.1f} execs/sec")

    if not rows:
        return None

    def avg(key):
        return sum(r[key] for r in rows) / len(rows)

    result = {
        "n": len(rows),
        "interesting": avg("interesting"),
        "splicing_execs": avg("splicing_execs"),
        "splicing_time_s": avg("splicing_time_s"),
        "effectiveness": avg("effectiveness"),
        "throughput": avg("throughput"),
    }

    print(f"interesting: {result['interesting']:.1f} / "
          f"execs: {result['splicing_execs']:.0f} / "
          f"time(s): {result['splicing_time_s']:.0f}"
          f"\nsplicing effectiveness: {result['effectiveness']:.4%}"
          f"\nsplicing throughput: {result['throughput']:.1f} execs/sec")

    return result


def analyze_outdir(outdir, iter_cnt, verbose=False):
    done_benchmarks = []
    results = {}
    for dirname in sorted(os.listdir(outdir)):
        if dirname == FUZZ_LOG_NAME:
            continue
        if not os.path.isdir(os.path.join(outdir, dirname)):
            continue
        bench_name = re.sub(r"-\d+$", "", dirname)
        if bench_name == dirname or bench_name in done_benchmarks:
            continue
        print("[*] Analysis of %s" % bench_name)
        result = analyze_benchmark(outdir, iter_cnt, bench_name, verbose)
        print("=====================================")
        done_benchmarks.append(bench_name)
        if result:
            results[bench_name] = result

    print("\n[*] Summary")
    print(f"{'benchmark':<24} {'effectiveness':>14} {'throughput (execs/s)':>22}")
    for bench_name, result in results.items():
        print(f"{bench_name:<24} {result['effectiveness']:>14.4%} "
              f"{result['throughput']:>22.1f}")


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: %s <outdir path> [verbose (on/off)]" % sys.argv[0])
        exit(1)
    outdir = sys.argv[1]
    verbose = (len(sys.argv) == 3 and sys.argv[2] == "on")
    _, _, iter_cnt = check_fuzzlog(outdir)
    analyze_outdir(outdir, iter_cnt, verbose)


if __name__ == "__main__":
    main()
