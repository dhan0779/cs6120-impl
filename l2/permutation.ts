function permutation(n: bigint, k: bigint): bigint {
    if (k > n) {
        return 0n;
    }
    return factorial(n) / factorial(n - k);
}

function factorial(n: bigint):bigint {
    for (let i = n - 1n; i > 0n; i=i-1n) {
        n = n * i;
    }
    return n;
}

function main(n: bigint, k: bigint) {
    var res: bigint = permutation(n, k);
    console.log(res);

}