function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
}


async function login() {
    const username = document.getElementById("name").value;
    const password = document.getElementById("pass").value;

    const response = await fetch('/auth/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({username: username, password: password})
    });

    const data = await response.json();
    console.log(data);
}
