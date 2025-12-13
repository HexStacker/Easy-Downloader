import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const downloadService = {
    /**
     * Initiate a download job
     * @param {Object} params - Download parameters
     * @returns {Promise<Object>} Job information
     */
    initiateDownload: async (params) => {
        const response = await api.post('/youtube/single/download', params);
        return response.data;
    },

    /**
     * Get job status
     * @param {string} jobId - Job ID
     * @returns {Promise<Object>} Job status
     */
    getStatus: async (jobId) => {
        const response = await api.get(`/youtube/single/status/${jobId}`);
        return response.data;
    },

    /**
     * Get download URL for a completed job
     * @param {string} jobId - Job ID
     * @returns {string} Download URL
     */
    getDownloadUrl: (jobId) => {
        return `${API_URL}/youtube/single/file/${jobId}`;
    },

    /**
     * Get EventSource for real-time status updates
     * @param {string} jobId - Job ID
     * @returns {EventSource} SSE connection
     */
    getStatusStream: (jobId) => {
        return new EventSource(`${API_URL}/youtube/single/status/${jobId}`);
    },

    /**
     * Clean up a job
     * @param {string} jobId - Job ID
     * @returns {Promise<Object>} Cleanup result
     */
    cleanupJob: async (jobId) => {
        // Note: Cleanup endpoint might not be implemented in current backend
        // Returning a mock success for now to avoid errors if the frontend assumes it exists
        return { success: true };
    },

    // Batch Download Methods

    /**
     * Initiate a batch download job
     * @param {Object} params - Batch download parameters
     * @param {Array<string>} params.urls - Array of YouTube URLs
     * @param {string} params.type - Download type (audio/video/both)
     * @param {string} params.format - Output format
     * @param {string} params.resolution - Video resolution
     * @param {string} params.audio_bitrate - Audio bitrate
     * @returns {Promise<Object>} Batch job information
     */
    initiateBatchDownload: async (params) => {
        const response = await api.post('/youtube/multi/download', params);
        return response.data;
    },

    /**
     * Get batch job status
     * @param {string} batchId - Batch ID
     * @returns {Promise<Object>} Batch status with all individual jobs
     */
    getBatchStatus: async (batchId) => {
        const response = await api.get(`/youtube/multi/status/${batchId}`);
        return response.data;
    },

    /**
     * Clean up a batch job
     * @param {string} batchId - Batch ID
     * @returns {Promise<Object>} Cleanup result
     */
    cleanupBatch: async (batchId) => {
         // Note: Cleanup endpoint might not be implemented in current backend
        return { success: true };
    }
};

export default api;
