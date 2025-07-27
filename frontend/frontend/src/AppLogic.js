    // api.js (or similar file)
    import axios from 'axios';

    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';
    axios.defaults.withCredentials = true; // Essential for sending cookies with cross-origin requests

    export const api = axios.create({
        baseURL: 'http://localhost:8000/api/', // Your Django API base URL
    });