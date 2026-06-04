import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/cctv/:path*",
        destination: `${process.env.BACKEND_URL || "http://127.0.0.1:8000"}/cctv/:path*`,
      },
    ];
  },
};

export default nextConfig;
