// Test double for the network. Routes map a URL to a response or a list of
// responses served in order. Every call is logged with its headers so tests
// can assert what Telos sent. Excluded from the npm package.
import { ResponseCache } from "./cache.mjs";
import { ReachHttp } from "./http.mjs";
import { HostLimiter } from "./limiter.mjs";

const NO_BODY = new Set([204, 304]);

export function fakeFetch(routes) {
  const calls = [];
  const served = new Map();
  const fetchImpl = async (url, init = {}) => {
    const headers = Object.fromEntries(Object.entries(init.headers ?? {}).map(([k, v]) => [k.toLowerCase(), v]));
    calls.push({ url, method: init.method ?? "GET", headers, body: init.body ?? null });
    let route = routes[url];
    if (Array.isArray(route)) {
      const n = served.get(url) ?? 0;
      served.set(url, n + 1);
      route = route[Math.min(n, route.length - 1)];
    }
    if (typeof route === "function") route = route({ url, headers });
    if (route instanceof Error) throw route;
    const spec = route ?? { status: 404, body: "not found" };
    const status = spec.status ?? 200;
    return new Response(NO_BODY.has(status) ? null : spec.body ?? "", { status, headers: spec.headers ?? {} });
  };
  return { fetchImpl, calls };
}

/** A ReachHttp on a fake clock: sleeps advance time instantly and are logged. */
export function fakeHttp(routes, { env = {}, cacheDir = null } = {}) {
  let clock = 1_000_000;
  const sleeps = [];
  const now = () => clock;
  const sleep = async (ms) => {
    sleeps.push(ms);
    clock += ms;
  };
  const { fetchImpl, calls } = fakeFetch(routes);
  const limiter = new HostLimiter({ now, sleep });
  const cache = new ResponseCache({ dir: cacheDir, now });
  const http = new ReachHttp({ fetchImpl, limiter, cache, env });
  return { http, calls, sleeps, advance: (ms) => (clock += ms), now };
}
