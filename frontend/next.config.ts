import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,  // Ensures /admin generates /admin/index.html
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
