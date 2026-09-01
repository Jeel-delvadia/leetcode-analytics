// Utility helper functions for LeetCode Extension

export function parseRuntime(runtimeStr) {
  if (!runtimeStr) return null;
  const match = runtimeStr.match(/(\d+)/);
  return match ? parseInt(match[1], 10) : null;
}

export function parseMemory(memoryStr) {
  if (!memoryStr) return null;
  const match = memoryStr.match(/([\d.]+)\s*(MB|KB)/i);
  if (!match) return null;
  const val = parseFloat(match[1]);
  const unit = match[2].toUpperCase();
  return unit === 'MB' ? Math.round(val * 1024) : Math.round(val);
}

export function formatDate(timestamp) {
  const d = typeof timestamp === 'number' ? new Date(timestamp * 1000) : new Date(timestamp);
  return d.toISOString();
}
