class union_find:
    def __init__(self, n: int) -> None:
        assert 0 <= n
        self.n = n
        self.parent_or_size = [-1] * n

    def unite(self, u: int, v: int) -> None:
        assert 0 <= u < self.n
        assert 0 <= v < self.n
        u = self.find(u)
        v = self.find(v)

        if u != v:
            if self.parent_or_size[u] > self.parent_or_size[v]:
                u, v = v, u

            self.parent_or_size[u] += self.parent_or_size[v]
            self.parent_or_size[v] = u

    def find(self, u: int) -> int:
        assert 0 <= u < self.n
        if self.parent_or_size[u] < 0:
            return u
        else:
            self.parent_or_size[u] = self.find(self.parent_or_size[u])
            return self.parent_or_size[u]

    def group_size(self, u: int) -> int:
        assert 0 <= u < self.n
        return -self.parent_or_size[self.find(u)]


def main() -> None:
    N, M = map(int, input().split())
    u = union_find(N)

    for _ in range(M):
        A, B = map(int, input().split())
        assert 1 <= A <= N
        assert 1 <= B <= N

        A -= 1
        B -= 1

        u.unite(A, B)

    assert 2 <= N <= 100
    assert 1 <= M <= N * (N - 1) // 2
    assert u.group_size(0) == N


if __name__ == '__main__':
    main()
