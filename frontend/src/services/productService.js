const API_URL = import.meta.env.VITE_API_URL || `${window.location.protocol}//${window.location.hostname}:5000`;

export const checkProduct = async (productsData) => {
    const response = await fetch(`${API_URL}/check`, {
        method: 'POST',
        headers: { 'Content-type': 'application/json' },
        body: JSON.stringify({ items: productsData }),
    })
    
    if (!response.ok) {
        throw new Error('Network error was not OK');
    }

    return await response.json();
}