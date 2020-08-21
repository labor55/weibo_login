function get_arg(e) {
    var ua = "5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    var t = a.md5(ua),
        r = "" + (new Date).getTime(),
        i = r + parseInt(10 * Math.random(), 10);
    return {
        ts: r,
        bv: t,
        salt: i,
        sign: n.md5("fanyideskweb" + e + i + "mmbP%A-r6U3Nw(n]BjuEU")
    }
}