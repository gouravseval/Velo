/// <reference types="vite/client" />
import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
})

export const API_BASE_URL = BASE_URL
