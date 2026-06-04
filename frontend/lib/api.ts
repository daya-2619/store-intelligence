import axios from "axios";

const isServer = typeof window === 'undefined';

export const api = axios.create({
    baseURL: isServer ? (process.env.BACKEND_URL || "http://127.0.0.1:8000") : "http://127.0.0.1:8000",
});