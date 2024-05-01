// Get cookie for CSRF token verification
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Make fetch request to Django API
async function makeRequest(url, method, data, ) {
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: data
    });
    return response;
}

// Get json data from response
async function getJson(response) {
    const data = await response.json();
    return data;
}

// Definitions
const VehicleType = {
    VEHICLE: 'vehicle',
    PEDESTRIAN: 'pedestrian'
};

export { getCookie, VehicleType };