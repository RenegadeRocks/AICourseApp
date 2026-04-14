/** @type {import('next').NextConfig} */
const path = require("path");
module.exports = {
  typedRoutes: true,
  // Vault lives one level up — allow reading it at runtime
  outputFileTracingRoot: path.join(__dirname, ".."),
  webpack: (config) => {
    config.externals = [...(config.externals || []), "better-sqlite3"];
    return config;
  },
};
