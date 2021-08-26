import itertools


def main() -> None:
    S, K_str = input().split()

    assert 1 <= len(S) <= 8
    assert S.islower()

    K_max = 0
    for _ in itertools.permutations(sorted(list(S))):
        K_max += 1

    assert 1 <= int(K_str) <= K_max


if __name__ == '__main__':
    main()
