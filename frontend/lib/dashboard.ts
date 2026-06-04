import { api } from "./api";

export const getPOSSummary = async (storeId: string) => {
  const res = await api.get(`/stores/${storeId}/pos/summary`);
  return res.data;
};

export const getMetrics = async (
  storeId: string
) => {
  const res = await api.get(
    `/stores/${storeId}/metrics`
  );

  return res.data;
};

export const getFunnel = async (
  storeId: string
) => {
  const res = await api.get(
    `/stores/${storeId}/funnel`
  );

  return res.data;
};

export const getVisualHeatmap = async (
  storeId: string
) => {
  const res = await api.get(
    `/stores/${storeId}/visual-heatmap`
  );

  return res.data;
};

export const getAnomalies = async (
  storeId: string
) => {
  const res = await api.get(
    `/stores/${storeId}/anomalies`
  );

  return res.data;
};

export const getLiveAnalytics = async (storeId: string) => {
  const res = await api.get(
    `/stores/${storeId}/live`
  );

  return res.data;
};

export const getHealth = async (
  storeId: string
) => {
  const res = await api.get(
    `/stores/${storeId}/health`
  );

  return res.data;
};

export const getCameras = async (storeId: string) => {
  const res = await api.get(`/stores/${storeId}/cameras`);
  return res.data;
};